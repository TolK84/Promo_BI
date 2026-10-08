-- demo_agro: схема демо-базы (звезда). Запуск:
--   docker exec -i superset_db psql -U demo_user -d demo_agro < schema.sql
-- Затем данные: python3 generate_mock.py > data.sql && docker exec -i superset_db psql -U demo_user -d demo_agro < data.sql

DROP VIEW  IF EXISTS v_supplier_debt, v_payment_schedule_status, v_contract_summary, v_order_line_status CASCADE;
DROP TABLE IF EXISTS fact_sales_plan, fact_payment_out, fact_purchase_line, fact_payment_in, fact_payment_schedule,
                     fact_sales_line, fact_order_line, dim_contract, dim_warehouse, dim_product, dim_product_group,
                     dim_manufacturer, dim_supplier, dim_customer, dim_manager, dim_division, dim_season,
                     dim_date, dim_report_date CASCADE;

-- ---------- Справочники ----------

CREATE TABLE dim_report_date (report_date date PRIMARY KEY);      -- «дата формирования»: на неё считаются просрочки и долг

CREATE TABLE dim_date (
    date_id     date PRIMARY KEY,
    year        int  NOT NULL,
    quarter     int  NOT NULL,
    month       int  NOT NULL,
    month_name  text NOT NULL,
    month_start date NOT NULL,
    week        int  NOT NULL,
    weekday     int  NOT NULL            -- 1 = понедельник
);

CREATE TABLE dim_season   (season_id int PRIMARY KEY, name text NOT NULL, year int NOT NULL);
CREATE TABLE dim_division (division_id int PRIMARY KEY, name text NOT NULL);
CREATE TABLE dim_manager  (manager_id int PRIMARY KEY, name text NOT NULL, division_id int NOT NULL REFERENCES dim_division);
CREATE TABLE dim_customer (customer_id int PRIMARY KEY, name text NOT NULL, region text NOT NULL, manager_id int NOT NULL REFERENCES dim_manager);
CREATE TABLE dim_supplier (supplier_id int PRIMARY KEY, name text NOT NULL, country text NOT NULL);
CREATE TABLE dim_manufacturer  (manufacturer_id int PRIMARY KEY, name text NOT NULL);
CREATE TABLE dim_product_group (group_id int PRIMARY KEY, name text NOT NULL);
CREATE TABLE dim_product (
    product_id      int PRIMARY KEY,
    name            text NOT NULL,
    group_id        int  NOT NULL REFERENCES dim_product_group,
    manufacturer_id int  NOT NULL REFERENCES dim_manufacturer,
    unit            text NOT NULL
);
CREATE TABLE dim_warehouse (warehouse_id int PRIMARY KEY, name text NOT NULL);

CREATE TABLE dim_contract (
    contract_id       int PRIMARY KEY,
    number            text NOT NULL,
    customer_id       int  NOT NULL REFERENCES dim_customer,
    manager_id        int  NOT NULL REFERENCES dim_manager,
    season_id         int  NOT NULL REFERENCES dim_season,
    contract_date     date NOT NULL,
    amount            numeric(18,2) NOT NULL,
    sign_type         text NOT NULL,      -- 'Электронный' / 'Бумажный'
    original_received boolean NOT NULL,   -- оригинал договора получен
    status            text NOT NULL       -- 'Действует' / 'Закрыт'
);

-- ---------- Факты ----------

-- Заказы клиентов (строка = товар в заказе)
CREATE TABLE fact_order_line (
    order_line_id int PRIMARY KEY,
    order_id      int  NOT NULL,
    order_date    date NOT NULL,
    contract_id   int  NOT NULL REFERENCES dim_contract,
    customer_id   int  NOT NULL REFERENCES dim_customer,
    manager_id    int  NOT NULL REFERENCES dim_manager,
    season_id     int  NOT NULL REFERENCES dim_season,
    product_id    int  NOT NULL REFERENCES dim_product,
    warehouse_id  int  NOT NULL REFERENCES dim_warehouse,
    qty           numeric(18,2) NOT NULL,
    price         numeric(18,2) NOT NULL,
    amount        numeric(18,2) NOT NULL
);

