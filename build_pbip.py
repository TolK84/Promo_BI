#!/usr/bin/env python3
"""Собирает заготовку Power BI проекта Demo_Agro (PBIP: TMDL + PBIR) в указанной папке.
   python3 build_pbip.py <папка>
Таблицы — пустые заглушки с типизированными колонками; запросы к Postgres подключаются вручную."""
import hashlib
import json
import os
import re
import sys
import uuid

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
NAME = "Demo_Agro"
MODEL = os.path.join(OUT, f"{NAME}.SemanticModel")
REPORT = os.path.join(OUT, f"{NAME}.Report")
NS = uuid.UUID("5d1f7a52-0c0e-4f43-9e8a-2b9d1c7a6e11")


def guid(s):
    return str(uuid.uuid5(NS, s))


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def wjson(path, obj):
    write(path, json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def q(name):
    return name if re.fullmatch(r"\w+", name) else "'" + name.replace("'", "''") + "'"


# ======================= МОДЕЛЬ =======================
# колонка: (имя, тип, опции)  тип: int/text/num/date/bool; опции: hidden, fmt, key, sort
T2TMDL = {"int": "int64", "text": "string", "num": "double", "date": "dateTime", "bool": "boolean"}
T2M = {"int": "Int64.Type", "text": "text", "num": "number", "date": "date", "bool": "logical"}


def C(name, typ, **o):
    return (name, typ, o)


TABLES = [
    ("dim_date", "Дата (календарь). Источник: dim_date", [
        C("date_id", "date", key=True, fmt="dd.mm.yyyy"), C("year", "int", fmt="0", summ="none"), C("quarter", "int", fmt="0", summ="none"),
        C("month", "int", fmt="0", summ="none", hidden=True), C("month_name", "text", sort="month"),
        C("month_start", "date", fmt="mmm yyyy"), C("week", "int", fmt="0", summ="none", hidden=True),
        C("weekday", "int", fmt="0", summ="none", hidden=True)], {"dataCategory": "Time"}),
    ("dim_report_date", "Дата формирования (одна строка). Источник: dim_report_date", [
        C("report_date", "date", fmt="dd.mm.yyyy")], {}),
    ("dim_season", "Источник: dim_season; name → season_name", [
        C("season_id", "int", hidden=True, summ="none"), C("season_name", "text"), C("season_year", "int", hidden=True, summ="none")], {}),
    ("dim_division", "Источник: dim_division; name → division_name", [
        C("division_id", "int", hidden=True, summ="none"), C("division_name", "text")], {}),
    ("dim_manager", "Источник: dim_manager; name → manager_name", [
        C("manager_id", "int", hidden=True, summ="none"), C("manager_name", "text"), C("division_id", "int", hidden=True, summ="none")], {}),
    ("dim_customer", "Источник: dim_customer; name → customer_name", [
        C("customer_id", "int", hidden=True, summ="none"), C("customer_name", "text"), C("region", "text"),
        C("manager_id", "int", hidden=True, summ="none")], {}),
    ("dim_supplier", "Источник: dim_supplier; name → supplier_name", [
        C("supplier_id", "int", hidden=True, summ="none"), C("supplier_name", "text"), C("country", "text")], {}),
    ("dim_manufacturer", "Источник: dim_manufacturer; name → manufacturer_name", [
        C("manufacturer_id", "int", hidden=True, summ="none"), C("manufacturer_name", "text")], {}),
    ("dim_product_group", "Источник: dim_product_group; name → group_name", [
        C("group_id", "int", hidden=True, summ="none"), C("group_name", "text")], {}),
    ("dim_product", "Источник: dim_product; name → product_name", [
        C("product_id", "int", hidden=True, summ="none"), C("sku", "text"), C("product_name", "text"), C("pack", "text"),
        C("group_id", "int", hidden=True, summ="none"),
        C("manufacturer_id", "int", hidden=True, summ="none"), C("unit", "text")], {}),
    ("dim_warehouse", "Источник: dim_warehouse; name → warehouse_name", [
        C("warehouse_id", "int", hidden=True, summ="none"), C("warehouse_name", "text")], {}),
    ("dim_contract", "Источник: dim_contract; amount → contract_amount", [
        C("contract_id", "int", hidden=True, summ="none"), C("number", "text"), C("customer_id", "int", hidden=True, summ="none"),
        C("manager_id", "int", hidden=True, summ="none"), C("season_id", "int", hidden=True, summ="none"),
        C("contract_date", "date", fmt="dd.mm.yyyy"), C("contract_amount", "num", fmt="#,0", summ="sum"), C("sign_type", "text"),
        C("original_received", "bool"), C("status", "text")], {}),
    ("fact_order_line", "Источник: fact_order_line (shipped_qty, remaining_qty, ship_status — вычисляемые колонки DAX)", [
        C("order_line_id", "int", hidden=True, summ="none"), C("order_id", "int", hidden=True, summ="none"), C("order_date", "date", fmt="dd.mm.yyyy"),
        C("contract_id", "int", hidden=True, summ="none"), C("customer_id", "int", hidden=True, summ="none"),
        C("manager_id", "int", hidden=True, summ="none"), C("season_id", "int", hidden=True, summ="none"),
        C("product_id", "int", hidden=True, summ="none"), C("warehouse_id", "int", hidden=True, summ="none"),
        C("qty", "num", fmt="#,0", summ="sum"), C("price", "num", fmt="#,0", summ="none"), C("amount", "num", fmt="#,0", summ="sum"),
        C("shipped_qty", "num", fmt="#,0", summ="sum",
          calc="CALCULATE(SUM(fact_sales_line[qty]), FILTER(ALL(fact_sales_line), fact_sales_line[order_line_id] = fact_order_line[order_line_id]))"),
        C("remaining_qty", "num", fmt="#,0", summ="sum", calc="[qty] - [shipped_qty]"),
        C("ship_status", "text",
          calc='SWITCH(TRUE(), [shipped_qty] = 0, "Не отгружен", [shipped_qty] < [qty], "Частично отгружен", "Отгружен")')], {}),
    ("fact_sales_line", "Источник: fact_sales_line", [
        C("sale_line_id", "int", hidden=True, summ="none"), C("sale_id", "int", hidden=True, summ="none"), C("sale_date", "date", fmt="dd.mm.yyyy"),
        C("order_line_id", "int", hidden=True, summ="none"), C("order_id", "int", hidden=True, summ="none"),
        C("contract_id", "int", hidden=True, summ="none"), C("customer_id", "int", hidden=True, summ="none"),
        C("manager_id", "int", hidden=True, summ="none"), C("season_id", "int", hidden=True, summ="none"),
        C("product_id", "int", hidden=True, summ="none"), C("warehouse_id", "int", hidden=True, summ="none"),
        C("qty", "num", fmt="#,0", summ="sum"), C("amount", "num", fmt="#,0", summ="sum"), C("cost_amount", "num", fmt="#,0", summ="sum")], {}),
    ("fact_payment_schedule", "Источник: представление v_payment_schedule_status (FIFO-разнос оплат по этапам)", [
        C("contract_id", "int", hidden=True, summ="none"), C("stage_no", "int", fmt="0", summ="none"), C("due_date", "date", fmt="dd.mm.yyyy"),
        C("kind", "text"), C("percent", "num", fmt="0.0", summ="none"), C("plan_amount", "num", fmt="#,0", summ="sum"),
        C("paid_amount", "num", fmt="#,0", summ="sum"), C("unpaid_amount", "num", fmt="#,0", summ="sum"),
        C("overdue_amount", "num", fmt="#,0", summ="sum")], {}),
    ("fact_payment_in", "Источник: fact_payment_in", [
        C("payment_id", "int", hidden=True, summ="none"), C("payment_date", "date", fmt="dd.mm.yyyy"),
        C("customer_id", "int", hidden=True, summ="none"), C("contract_id", "int", hidden=True, summ="none"),
        C("amount", "num", fmt="#,0", summ="sum"), C("purpose", "text")], {}),
    ("fact_purchase_line", "Источник: fact_purchase_line", [
        C("purchase_line_id", "int", hidden=True, summ="none"), C("purchase_id", "int", hidden=True, summ="none"),
        C("purchase_date", "date", fmt="dd.mm.yyyy"), C("supplier_id", "int", hidden=True, summ="none"),
        C("product_id", "int", hidden=True, summ="none"), C("warehouse_id", "int", hidden=True, summ="none"),
        C("qty", "num", fmt="#,0", summ="sum"), C("amount", "num", fmt="#,0", summ="sum")], {}),
    ("fact_payment_out", "Источник: fact_payment_out", [
        C("payment_id", "int", hidden=True, summ="none"), C("payment_date", "date", fmt="dd.mm.yyyy"),
        C("supplier_id", "int", hidden=True, summ="none"), C("purchase_id", "int", hidden=True, summ="none"),
        C("amount", "num", fmt="#,0", summ="sum")], {}),
    ("fact_sales_plan", "Источник: fact_sales_plan", [
        C("plan_month", "date", fmt="mmm yyyy"), C("manager_id", "int", hidden=True, summ="none"),
        C("division_id", "int", hidden=True, summ="none"), C("product_group_id", "int", hidden=True, summ="none"),
        C("plan_amount", "num", fmt="#,0", summ="sum"), C("plan_qty", "num", fmt="#,0", summ="sum")], {}),
    ("fact_supplier_order_line", "Источник: fact_supplier_order_line (заказы поставщикам, входящий поток)", [
        C("supplier_order_line_id", "int", hidden=True, summ="none"), C("supplier_order_id", "int", hidden=True, summ="none"),
        C("number", "text"), C("order_date", "date", fmt="dd.mm.yyyy"), C("expected_date", "date", fmt="dd.mm.yyyy"),
        C("supplier_id", "int", hidden=True, summ="none"), C("product_id", "int", hidden=True, summ="none"),
        C("warehouse_id", "int", hidden=True, summ="none"), C("qty", "num", fmt="#,0", summ="sum"),
        C("price", "num", fmt="#,0", summ="none"), C("amount", "num", fmt="#,0", summ="sum"), C("status", "text")], {}),
    ("fact_supply_trace", "Источник: представление v_supply_trace (готовое распределение склада и входящих заказов по строкам заказов, не пересчитывать в DAX)", [
        C("order_line_id", "int", hidden=True, summ="none"), C("order_id", "int", hidden=True, summ="none"),
        C("order_date", "date", fmt="dd.mm.yyyy"), C("year", "int", hidden=True, summ="none"),
        C("contract_id", "int", hidden=True, summ="none"), C("contract_number", "text"),
        C("customer_id", "int", hidden=True, summ="none"), C("customer_name", "text"), C("region", "text"),
        C("manager_id", "int", hidden=True, summ="none"), C("manager_name", "text"), C("division_name", "text", hidden=True),
        C("season_id", "int", hidden=True, summ="none"), C("season_name", "text", hidden=True),
        C("product_id", "int", hidden=True, summ="none"), C("sku", "text"), C("product_name", "text"), C("product_group", "text"),
        C("manufacturer", "text"), C("unit", "text"), C("pack", "text"), C("product_label", "text"),
        C("supply_status", "text"), C("next_arrival", "date", fmt="dd.mm.yyyy"),
        C("contract_qty", "num", fmt="#,0", summ="sum"), C("shipped_qty", "num", fmt="#,0", summ="sum"),
        C("remaining_qty", "num", fmt="#,0", summ="sum"), C("from_stock_qty", "num", fmt="#,0", summ="sum"),
        C("from_incoming_qty", "num", fmt="#,0", summ="sum"), C("shortage_qty", "num", fmt="#,0", summ="sum"),
        C("remaining_amount", "num", fmt="#,0", summ="sum"), C("from_stock_amount", "num", fmt="#,0", summ="sum"),
        C("from_incoming_amount", "num", fmt="#,0", summ="sum"), C("shortage_amount", "num", fmt="#,0", summ="sum"),
        C("product_stock_qty", "num", fmt="#,0", summ="none", hidden=True), C("product_incoming_qty", "num", fmt="#,0", summ="none", hidden=True),
        C("product_outgoing_qty", "num", fmt="#,0", summ="none", hidden=True)], {}),
]



# источник в Postgres (схема public) и переименование колонок -> имена модели
SRC = {
    "dim_season": ("dim_season", {"name": "season_name", "year": "season_year"}),
    "dim_division": ("dim_division", {"name": "division_name"}),
    "dim_manager": ("dim_manager", {"name": "manager_name"}),
    "dim_customer": ("dim_customer", {"name": "customer_name"}),
    "dim_supplier": ("dim_supplier", {"name": "supplier_name"}),
    "dim_manufacturer": ("dim_manufacturer", {"name": "manufacturer_name"}),
    "dim_product_group": ("dim_product_group", {"name": "group_name"}),
    "dim_product": ("dim_product", {"name": "product_name"}),
    "dim_warehouse": ("dim_warehouse", {"name": "warehouse_name"}),
    "dim_contract": ("dim_contract", {"amount": "contract_amount"}),
    "fact_payment_schedule": ("v_payment_schedule_status", {}),
    "fact_supply_trace": ("v_supply_trace", {}),
}


# ---------- отображаемые имена полей (в модели и отчёте) ----------
# внутренние имена (ключи) остаются в коде; наружу уходят русские
RU_DEFAULT = {
    "date_id": "Дата", "year": "Год", "quarter": "Квартал", "month": "Месяц №", "month_name": "Месяц",
    "month_start": "Начало месяца", "week": "Неделя", "weekday": "День недели №", "report_date": "Дата отчёта",
    "season_id": "ID сезона", "season_name": "Сезон", "season_year": "Год сезона",
    "division_id": "ID подразделения", "division_name": "Подразделение",
    "manager_id": "ID менеджера", "manager_name": "Менеджер",
    "customer_id": "ID клиента", "customer_name": "Клиент", "region": "Регион",
    "supplier_id": "ID поставщика", "supplier_name": "Поставщик", "country": "Страна",
    "manufacturer_id": "ID производителя", "manufacturer_name": "Производитель",
    "group_id": "ID группы", "group_name": "Группа товаров", "product_group_id": "ID группы",
    "product_id": "ID товара", "sku": "Артикул", "product_name": "Товар", "pack": "Фасовка", "unit": "Ед. изм.",
    "warehouse_id": "ID склада", "warehouse_name": "Склад",
    "contract_id": "ID договора", "number": "Номер договора", "contract_date": "Дата договора",
    "contract_amount": "Сумма договора", "sign_type": "Тип подписания", "original_received": "Оригинал получен",
    "status": "Статус", "order_line_id": "ID строки заказа", "order_id": "ID заказа", "order_date": "Дата заказа",
    "qty": "Количество", "price": "Цена", "amount": "Сумма",
    "shipped_qty": "Кол-во отгружено", "remaining_qty": "Кол-во к отгрузке", "ship_status": "Статус отгрузки",
    "sale_line_id": "ID строки продажи", "sale_id": "ID продажи", "sale_date": "Дата продажи", "cost_amount": "Себестоимость",
    "stage_no": "№ этапа", "due_date": "Срок оплаты", "kind": "Вид платежа", "percent": "Доля, %",
    "plan_amount": "Плановая сумма", "paid_amount": "Оплачено", "unpaid_amount": "Не оплачено", "overdue_amount": "Просрочено",
    "payment_id": "ID платежа", "payment_date": "Дата платежа", "purpose": "Назначение платежа",
    "purchase_line_id": "ID строки закупки", "purchase_id": "ID закупки", "purchase_date": "Дата закупки",
    "plan_month": "Месяц плана", "plan_qty": "Плановое кол-во",
    "supplier_order_line_id": "ID строки заказа поставщику", "supplier_order_id": "ID заказа поставщику",
    "expected_date": "Ожидаемая дата поставки",
    "contract_number": "Номер договора", "product_group": "Группа товаров", "manufacturer": "Производитель",
    "product_label": "Товар (полное название)", "supply_status": "Статус обеспечения", "next_arrival": "Ближайшее поступление",
    "contract_qty": "Кол-во по договору", "from_stock_qty": "Кол-во со склада", "from_incoming_qty": "Кол-во из входящих",
    "shortage_qty": "Кол-во дефицита", "remaining_amount": "Сумма к отгрузке", "from_stock_amount": "Сумма со склада",
    "from_incoming_amount": "Сумма из входящих", "shortage_amount": "Сумма дефицита",
    "product_stock_qty": "Остаток товара на складе", "product_incoming_qty": "Входящий объём по товару",
    "product_outgoing_qty": "Исходящий объём по товару",
}
RU_OVERRIDE = {
    ("dim_contract", "status"): "Статус договора",
    ("fact_order_line", "number"): "Номер заказа",
    ("fact_supplier_order_line", "number"): "Номер заказа поставщику",
    ("fact_supplier_order_line", "status"): "Статус заказа поставщику",
    ("fact_payment_schedule", "percent"): "Доля этапа, %",
    ("fact_payment_out", "amount"): "Сумма оплаты",
    ("fact_payment_in", "amount"): "Сумма оплаты",
    ("fact_supply_trace", "order_date"): "Дата заказа",
}
_TBL_NAMES = {t[0] for t in TABLES}


def ru(table, col):
    if (table, col) in RU_OVERRIDE:
        return RU_OVERRIDE[(table, col)]
    if col not in RU_DEFAULT:
        raise KeyError(f"нет русского имени для {table}.{col}")
    return RU_DEFAULT[col]


_SELF = {}   # таблица -> {внутр.имя: русское}
for _t, _d, _cols, _p in TABLES:
    _SELF[_t] = {c[0]: ru(_t, c[0]) for c in _cols}
_all = {(t, c) for t, m in _SELF.items() for c in m}


def tr_dax(dax, own=None):
    """table[col] -> table[Русское]; при own — ещё и [col] в вычисляемых колонках своей таблицы"""
    dax = re.sub(r"\b(\w+)\[(\w+)\]", lambda m: f"{m.group(1)}[{_SELF[m.group(1)][m.group(2)]}]"
                 if m.group(1) in _SELF and m.group(2) in _SELF[m.group(1)] else m.group(0), dax)
    if own:
        dax = re.sub(r"(?<![\w\]])\[(\w+)\]", lambda m: f"[{_SELF[own][m.group(1)]}]" if m.group(1) in _SELF[own] else m.group(0), dax)
    return dax


def tr_ref(ref):   # 'table.col' -> 'table.Русское'
    t, c = ref.split(".", 1)
    return f"{t}.{_SELF[t][c]}" if t in _SELF and c in _SELF[t] else ref


def table_tmdl(name, desc, cols, props):
    L = [f"table {q(name)}"]
    for k, v in props.items():
        L.append(f"\t{k}: {v}")
    L.append(f"\tlineageTag: {guid('t:' + name)}")
    L.append("")
    for cn, typ, o in cols:
        L.append(f"\tcolumn {q(ru(name, cn))}" + (f" = {tr_dax(o['calc'], name)}" if o.get("calc") else ""))
        L.append(f"\t\tdataType: {T2TMDL[typ]}")
        if o.get("key"):
            L.append("\t\tisKey")
        if o.get("hidden"):
            L.append("\t\tisHidden")
        if o.get("fmt"):
            L.append(f"\t\tformatString: {o['fmt']}")
        L.append(f"\t\tlineageTag: {guid('c:' + name + '.' + cn)}")
        summ = o.get("summ", "sum" if typ == "num" else "none")
        L.append(f"\t\tsummarizeBy: {summ}")
        if not o.get("calc"):
            L.append(f"\t\tsourceColumn: {ru(name, cn)}")
        if o.get("sort"):
            L.append(f"\t\tsortByColumn: {q(ru(name, o['sort']))}")
        L.append("")
        L.append("\t\tannotation SummarizationSetBy = Automatic")
        L.append("")
    item, ren0 = SRC.get(name, (name, {}))
    back = {v: k for k, v in ren0.items()}                      # внутр.имя -> имя в БД
    ren = {back.get(c[0], c[0]): ru(name, c[0]) for c in cols if not c[2].get("calc")}
    steps = [f'                    Source = PostgreSQL.Database(DbServer, DbName),',
             f'                    Data = Source{{[Schema = "public", Item = "{item}"]}}[Data]']
    last = "Data"
    if ren:
        pairs = ", ".join('{"%s", "%s"}' % (k, v) for k, v in ren.items())
        steps[-1] += ","
        steps.append(f"                    Renamed = Table.RenameColumns(Data, {{{pairs}}})")
        last = "Renamed"
    L += [f"\tpartition {q(name)} = m", "\t\tmode: import", "\t\tsource =", "\t\t\t\tlet"] + [s.replace("                    ", "\t\t\t\t    ", 1) for s in steps]
    L += ["\t\t\t\tin", f"\t\t\t\t    {last}", ""]
    return "\n".join(L)


# связи: (таблица-факт.колонка, таблица-измерение.колонка)
RELS = [
    ("fact_sales_line.sale_date", "dim_date.date_id"), ("fact_sales_line.contract_id", "dim_contract.contract_id"),
    ("fact_sales_line.product_id", "dim_product.product_id"), ("fact_sales_line.warehouse_id", "dim_warehouse.warehouse_id"),
    ("fact_order_line.order_date", "dim_date.date_id"), ("fact_order_line.contract_id", "dim_contract.contract_id"),
    ("fact_order_line.product_id", "dim_product.product_id"), ("fact_order_line.warehouse_id", "dim_warehouse.warehouse_id"),
    ("fact_payment_schedule.due_date", "dim_date.date_id"), ("fact_payment_schedule.contract_id", "dim_contract.contract_id"),
    ("fact_payment_in.payment_date", "dim_date.date_id"), ("fact_payment_in.contract_id", "dim_contract.contract_id"),
    ("fact_purchase_line.purchase_date", "dim_date.date_id"), ("fact_purchase_line.supplier_id", "dim_supplier.supplier_id"),
    ("fact_purchase_line.product_id", "dim_product.product_id"), ("fact_purchase_line.warehouse_id", "dim_warehouse.warehouse_id"),
    ("fact_payment_out.payment_date", "dim_date.date_id"), ("fact_payment_out.supplier_id", "dim_supplier.supplier_id"),
    ("fact_sales_plan.plan_month", "dim_date.date_id"), ("fact_sales_plan.manager_id", "dim_manager.manager_id"),
    ("fact_sales_plan.product_group_id", "dim_product_group.group_id"),
    ("dim_contract.customer_id", "dim_customer.customer_id"), ("dim_contract.season_id", "dim_season.season_id"),
    ("fact_supplier_order_line.order_date", "dim_date.date_id"), ("fact_supplier_order_line.supplier_id", "dim_supplier.supplier_id"),
    ("fact_supplier_order_line.product_id", "dim_product.product_id"), ("fact_supplier_order_line.warehouse_id", "dim_warehouse.warehouse_id"),
    ("fact_supply_trace.contract_id", "dim_contract.contract_id"),
    ("dim_customer.manager_id", "dim_manager.manager_id"), ("dim_manager.division_id", "dim_division.division_id"),
    ("dim_product.group_id", "dim_product_group.group_id"), ("dim_product.manufacturer_id", "dim_manufacturer.manufacturer_id"),
]

# меры: (имя, DAX, формат, папка)
M_INT, M_PCT = "#,0", "0.0%"
CUM = ("VAR vAsOf = MIN(MAX(dim_date[date_id]), [Дата формирования])\nRETURN\nCALCULATE(SUM({col}), REMOVEFILTERS(dim_date), dim_date[date_id] <= vAsOf)")
MEASURES = [
    ("Выручка", "SUM(fact_sales_line[amount])", M_INT, "Продажи"),
    ("Себестоимость", "SUM(fact_sales_line[cost_amount])", M_INT, "Продажи"),
    ("Маржа", "[Выручка] - [Себестоимость]", M_INT, "Продажи"),
    ("Маржа %", "DIVIDE([Маржа], [Выручка])", M_PCT, "Продажи"),
    ("Отгружено, кол-во", "SUM(fact_sales_line[qty])", M_INT, "Продажи"),
    ("Заказано, сумма", "SUM(fact_order_line[amount])", M_INT, "Заказы"),
    ("Строк заказов", "COUNTROWS(fact_order_line)", M_INT, "Заказы"),
    ("Остаток к отгрузке, кол-во", "SUM(fact_order_line[remaining_qty])", M_INT, "Заказы"),
    ("Сумма договоров", "SUM(dim_contract[contract_amount])", M_INT, "Договоры"),
    ("Договоров", "DISTINCTCOUNT(dim_contract[contract_id])", "0", "Договоры"),
    ("Оплачено клиентами", "SUM(fact_payment_in[amount])", M_INT, "Оплаты"),
    ("Предоплаты", 'CALCULATE([Оплачено клиентами], fact_payment_in[purpose] = "Предоплата")', M_INT, "Оплаты"),
    ("План оплат", "SUM(fact_payment_schedule[plan_amount])", M_INT, "Оплаты"),
    ("Оплачено по графику", "SUM(fact_payment_schedule[paid_amount])", M_INT, "Оплаты"),
    ("Не оплачено по графику", "SUM(fact_payment_schedule[unpaid_amount])", M_INT, "Оплаты"),
    ("Просроченная задолженность", "SUM(fact_payment_schedule[overdue_amount])", M_INT, "Оплаты"),
    ("Выполнение графика %", "DIVIDE([Оплачено по графику], [План оплат])", M_PCT, "Оплаты"),
    ("Отгружено нарастающим", CUM.format(col="fact_sales_line[amount]"), M_INT, "Дебиторка"),
    ("Оплачено нарастающим", CUM.format(col="fact_payment_in[amount]"), M_INT, "Дебиторка"),
    ("Сальдо расчётов", "[Отгружено нарастающим] - [Оплачено нарастающим]", M_INT, "Дебиторка"),
    ("Дебиторская задолженность", "SUMX(VALUES(dim_contract[contract_id]), MAX(0, [Сальдо расчётов]))", M_INT, "Дебиторка"),
    ("Остаток предоплаты", "SUMX(VALUES(dim_contract[contract_id]), MAX(0, -[Сальдо расчётов]))", M_INT, "Дебиторка"),
    ("Закуплено, сумма", "SUM(fact_purchase_line[amount])", M_INT, "Закупки"),
    ("Закуплено, кол-во", "SUM(fact_purchase_line[qty])", M_INT, "Закупки"),
    ("Оплачено поставщикам", "SUM(fact_payment_out[amount])", M_INT, "Закупки"),
    ("Закуплено нарастающим", CUM.format(col="fact_purchase_line[amount]").replace("dim_date[date_id] <= vAsOf", "dim_date[date_id] <= vAsOf"), M_INT, "Закупки"),
    ("Оплачено поставщикам нарастающим", CUM.format(col="fact_payment_out[amount]"), M_INT, "Закупки"),
    ("Долг перед поставщиками", "[Закуплено нарастающим] - [Оплачено поставщикам нарастающим]", M_INT, "Закупки"),
    ("План продаж", "SUM(fact_sales_plan[plan_amount])", M_INT, "План"),
    ("План, кол-во", "SUM(fact_sales_plan[plan_qty])", M_INT, "План"),
    ("Отклонение от плана", "[Выручка] - [План продаж]", M_INT, "План"),
    ("Выполнение плана %", "DIVIDE([Выручка], [План продаж])", M_PCT, "План"),
    ("Заказано у поставщиков, сумма", "SUM(fact_supplier_order_line[amount])", M_INT, "Закупки"),
    ("К реализации", "SUM(fact_supply_trace[remaining_amount])", M_INT, "Обеспечение"),
    ("Ждёт поставки от поставщика", "SUM(fact_supply_trace[from_incoming_amount])", M_INT, "Обеспечение"),
    ("Дефицит: не обеспечено даже заказанным", "SUM(fact_supply_trace[shortage_amount])", M_INT, "Обеспечение"),
    ("По договору", "SUM(fact_supply_trace[contract_qty])", M_INT, "Обеспечение"),
    ("Отгружено", "SUM(fact_supply_trace[shipped_qty])", M_INT, "Обеспечение"),
    ("В заказе исходящем (к реализации)", "SUM(fact_supply_trace[remaining_qty])", M_INT, "Обеспечение"),
    ("На складе", "SUM(fact_supply_trace[from_stock_qty])", M_INT, "Обеспечение"),
    ("В заказе входящем", "SUM(fact_supply_trace[from_incoming_qty])", M_INT, "Обеспечение"),
    ("Не хватает", "SUM(fact_supply_trace[shortage_qty])", M_INT, "Обеспечение"),
    ("Цвет строки (обеспечение)", 'SWITCH(TRUE(), SUM(fact_supply_trace[shortage_qty]) > 0, "#F4A6A6", SUM(fact_supply_trace[from_incoming_qty]) > 0, "#FFE27A", BLANK())', "", "Служебные", True),
    ("Дата формирования", "MAX(dim_report_date[report_date])", "dd.mm.yyyy", "Служебные"),
]


def measures_tmdl():
    L = ["table _Measures", "\texcludeFromModelRefresh", f"\tlineageTag: {guid('t:_Measures')}", ""]
    for m in MEASURES:
        name, dax, fmt, folder = m[:4]
        hidden = len(m) > 4 and m[4]
        if "\n" in dax:
            L.append(f"\tmeasure {q(name)} = ```")
            L += ["\t\t\t" + x for x in tr_dax(dax).split("\n")]
            L.append("\t\t\t```")
        else:
            L.append(f"\tmeasure {q(name)} = {tr_dax(dax)}")
        if fmt:
            L.append(f"\t\tformatString: {fmt}")
        if hidden:
            L.append("\t\tisHidden")
        L.append(f"\t\tdisplayFolder: {folder}")
        L.append(f"\t\tlineageTag: {guid('m:' + name)}")
        L.append("")
    L += ["\tpartition _Measures = m", "\t\tmode: import", "\t\tsource =", "\t\t\t\tlet",
          '\t\t\t\t    Source = #table(type table [Column1 = text], {}),',
          '\t\t\t\t    #"Removed Columns" = Table.RemoveColumns(Source, {"Column1"})', "\t\t\t\tin", '\t\t\t\t    #"Removed Columns"', ""]
    return "\n".join(L)


def build_model():
    wjson(os.path.join(MODEL, "definition.pbism"), {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
        "version": "4.2", "settings": {}})
    d = os.path.join(MODEL, "definition")
    write(os.path.join(d, "database.tmdl"), "database\n\tcompatibilityLevel: 1606\n")
    expr = []
    for pn, pv in (("DbServer", "localhost:15432"), ("DbName", "demo_agro")):
        expr += [f'expression {pn} = "{pv}" meta [IsParameterQuery = true, Type = "Text", IsParameterQueryRequired = true]',
                 f"\tlineageTag: {guid('e:' + pn)}", "", "\tannotation PBI_ResultType = Text", ""]
    write(os.path.join(d, "expressions.tmdl"), "\n".join(expr))
    names = [t[0] for t in TABLES] + ["_Measures"]
    model = ["model Model", "\tculture: en-US", "\tdefaultPowerBIDataSourceVersion: powerBI_V3", "\tsourceQueryCulture: ru-RU",
             "\tdataAccessOptions", "\t\tlegacyRedirects", "\t\treturnErrorValuesAsNull", "",
             "annotation __PBI_TimeIntelligenceEnabled = 0", "",
             "annotation PBI_QueryOrder = " + json.dumps(names, ensure_ascii=False), ""]
    model += [f"ref table {q(n)}" for n in names] + ["", "ref expression DbServer", "ref expression DbName"]
    write(os.path.join(d, "model.tmdl"), "\n".join(model) + "\n")
    rel = []
    for f, t in RELS:
        rel += [f"relationship {guid('r:' + f + '>' + t)}", f"\tfromColumn: {q(f.split('.')[0])}.{q(_SELF[f.split('.')[0]][f.split('.')[1]])}",
                f"\ttoColumn: {q(t.split('.')[0])}.{q(_SELF[t.split('.')[0]][t.split('.')[1]])}", ""]
    write(os.path.join(d, "relationships.tmdl"), "\n".join(rel))
    for name, desc, cols, props in TABLES:
        write(os.path.join(d, "tables", f"{name}.tmdl"), table_tmdl(name, desc, cols, props))
    write(os.path.join(d, "tables", "_Measures.tmdl"), measures_tmdl())
    keep = {f"{n}.tmdl" for n, *_ in TABLES} | {"_Measures.tmdl"}
    td = os.path.join(d, "tables")
    for fn in os.listdir(td):          # хвосты автодат Desktop и старых таблиц убираем в _stale
        if fn not in keep:
            os.makedirs(os.path.join(td, "..", "..", "..", "_trash", "stale"), exist_ok=True)
            os.replace(os.path.join(td, fn), os.path.join(td, "..", "..", "..", "_trash", "stale", fn))


# ======================= ОТЧЁТ =======================
# Оформление по мотивам отчёта-образца: серый холст + светлый скруглённый «лист», Arial, салатовые заголовки,
# колонка срезов справа (220 px), поля 19 px, скругление 20 у таблиц и графиков.
SCH = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition"
FONT = "Arial"
LIME, GREEN = "#00A3FF", "#2F7BFF"   # акцент (неон-синий) и цвет столбцов
THEME_FILE = "Demo_Agro_Theme.json"
THEME_FALLBACK = {
    "name": "Demo_Agro_Theme",
    "dataColors": ["#2F7BFF", "#00A3FF", "#2D386D", "#7B61FF", "#00C2A8", "#00A3FF", "#FFB020", "#E56E1D", "#5C97D2", "#9AA5B1",
                   "#14B8A6", "#475569"],
    "foreground": "#111111", "background": "#F3F3F3", "tableAccent": "#2F7BFF", "good": "#27A481", "bad": "#E56E1D",
    "neutral": "#2464B1", "maximum": "#00A3FF", "center": "#7B61FF", "minimum": "#2D386D",
    "textClasses": {k: {"fontFace": "Arial"} for k in ("label", "callout", "title", "header")}}


def hid(*parts):
    return hashlib.md5("|".join(parts).encode()).hexdigest()[:20]


def lit(v):
    return {"expr": {"Literal": {"Value": v}}}


def S(v):
    return lit("'" + v + "'")


def Dn(n):
    return lit(f"{n}D")


def Ln(n):
    return lit(f"{n}L")


def B(b):
    return lit("true" if b else "false")


def tc(i, p=0):
    return {"solid": {"color": {"expr": {"ThemeDataColor": {"ColorId": i, "Percent": p}}}}}


def hexc(h):
    return {"solid": {"color": {"expr": {"Literal": {"Value": f"'{h}'"}}}}}


def op(props, sel=None):
    d = {"properties": props}
    if sel is not None:
        d["selector"] = sel
    return d


DEF = {"id": "default"}


def f_col(entity, prop):
    prop = _SELF[entity][prop]
    return {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}


def f_msr(prop):
    return {"Measure": {"Expression": {"SourceRef": {"Entity": "_Measures"}}, "Property": prop}}


def P(spec):
    """'dim_date.year' -> колонка; '#Выручка' -> мера"""
    if spec.startswith("#"):
        n = spec[1:]
        return {"field": f_msr(n), "queryRef": f"_Measures.{n}", "nativeQueryRef": n, "active": True}
    e, p = spec.split(".", 1)
    rp = _SELF[e][p]
    return {"field": f_col(e, p), "queryRef": f"{e}.{rp}", "nativeQueryRef": rp, "active": True}


def container(title=None, tsize=10, talign="left", tbg=None, tcolor=None, radius=20, border=True, bg=True, bold=True):
    c = {}
    if title:
        tp = {"show": B(True), "text": S(title), "alignment": S(talign), "fontSize": Dn(tsize), "fontFamily": S(FONT),
              "bold": B(bold), "fontColor": tcolor or tc(1, 0), "titleWrap": B(True)}
        if tbg:
            tp["background"] = tbg
        c["title"] = [op(tp)]
    else:
        c["title"] = [op({"show": B(False)})]
    c["background"] = [op({"show": B(bg), "transparency": Dn(0), **({"color": tc(0, 0)} if bg else {})})]
    c["border"] = [op({"show": B(border), "color": tc(0, -0.2), "radius": Dn(radius), "width": Dn(1)})]
    c["dropShadow"] = [op({"show": B(False)})]
    return c


class Page:
    def __init__(self, name):
        self.name, self.id, self.visuals, self.z = name, hid("page", name), [], 0

    def add(self, key, vtype, x, y, w, h, roles=None, objects=None, cont=None, sort=None, sync=None, filters=None):
        v = {"$schema": f"{SCH}/visualContainer/2.7.0/schema.json", "name": hid(self.name, key),
             "position": {"x": x, "y": y, "z": self.z * 1000, "height": h, "width": w, "tabOrder": self.z * 1000}}
        self.z += 1
        vis = {"visualType": vtype}
        if roles:
            qs = {r: {"projections": [P(s) for s in specs]} for r, specs in roles.items()}
            query = {"queryState": qs}
            if sort:
                fld = f_msr(sort[1:]) if sort.startswith("#") else f_col(*sort.split(".", 1))
                query["sortDefinition"] = {"sort": [{"field": fld, "direction": "Descending"}], "isDefaultSort": True}
            vis["query"] = query
        if objects:
            vis["objects"] = objects
        if cont:
            vis["visualContainerObjects"] = cont
        if sync:
            vis["syncGroup"] = {"groupName": sync, "fieldChanges": True, "filterChanges": True}
        vis["drillFilterOtherVisuals"] = True
        v["visual"] = vis
        if filters:
            v["filterConfig"] = filters
        self.visuals.append(v)


def chrome(p, title, clear_btn=True):
    """Подложка-лист, заголовок страницы, кнопка сброса срезов."""
    p.add("sheet", "shape", 0, 0, 1280, 720,
          objects={"shape": [op({"tileShape": S("rectangle"), "roundEdge": Ln(30)})], "rotation": [op({"shapeAngle": Ln(0)})],
                   "shadow": [op({"show": B(False)})], "fill": [op({"fillColor": tc(0, 0)}, DEF)],
                   "outline": [op({"show": B(True)}), op({"lineColor": tc(0, -0.5)}, DEF)]},
          cont={"background": [op({"show": B(False), "transparency": Dn(0)})], "general": [op({"keepLayerOrder": B(True)})],
                "border": [op({"width": Dn(1)})], "visualHeader": [op({"show": B(False)})]})
    p.add("title", "textbox", 437, 17, 401, 48,
          objects={"general": [op({"paragraphs": [{"textRuns": [{"value": title, "textStyle": {
              "fontWeight": "bold", "fontFamily": FONT, "fontSize": "14pt", "color": LIME.lower()}}], "horizontalTextAlignment": "center"}]})]},
          cont={"background": [op({"show": B(False)})]})
    if clear_btn:
        p.add("clear", "actionButton", 1141, 14, 124, 40,
              objects={"icon": [op({"shapeType": S("clearAllSlicers"), "lineColor": tc(1, 0), "lineWeight": Ln(1)}, DEF)],
                       "text": [op({"show": B(True)}), op({"text": S("Сбросить срезы"), "horizontalAlignment": S("center"),
                                                         "fontFamily": S(FONT), "fontSize": Dn(8)}, DEF)],
                       "outline": [op({"show": B(False)})]})


def years_filter():
    """Фильтр уровня визуала: только годы данных 2024-2026."""
    return {"filters": [{
        "name": hid("flt", "year"), "type": "Categorical", "howCreated": "User",
        "field": f_col("dim_date", "year"),
        "filter": {"Version": 2, "From": [{"Name": "d", "Entity": "dim_date", "Type": 0}],
                   "Where": [{"Condition": {"In": {
                       "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": _SELF["dim_date"]["year"]}}],
                       "Values": [[{"Literal": {"Value": f"{y}L"}}] for y in (2024, 2025, 2026)]}}}]}}]}


