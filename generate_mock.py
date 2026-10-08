#!/usr/bin/env python3
"""Генератор мок-данных demo_agro (только stdlib). Вывод — SQL с COPY-блоками.
   python3 generate_mock.py > data.sql
   docker exec -i superset_db psql -U demo_user -d demo_agro < data.sql
Все названия вымышлены. Данные детерминированы (seed)."""
import random
import sys
import datetime as dt
from collections import defaultdict

random.seed(20261007)
D = dt.timedelta
START, END, CAL_END = dt.date(2024, 1, 1), dt.date(2026, 9, 30), dt.date(2027, 3, 31)
INFL = {2024: 1.0, 2025: 1.07, 2026: 1.14}

out = []


def emit(table, cols, rows):
    out.append(f"COPY {table} ({', '.join(cols)}) FROM stdin;")
    for r in rows:
        out.append("\t".join("\\N" if v is None else ("t" if v is True else "f" if v is False else str(v)) for v in r))
    out.append("\\.")
    out.append("")


# ---------------- справочники ----------------
MONTHS_RU = ["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]
seasons = [(1, "Сезон 2024", 2024), (2, "Сезон 2025", 2025), (3, "Сезон 2026", 2026)]
divisions = [(1, "Отдел Север"), (2, "Отдел Юг"), (3, "Отдел Центр")]
first = ["Азамат", "Дмитрий", "Айгерим", "Сергей", "Марат", "Елена", "Алексей", "Нурлан", "Ольга"]
last = ["Ахметов", "Иванов", "Сарсенова", "Петров", "Байжанов", "Смирнова", "Козлов", "Тулеубаев", "Васильева"]
managers = [(i + 1, f"{last[i]} {first[i]}", i % 3 + 1) for i in range(9)]
mgr_div = {m[0]: m[2] for m in managers}

forms = ["ТОО", "КХ", "ИП"]
words = ["Алтын Дала", "Нива", "Степной Колос", "Жайлау", "Агро-Восток", "Золотая Нива", "Сары Арка", "Береке", "Урожай",
         "Ак Бидай", "Жасыл Дала", "Хлебный Дом", "Целинное", "Дружба", "Мир Агро", "Наурыз", "Горизонт", "Колос-Плюс",
         "Сеятель", "Тың", "Алқа", "Равнина", "Зерновой Двор", "Агросфера", "Новый День", "Родник", "Восход", "Сельмаш-Агро"]
suffix = ["", "", "", " Плюс", " Групп", " Север", " Юг"]
regions = ["Костанайская обл.", "Акмолинская обл.", "Северо-Казахстанская обл.", "Павлодарская обл.",
           "Карагандинская обл.", "Актюбинская обл.", "Жамбылская обл.", "Туркестанская обл."]
customers, used = [], set()
while len(customers) < 90:
    nm = f"{random.choice(forms)} «{random.choice(words)}{random.choice(suffix)}»"
    if nm in used:
        continue
    used.add(nm)
    customers.append((len(customers) + 1, nm, random.choice(regions), random.choice(managers)[0]))
cust_mgr = {c[0]: c[3] for c in customers}
cust_class = {c[0]: random.choices(["good", "mid", "bad"], [0.55, 0.30, 0.15])[0] for c in customers}

suppliers = [(1, "ТД «Агрокомплект»", "Казахстан"), (2, "Chem Trade Ltd", "Нидерланды"), (3, "Союз-Снаб", "Россия"),
             (4, "Базис Агро", "Казахстан"), (5, "Terra Supply", "Германия"), (6, "Дельта Трейд", "Казахстан"),
             (7, "Агрохим-Поставка", "Казахстан"), (8, "Nordic Agro Trade", "Польша")]
manufacturers = [(1, "AgroLine"), (2, "NordChem"), (3, "SteppeCrop"), (4, "GreenField Labs"), (5, "TerraProtect"), (6, "Delta Agro")]

# id, название, цена от/до, qty от/до/шаг, маржа от/до, ед., префикс, число товаров
G = [(1, "Гербициды", 4500, 9000, 200, 3000, 10, 0.18, 0.28, "л", "Гербицид", 6),
     (2, "Фунгициды", 6000, 15000, 100, 1500, 10, 0.20, 0.30, "л", "Фунгицид", 6),
     (3, "Инсектициды", 5000, 12000, 100, 1200, 10, 0.20, 0.30, "л", "Инсектицид", 5),
     (4, "Протравители", 5000, 9000, 200, 2000, 10, 0.18, 0.26, "л", "Протравитель", 5),
     (5, "Удобрения", 250, 600, 5000, 40000, 500, 0.07, 0.12, "кг", "Удобрение", 5),
     (6, "Семена", 300, 900, 10000, 80000, 500, 0.08, 0.14, "кг", "Семена", 5),
     (7, "Адъюванты", 3000, 5000, 100, 800, 10, 0.22, 0.30, "л", "Адъювант", 3)]
GD = {g[0]: g for g in G}
brands = random.sample(["Страж", "Фаворит", "Аргон", "Титан", "Ратник", "Сокол", "Барс", "Кедр", "Орион", "Вектор", "Зенит", "Атлас",
                        "Гранит", "Дозор", "Эталон", "Фарватер", "Кондор", "Мастер", "Пионер", "Ястреб", "Рубеж", "Лидер", "Нектар",
                        "Аврора", "Бастион", "Витязь", "Импульс", "Каскад", "Легион", "Маяк", "Норд", "Олимп", "Прометей", "Редут",
                        "Саян", "Трофей"], 35)
products, base_price, prod_supplier = [], {}, {}
for g in G:
    for _ in range(g[11]):
        pid = len(products) + 1
        products.append((pid, f"{g[10]} {brands[pid - 1]}", g[0], random.choice(manufacturers)[0], g[9]))
        base_price[pid] = round(random.uniform(g[2], g[3]), -1)
        prod_supplier[pid] = random.choice(suppliers)[0]
prod_group = {p[0]: p[2] for p in products}
warehouses = [(1, "Склад Центральный"), (2, "Склад Север"), (3, "Склад Юг")]


def rnd_money(x):
    return int(round(x))


# ---------------- договоры, заказы, продажи ----------------
contracts, orders_lines, sales_lines, schedule, pay_in = [], [], [], [], []
order_id = order_line_id = sale_line_id = sale_id_seq = pay_id = 0
sale_ids = {}
n_contracts = {2024: 70, 2025: 95, 2026: 115}
need = defaultdict(float)  # (год, product) -> qty

TEMPLATES = [
    (0.40, lambda c, y: [(0.4, "Предоплата", c + D(days=10)), (0.6, "Оплата", dt.date(y, 10, 15))]),
    (0.20, lambda c, y: [(1.0, "Оплата", dt.date(y, 10, 1))]),
    (0.25, lambda c, y: [(0.3, "Предоплата", c + D(days=10)), (0.3, "Оплата", dt.date(y, 7, 20)), (0.4, "Оплата", dt.date(y, 10, 20))]),
    (0.15, lambda c, y: [(0.5, "Предоплата", c + D(days=14)), (0.5, "Оплата", dt.date(y, 9, 10))]),
]


def delay(cls):
    if cls == "good":
        return max(-3, int(random.gauss(2, 4)))
    if cls == "mid":
        return int(abs(random.gauss(12, 10)))
    return int(random.uniform(15, 100))


contract_totals = {}
for sid, _, year in seasons:
    for k in range(n_contracts[year]):
        contract_id = len(contracts) + 1
        cust = random.choice(customers)
        cdate = dt.date(year, 1, 10) + D(days=int(random.triangular(0, 130, 35)))
        mgr = cust[3]
        c_total = 0
        for _o in range(random.choices([1, 2, 3], [0.5, 0.35, 0.15])[0]):
            order_id += 1
            odate = cdate + D(days=random.randint(0, 35))
            ship_dates = [odate + D(days=random.randint(5, 45))]
            for _ in range(random.randint(0, 2)):
                ship_dates.append(ship_dates[-1] + D(days=random.randint(7, 40)))
            for pid in random.sample(range(1, len(products) + 1), random.randint(2, 5)):
                g = GD[prod_group[pid]]
                order_line_id += 1
                qty = random.randrange(g[4], g[5] + 1, g[6])
                price = round(base_price[pid] * INFL[year] * random.uniform(0.93, 1.07) / 10) * 10
                amount = qty * price
                wh = random.choice(warehouses)[0]
                orders_lines.append((order_line_id, order_id, odate, contract_id, cust[0], mgr, sid, pid, wh, qty, price, amount))
                c_total += amount
                need[(year, pid)] += qty
                # отгрузки
                r = random.random()
                frac = 0 if r < 0.05 else (1.0 if r < 0.85 else random.uniform(0.3, 0.8))
                shipped = int(qty * frac)
                nb = random.randint(1, len(ship_dates))
                if shipped > 0:
                    margin = random.uniform(g[7], g[8])
                    part = shipped // nb
                    for bi in range(nb):
                        q = part if bi < nb - 1 else shipped - part * (nb - 1)
                        sdate = ship_dates[bi]
                        if q <= 0 or sdate > END:
                            continue
                        key = (order_id, bi)
                        if key not in sale_ids:
                            sale_id_seq += 1
                            sale_ids[key] = sale_id_seq
                        sale_line_id += 1
                        a = q * price
                        sales_lines.append((sale_line_id, sale_ids[key], sdate, order_line_id, order_id, contract_id, cust[0], mgr, sid, pid, wh,
                                            q, a, rnd_money(a * (1 - margin))))
        contract_totals[contract_id] = c_total
        sign = "Электронный" if random.random() < 0.6 else "Бумажный"
        orig = random.random() < (0.95 if year < 2026 else 0.8)
        contracts.append([contract_id, f"Д-{year % 100}/{k + 1:04d}", cust[0], mgr, sid, cdate, c_total, sign, orig, "Действует"])

        # график платежей
        tpl = random.choices(TEMPLATES, [t[0] for t in TEMPLATES])[0][1](cdate, year)
        left, stages = c_total, []
        for i, (pct, kind, due) in enumerate(tpl):
            amt = left if i == len(tpl) - 1 else rnd_money(round(c_total * pct, -3))
            left -= amt
            stages.append((i + 1, due, pct, amt, kind))
            schedule.append((contract_id, i + 1, due, round(pct * 100, 2), amt, kind))
        # оплаты по этапам
        cls = cust_class[cust[0]]
        for (_, due, pct, amt, kind) in stages:
            u = random.random()
            if cls == "bad" and u < 0.08:
                continue
            total = amt if u > 0.10 else rnd_money(round(amt * random.uniform(0.4, 0.85), -3))
            parts = [total]
            if random.random() < 0.3 and total > 2_000_000:
                f1 = rnd_money(round(total * random.uniform(0.4, 0.7), -3))
                parts = [f1, total - f1]
            pdate = due + D(days=delay(cls))
            for j, p in enumerate(parts):
                d = pdate + D(days=random.randint(3, 25) if j else 0)
                if d > END or p <= 0:
                    continue
                pay_id += 1
                pay_in.append((pay_id, d, cust[0], contract_id, p, kind))

# итоги и статус договоров
shipped_c, paid_c = defaultdict(float), defaultdict(float)
for s in sales_lines:
    shipped_c[s[5]] += s[12]
for p in pay_in:
    paid_c[p[3]] += p[4]
for c in contracts:
    if shipped_c[c[0]] >= 0.99 * c[6] and paid_c[c[0]] >= 0.999 * c[6]:
        c[9] = "Закрыт"

# ---------------- закупки и оплаты поставщикам ----------------
purchases, pay_out = [], []
purch_ids, purchase_total = {}, defaultdict(float)
pl_id = 0
for (year, pid), qty in sorted(need.items()):
    lo = max(START, dt.date(year - 1, 11, 1))
    span = (dt.date(year, 4, 30) - lo).days
    nb = random.choice([2, 3])
    for b in range(nb):
        pdate = lo + D(days=random.randint(0, span))
        sup = prod_supplier[pid]
        key = (sup, pdate)
        if key not in purch_ids:
            purch_ids[key] = len(purch_ids) + 1
        pl_id += 1
        q = rnd_money(qty * 1.03 / nb)
        unit = round(base_price[pid] * INFL[year] * random.uniform(0.74, 0.82) / 10) * 10
        amt = q * unit
        purchases.append((pl_id, purch_ids[key], pdate, sup, pid, random.choice(warehouses)[0], q, amt))
        purchase_total[purch_ids[key]] += amt
purch_meta = {pid_: (d, s) for (s, d), pid_ in purch_ids.items()}
po_id = 0
for pid_, total in sorted(purchase_total.items()):
    d, sup = purch_meta[pid_]
    if random.random() < 0.04:
        continue
    total = rnd_money(total)
    parts = [total]
    if random.random() < 0.35:
        f1 = rnd_money(round(total * random.uniform(0.4, 0.7), -3))
        parts = [f1, total - f1]
    pdate = d + D(days=random.randint(15, 45))
    for j, p in enumerate(parts):
        dd = pdate + D(days=random.randint(20, 50) if j else 0)
        if dd > END:
            continue
        po_id += 1
        pay_out.append((po_id, dd, sup, pid_, p))

# ---------------- план продаж ----------------
actual = defaultdict(float)
actual_qty = defaultdict(float)
for s in sales_lines:
    key = (s[2].year, s[2].month, s[7], prod_group[s[9]])
    actual[key] += s[12]
    actual_qty[key] += s[11]
plan = []
for y in (2024, 2025, 2026):
    for m in range(1, 13):
        for mg in managers:
            for g in G:
                key = (y, m, mg[0], g[0])
                if dt.date(y, m, 1) <= END:
                    base = actual.get(key, 0)
                else:
                    base = actual.get((y - 1, m, mg[0], g[0]), 0) * 1.1
                if base <= 0:
                    continue
                pa = rnd_money(round(base * random.uniform(0.85, 1.25), -3))
                avg_price = (g[2] + g[3]) / 2 * INFL[y]
                plan.append((dt.date(y, m, 1), mg[0], mg[2], g[0], pa, rnd_money(pa / avg_price)))

# ---------------- вывод ----------------
cal = []
d = START
while d <= CAL_END:
    iso = d.isocalendar()
    cal.append((d, d.year, (d.month - 1) // 3 + 1, d.month, MONTHS_RU[d.month - 1], d.replace(day=1), iso[1], iso[2]))
    d += D(days=1)

emit("dim_report_date", ["report_date"], [(END,)])
emit("dim_date", ["date_id", "year", "quarter", "month", "month_name", "month_start", "week", "weekday"], cal)
emit("dim_season", ["season_id", "name", "year"], seasons)
emit("dim_division", ["division_id", "name"], divisions)
emit("dim_manager", ["manager_id", "name", "division_id"], managers)
emit("dim_customer", ["customer_id", "name", "region", "manager_id"], customers)
emit("dim_supplier", ["supplier_id", "name", "country"], suppliers)
emit("dim_manufacturer", ["manufacturer_id", "name"], manufacturers)
emit("dim_product_group", ["group_id", "name"], [(g[0], g[1]) for g in G])
emit("dim_product", ["product_id", "name", "group_id", "manufacturer_id", "unit"], products)
emit("dim_warehouse", ["warehouse_id", "name"], warehouses)
emit("dim_contract", ["contract_id", "number", "customer_id", "manager_id", "season_id", "contract_date", "amount", "sign_type",
                      "original_received", "status"], contracts)
emit("fact_order_line", ["order_line_id", "order_id", "order_date", "contract_id", "customer_id", "manager_id", "season_id", "product_id",
                         "warehouse_id", "qty", "price", "amount"], orders_lines)
emit("fact_sales_line", ["sale_line_id", "sale_id", "sale_date", "order_line_id", "order_id", "contract_id", "customer_id", "manager_id",
                         "season_id", "product_id", "warehouse_id", "qty", "amount", "cost_amount"], sales_lines)
emit("fact_payment_schedule", ["contract_id", "stage_no", "due_date", "percent", "amount", "kind"], schedule)
emit("fact_payment_in", ["payment_id", "payment_date", "customer_id", "contract_id", "amount", "purpose"], pay_in)
emit("fact_purchase_line", ["purchase_line_id", "purchase_id", "purchase_date", "supplier_id", "product_id", "warehouse_id", "qty", "amount"], purchases)
emit("fact_payment_out", ["payment_id", "payment_date", "supplier_id", "purchase_id", "amount"], pay_out)
emit("fact_sales_plan", ["plan_month", "manager_id", "division_id", "product_group_id", "plan_amount", "plan_qty"], plan)
sys.stdout.write("\n".join(out) + "\n")

rev = sum(s[12] for s in sales_lines)
cost = sum(s[13] for s in sales_lines)
print(f"contracts={len(contracts)} order_lines={len(orders_lines)} sales_lines={len(sales_lines)} pay_in={len(pay_in)} "
      f"purchases={len(purchases)} pay_out={len(pay_out)} plan={len(plan)} | revenue={rev / 1e9:.2f}B margin={(rev - cost) / rev:.1%} "
      f"paid_in={sum(p[4] for p in pay_in) / 1e9:.2f}B", file=sys.stderr)