-- Продажи (реализации): выручка и себестоимость, отсюда маржа
CREATE TABLE fact_sales_line (
    sale_line_id  int PRIMARY KEY,
    sale_id       int  NOT NULL,
    sale_date     date NOT NULL,
    order_line_id int  NOT NULL REFERENCES fact_order_line,
    order_id      int  NOT NULL,
    contract_id   int  NOT NULL REFERENCES dim_contract,
    customer_id   int  NOT NULL REFERENCES dim_customer,
    manager_id    int  NOT NULL REFERENCES dim_manager,
    season_id     int  NOT NULL REFERENCES dim_season,
    product_id    int  NOT NULL REFERENCES dim_product,
    warehouse_id  int  NOT NULL REFERENCES dim_warehouse,
    qty           numeric(18,2) NOT NULL,
    amount        numeric(18,2) NOT NULL,
    cost_amount   numeric(18,2) NOT NULL
);

-- График платежей по договору
CREATE TABLE fact_payment_schedule (
    contract_id int  NOT NULL REFERENCES dim_contract,
    stage_no    int  NOT NULL,
    due_date    date NOT NULL,
    percent     numeric(5,2)  NOT NULL,
    amount      numeric(18,2) NOT NULL,
    kind        text NOT NULL,            -- 'Предоплата' / 'Оплата'
    PRIMARY KEY (contract_id, stage_no)
);

-- Оплаты от клиентов
CREATE TABLE fact_payment_in (
    payment_id   int PRIMARY KEY,
    payment_date date NOT NULL,
    customer_id  int  NOT NULL REFERENCES dim_customer,
    contract_id  int  NOT NULL REFERENCES dim_contract,
    amount       numeric(18,2) NOT NULL,
    purpose      text NOT NULL            -- 'Предоплата' / 'Оплата'
);

-- Закупки у поставщиков
CREATE TABLE fact_purchase_line (
    purchase_line_id int PRIMARY KEY,
    purchase_id      int  NOT NULL,
    purchase_date    date NOT NULL,
    supplier_id      int  NOT NULL REFERENCES dim_supplier,
    product_id       int  NOT NULL REFERENCES dim_product,
    warehouse_id     int  NOT NULL REFERENCES dim_warehouse,
    qty              numeric(18,2) NOT NULL,
    amount           numeric(18,2) NOT NULL
);

-- Оплаты поставщикам
CREATE TABLE fact_payment_out (
    payment_id   int PRIMARY KEY,
    payment_date date NOT NULL,
    supplier_id  int  NOT NULL REFERENCES dim_supplier,
    purchase_id  int  NOT NULL,
    amount       numeric(18,2) NOT NULL
);

-- План продаж (месяц × менеджер × группа товаров)
CREATE TABLE fact_sales_plan (
    plan_month       date NOT NULL,
    manager_id       int  NOT NULL REFERENCES dim_manager,
    division_id      int  NOT NULL REFERENCES dim_division,
    product_group_id int  NOT NULL REFERENCES dim_product_group,
    plan_amount      numeric(18,2) NOT NULL,
    plan_qty         numeric(18,2) NOT NULL,
    PRIMARY KEY (plan_month, manager_id, product_group_id)
);

CREATE INDEX ON fact_order_line (contract_id);
CREATE INDEX ON fact_sales_line (contract_id);
CREATE INDEX ON fact_sales_line (order_line_id);
CREATE INDEX ON fact_sales_line (sale_date);
CREATE INDEX ON fact_payment_in (contract_id);
CREATE INDEX ON fact_payment_in (payment_date);
CREATE INDEX ON fact_purchase_line (purchase_id);
CREATE INDEX ON fact_payment_out (purchase_id);

-- ---------- Представления (аналоги DAX-мер) ----------