def slicer(p, key, y, h, field, title, mode, sync):
    p.add(key, "slicer", 1045, y, 220, h, roles={"Values": [field]}, sync=sync,
          filters=years_filter() if field == "dim_date.year" else None,
          objects={"data": [op({"mode": S(mode)})], "general": [op({"orientation": Dn(0)})], "header": [op({"show": B(False)})],
                   "items": [op({"fontFamily": S(FONT), "textSize": Dn(8)})], "selection": [op({"singleSelect": B(False)})]},
          cont={"title": [op({"show": B(True), "alignment": S("right"), "text": S(title), "background": hexc(LIME), "fontColor": tc(0, 0),
                              "fontSize": Dn(10), "fontFamily": S(FONT), "titleWrap": B(True)})],
                "background": [op({"show": B(True), "transparency": Dn(0)})],
                "border": [op({"show": B(True), "color": tc(0, -0.2), "radius": Dn(10), "width": Dn(1)})],
                "padding": [op({"bottom": Dn(0)})]})


def slicer_column(p, with_all=True):
    if with_all:
        slicer(p, "s_year", 70, 62, "dim_date.year", "Год", "Dropdown", "Год")
        slicer(p, "s_season", 140, 62, "dim_season.season_name", "Сезон", "Dropdown", "Сезон")
        slicer(p, "s_mgr", 210, 250, "dim_manager.manager_name", "Менеджер", "Basic", "Менеджер")
        slicer(p, "s_region", 470, 227, "dim_customer.region", "Регион", "Basic", "Регион")
    else:
        slicer(p, "s_year", 70, 62, "dim_date.year", "Год", "Dropdown", "Год поставщики")


def kpi(p, key, x, y, w, h, measures, money, stacked=False):
    """Карточки (cardVisual, стиль Cards): серая заливка, скругление 10, значение салатовым."""
    layout = [op({"orientation": Dn(1), "rowCount": Ln(len(measures))} if stacked else {"columnCount": Ln(len(measures)), "style": S("Cards")}),
              op({"rectangleRoundedCurve": Ln(10)}, DEF)]
    value = [op({"horizontalAlignment": S("center"), "fontSize": Dn(14), "bold": B(True), "fontFamily": S(FONT), "fontColor": hexc(LIME)}, DEF)]
    for m in measures:
        if m in money:
            value.append(op({"labelDisplayUnits": Dn(1000000), "labelPrecision": Ln(1)}, {"metadata": f"_Measures.{m}"}))
    p.add(key, "cardVisual", x, y, w, h, roles={"Data": ["#" + m for m in measures]},
          objects={"layout": layout, "value": value,
                   "label": [op({"fontFamily": S(FONT), "fontSize": Dn(9)}, DEF)],
                   "border": [op({"show": B(False)}, DEF)], "shapeCustomRectangle": [op({"rectangleRoundedCurve": Ln(10)}, DEF)],
                   "fillCustom": [op({"fillColor": tc(0, -0.1)}, DEF)]},
          cont={"background": [op({"show": B(False), "transparency": Dn(0)})],
                "padding": [op({"top": Dn(0), "bottom": Dn(0), "left": Dn(0), "right": Dn(0)})],
                "title": [op({"show": B(False)})], "border": [op({"width": Dn(1)})]})