-- Статус отгрузки по строкам заказов
CREATE VIEW v_order_line_status AS
SELECT o.order_line_id, o.order_id, o.contract_id, o.product_id, o.qty AS ordered_qty,
       COALESCE(s.shipped_qty, 0) AS shipped_qty,
       o.qty - COALESCE(s.shipped_qty, 0) AS remaining_qty,
       CASE WHEN COALESCE(s.shipped_qty, 0) = 0     THEN 'Не отгружен'
            WHEN COALESCE(s.shipped_qty, 0) < o.qty THEN 'Частично отгружен'
            ELSE 'Отгружен' END AS ship_status
FROM fact_order_line o
LEFT JOIN (SELECT order_line_id, SUM(qty) AS shipped_qty FROM fact_sales_line GROUP BY 1) s USING (order_line_id);

-- Договор: сумма, отгружено, оплачено, задолженность (debt > 0) или остаток предоплаты (debt < 0)
CREATE VIEW v_contract_summary AS
SELECT c.contract_id, c.number, c.customer_id, c.manager_id, c.season_id, c.contract_date, c.status,
       c.amount                               AS contract_amount,
       COALESCE(s.shipped, 0)                 AS shipped_amount,
       COALESCE(p.paid, 0)                    AS paid_amount,
       COALESCE(s.shipped, 0) - COALESCE(p.paid, 0)                AS debt,
       GREATEST(COALESCE(s.shipped, 0) - COALESCE(p.paid, 0), 0)   AS receivable,
       GREATEST(COALESCE(p.paid, 0) - COALESCE(s.shipped, 0), 0)   AS prepayment_balance,
       CASE WHEN c.amount = 0 THEN 0 ELSE ROUND(COALESCE(p.paid, 0) / c.amount, 4) END AS paid_pct
FROM dim_contract c
LEFT JOIN (SELECT contract_id, SUM(amount) AS shipped FROM fact_sales_line  GROUP BY 1) s USING (contract_id)
LEFT JOIN (SELECT contract_id, SUM(amount) AS paid    FROM fact_payment_in GROUP BY 1) p USING (contract_id);

-- График платежей: оплаты распределяются на этапы по FIFO (по дате этапа); просрочка на дату формирования
CREATE VIEW v_payment_schedule_status AS
WITH st AS (
    SELECT ps.*,
           SUM(ps.amount) OVER (PARTITION BY ps.contract_id ORDER BY ps.due_date, ps.stage_no) AS cum_plan,
           COALESCE(p.paid, 0) AS contract_paid
    FROM fact_payment_schedule ps
    LEFT JOIN (SELECT contract_id, SUM(amount) AS paid FROM fact_payment_in GROUP BY 1) p USING (contract_id)
), alloc AS (
    SELECT st.*, LEAST(amount, GREATEST(contract_paid - (cum_plan - amount), 0)) AS paid_amount FROM st
)
SELECT a.contract_id, a.stage_no, a.due_date, a.kind, a.percent,
       a.amount                AS plan_amount,
       a.paid_amount,
       a.amount - a.paid_amount AS unpaid_amount,
       CASE WHEN a.due_date < r.report_date THEN a.amount - a.paid_amount ELSE 0 END AS overdue_amount
FROM alloc a CROSS JOIN dim_report_date r;

-- Задолженность перед поставщиками
CREATE VIEW v_supplier_debt AS
SELECT s.supplier_id, s.name,
       COALESCE(pu.purchased, 0) AS purchased_amount,
       COALESCE(po.paid, 0)      AS paid_amount,
       COALESCE(pu.purchased, 0) - COALESCE(po.paid, 0) AS debt
FROM dim_supplier s
LEFT JOIN (SELECT supplier_id, SUM(amount) AS purchased FROM fact_purchase_line GROUP BY 1) pu USING (supplier_id)
LEFT JOIN (SELECT supplier_id, SUM(amount) AS paid      FROM fact_payment_out    GROUP BY 1) po USING (supplier_id);