def table(p, key, x, y, w, h, cols, title, sort=None):
    p.add(key, "tableEx", x, y, w, h, roles={"Values": cols}, sort=sort,
          objects={"columnHeaders": [op({"fontFamily": S(FONT), "fontSize": Dn(9), "bold": B(True), "fontColor": tc(1, 0),
                                         "backColor": tc(0, -0.1), "alignment": S("Center")})],
                   "values": [op({"fontFamily": S(FONT), "fontSize": Dn(9), "backColorPrimary": tc(0, 0), "backColorSecondary": tc(0, -0.05)})],
                   "grid": [op({"gridVertical": B(True), "gridHorizontal": B(True), "gridVerticalColor": tc(0, -0.2),
                                "gridHorizontalColor": tc(0, -0.2)})]},
          cont=container(title, tsize=10))


def columns(p, key, x, y, w, h, cat, val, title):
    p.add(key, "clusteredColumnChart", x, y, w, h, roles={"Category": [cat], "Y": ["#" + val]},
          objects={"legend": [op({"show": B(False)})], "zoom": [op({"show": B(False)})],
                   "categoryAxis": [op({"show": B(True), "fontFamily": S(FONT), "fontSize": Dn(8), "bold": B(False), "labelColor": tc(1, 0.4),
                                        "showAxisTitle": B(False), "concatenateLabels": B(True)})],
                   "valueAxis": [op({"show": B(False), "showAxisTitle": B(False)})],
                   "dataPoint": [op({"fill": hexc(GREEN)})],
                   "labels": [op({"show": B(True), "fontFamily": S(FONT), "fontSize": Dn(8), "bold": B(True), "labelDisplayUnits": Dn(1000000),
                                  "labelPrecision": Ln(0)})]},
          cont=container(title))


def donut(p, key, x, y, w, h, cat, val, title, money=True):
    lab = {"fontFamily": S(FONT), "fontSize": Dn(8), "labelStyle": S("Category, percent of total"), "percentageLabelPrecision": Ln(0)}
    p.add(key, "donutChart", x, y, w, h, roles={"Category": [cat], "Y": ["#" + val]},
          objects={"legend": [op({"show": B(False)})], "labels": [op(lab)], "slices": [op({"innerRadiusRatio": Ln(65)})]},
          cont=container(title, radius=22))


def year_tiles(p):
    """Плиточный срез «Год» (2024/2025/2026): одиночный выбор, действует только на свою страницу."""
    p.add("s_year_tiles", "slicer", 19, 70, 1009, 40, roles={"Values": ["dim_date.year"]}, filters=years_filter(),
          objects={"data": [op({"mode": S("Basic")})], "general": [op({"orientation": Dn(1)})], "header": [op({"show": B(False)})],
                   "items": [op({"fontFamily": S(FONT), "textSize": Dn(10), "bold": B(True)})],
                   "selection": [op({"singleSelect": B(True), "selectAllCheckboxEnabled": B(False)})]},
          cont={"title": [op({"show": B(False)})], "background": [op({"show": B(True), "transparency": Dn(0)})],
                "border": [op({"show": B(True), "color": tc(0, -0.2), "radius": Dn(10), "width": Dn(1)})]})


def text(p, key, x, y, w, h, value, size=9, color="#555555", bold=False, align="left"):
    style = {"fontFamily": FONT, "fontSize": f"{size}pt", "color": color}
    if bold:
        style["fontWeight"] = "bold"
    p.add(key, "textbox", x, y, w, h,
          objects={"general": [op({"paragraphs": [{"textRuns": [{"value": value, "textStyle": style}], "horizontalTextAlignment": align}]})]},
          cont={"background": [op({"show": B(False)})]})


def swatch(p, key, x, y, color):
    p.add(key, "shape", x, y, 16, 16,
          objects={"shape": [op({"tileShape": S("rectangle"), "roundEdge": Ln(4)})], "rotation": [op({"shapeAngle": Ln(0)})],
                   "fill": [op({"fillColor": hexc(color)}, DEF)], "outline": [op({"show": B(False)})], "shadow": [op({"show": B(False)})]},
          cont={"background": [op({"show": B(False)})], "visualHeader": [op({"show": B(False)})]})


def matrix(p, key, x, y, w, h, rows, vals, title, color_measure):
    """Матрица с иерархией строк, подытогами сверху и подсветкой строк мерой-цветом."""
    fill = {"solid": {"color": {"expr": {"Measure": {"Expression": {"SourceRef": {"Entity": "_Measures"}}, "Property": color_measure}}}}}
    values = [op({"fontFamily": S(FONT), "fontSize": Dn(9), "fontColorPrimary": tc(1, 0)})]
    values += [op({"backColor": fill}, {"metadata": f"_Measures.{m}"}) for m in vals]
    p.add(key, "pivotTable", x, y, w, h, roles={"Rows": rows, "Values": ["#" + m for m in vals]},
          objects={"columnHeaders": [op({"fontFamily": S(FONT), "fontSize": Dn(9), "bold": B(True), "fontColor": tc(1, 0),
                                         "backColor": tc(0, -0.1), "alignment": S("Center")})],
                   "rowHeaders": [op({"fontFamily": S(FONT), "fontSize": Dn(9), "fontColor": tc(1, 0)})],
                   "values": values,
                   "subTotals": [op({"rowSubtotals": B(True), "rowSubtotalsPosition": S("Top"), "columnSubtotals": B(False)})],
                   "grid": [op({"gridVertical": B(True), "gridHorizontal": B(True), "gridVerticalColor": tc(0, -0.2),
                                "gridHorizontalColor": tc(0, -0.2)})]},
          cont=container(title))


PAGES = []

p = Page("Продажи"); PAGES.append(p)
chrome(p, "Продажи")
slicer_column(p)
year_tiles(p)
kpi(p, "k", 19, 118, 1009, 70, ["Выручка", "Маржа", "Маржа %"], {"Выручка", "Маржа"})
columns(p, "c1", 19, 198, 640, 230, "dim_date.month_start", "Выручка", "Выручка по месяцам, млн")
donut(p, "d1", 671, 198, 357, 230, "dim_product_group.group_name", "Выручка", "Выручка по группам товаров")
table(p, "t1", 19, 438, 1009, 259, ["dim_manager.manager_name", "dim_division.division_name", "#Выручка", "#Маржа", "#Маржа %"],
      "Менеджеры: выручка и маржа", sort="#Выручка")

p = Page("Дебиторка"); PAGES.append(p)
chrome(p, "Дебиторка")
slicer_column(p)
year_tiles(p)
kpi(p, "k", 19, 118, 1009, 70, ["Дебиторская задолженность", "Просроченная задолженность"],
    {"Дебиторская задолженность", "Просроченная задолженность"})
table(p, "t1", 19, 198, 500, 499, ["dim_customer.customer_name", "dim_customer.region", "#Дебиторская задолженность"],
      "Топ клиентов по дебиторке (Первые N = 10 по мере)", sort="#Дебиторская задолженность")
table(p, "t2", 531, 198, 497, 499,
      ["dim_date.year", "fact_payment_schedule.kind", "#План оплат", "#Оплачено по графику", "#Не оплачено по графику", "#Просроченная задолженность"],
      "График платежей: план и факт")

p = Page("Логистика"); PAGES.append(p)
chrome(p, "Логистика")
slicer_column(p)
year_tiles(p)
donut(p, "d1", 19, 118, 420, 300, "fact_order_line.ship_status", "Строк заказов", "Статус отгрузки заказов")
kpi(p, "k", 19, 428, 420, 269, ["Строк заказов", "Заказано, сумма", "Остаток к отгрузке, кол-во"], {"Заказано, сумма"}, stacked=True)
table(p, "t1", 451, 118, 577, 579,
      ["dim_warehouse.warehouse_name", "fact_order_line.ship_status", "#Строк заказов", "#Заказано, сумма", "#Остаток к отгрузке, кол-во"],
      "Отгрузка по складам")

p = Page("Обеспечение"); PAGES.append(p)
chrome(p, "Обеспечение")
slicer(p, "s_mgr", 70, 300, "dim_manager.manager_name", "Менеджер", "Basic", "Менеджер")
slicer(p, "s_region", 380, 317, "dim_customer.region", "Регион", "Basic", "Регион")
kpi(p, "k", 19, 70, 1009, 80, ["К реализации", "Ждёт поставки от поставщика", "Дефицит: не обеспечено даже заказанным"],
    {"К реализации", "Ждёт поставки от поставщика", "Дефицит: не обеспечено даже заказанным"})
swatch(p, "lg1", 19, 162, "#FFE27A")
text(p, "lg1t", 40, 158, 400, 24, "на складе не хватает, но недостающее заказано у поставщика")
swatch(p, "lg2", 450, 162, "#F4A6A6")
text(p, "lg2t", 471, 158, 400, 24, "не хватает даже с учётом заказанного")
text(p, "note", 19, 186, 1009, 24, "Склад и входящие заказы распределяются между договорами по очереди заказов клиентов. "
     "Учитываются заказы текущего сезона.", size=8)
matrix(p, "m1", 19, 214, 1009, 483,
       ["fact_supply_trace.manager_name", "fact_supply_trace.customer_name", "fact_supply_trace.contract_number", "fact_supply_trace.product_label"],
       ["По договору", "Отгружено", "В заказе исходящем (к реализации)", "На складе", "В заказе входящем", "Не хватает"],
       "Прослеживаемость", "Цвет строки (обеспечение)")

p = Page("Поставщики"); PAGES.append(p)
chrome(p, "Поставщики")
slicer_column(p, with_all=False)
kpi(p, "k", 19, 70, 1009, 80, ["Закуплено, сумма", "Оплачено поставщикам", "Долг перед поставщиками"],
    {"Закуплено, сумма", "Оплачено поставщикам", "Долг перед поставщиками"})
table(p, "t1", 19, 160, 620, 537, ["dim_supplier.supplier_name", "#Закуплено, сумма", "#Оплачено поставщикам", "#Долг перед поставщиками"],
      "Задолженность перед поставщиками", sort="#Долг перед поставщиками")
donut(p, "d1", 651, 160, 377, 537, "dim_supplier.supplier_name", "Долг перед поставщиками", "Доля долга по поставщикам")


def load_theme():
    return THEME_FALLBACK


def build_report():
    wjson(os.path.join(OUT, f"{NAME}.pbip"), {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json", "version": "1.0",
        "artifacts": [{"report": {"path": f"{NAME}.Report"}}], "settings": {"enableAutoRecovery": True}})
    wjson(os.path.join(REPORT, "definition.pbir"), {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
        "version": "4.0", "datasetReference": {"byPath": {"path": f"../{NAME}.SemanticModel"}}})
    wjson(os.path.join(REPORT, "StaticResources", "RegisteredResources", THEME_FILE), load_theme())
    d = os.path.join(REPORT, "definition")
    wjson(os.path.join(d, "version.json"), {"$schema": f"{SCH}/versionMetadata/1.0.0/schema.json", "version": "2.0.0"})
    wjson(os.path.join(d, "report.json"), {
        "$schema": f"{SCH}/report/3.3.0/schema.json",
        "themeCollection": {
            "baseTheme": {"name": "CY26SU02", "reportVersionAtImport": {"visual": "2.6.0", "report": "3.1.0", "page": "2.3.0"}, "type": "SharedResources"},
            "customTheme": {"name": THEME_FILE, "reportVersionAtImport": {"visual": "2.7.0", "report": "3.2.0", "page": "2.3.1"},
                            "type": "RegisteredResources"}},
        "objects": {"section": [op({"verticalAlignment": S("Top")})], "outspacePane": [op({"expanded": B(False), "visible": B(False)})]},
        "resourcePackages": [
            {"name": "SharedResources", "type": "SharedResources", "items": [{"name": "CY26SU02", "path": "BaseThemes/CY26SU02.json", "type": "BaseTheme"}]},
            {"name": "RegisteredResources", "type": "RegisteredResources", "items": [{"name": THEME_FILE, "path": THEME_FILE, "type": "CustomTheme"}]}],
        "settings": {"useStylableVisualContainerHeader": True, "exportDataMode": "AllowSummarized", "defaultDrillFilterOtherVisuals": True,
                     "allowChangeFilterTypes": True, "useEnhancedTooltips": True, "useDefaultAggregateDisplayName": True}})
    wjson(os.path.join(d, "pages", "pages.json"), {
        "$schema": f"{SCH}/pagesMetadata/1.1.0/schema.json", "pageOrder": [x.id for x in PAGES], "activePageName": PAGES[0].id})
    for pg in PAGES:
        wjson(os.path.join(d, "pages", pg.id, "page.json"), {
            "$schema": f"{SCH}/page/2.1.0/schema.json", "name": pg.id, "displayName": pg.name, "displayOption": "FitToPage",
            "height": 720, "width": 1280,
            "objects": {"background": [op({"transparency": Dn(100), "color": tc(0, -0.2)})],
                        "outspace": [op({"transparency": Dn(0), "color": tc(0, -0.2)})]}})
        for v in pg.visuals:
            wjson(os.path.join(d, "pages", pg.id, "visuals", v["name"], "visual.json"), v)


build_model()
build_report()
print("ok:", OUT, len(TABLES) + 1, "tables,", len(RELS), "relationships,", len(MEASURES), "measures,", len(PAGES), "pages")
