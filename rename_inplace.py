#!/usr/bin/env python3
"""Переименовывает поля в уже открытом/правленном Desktop проекте, не пересоздавая его.
   python3 rename_inplace.py <папка с Demo_Agro.pbip>   (словари берутся из build_pbip.py рядом)"""
import os, re, sys, runpy
root = os.path.abspath(sys.argv[1])
gen = runpy.run_path(os.path.join(root, "build_pbip.py"), run_name="lib", init_globals={}) if False else None
src = open(os.path.join(root, "build_pbip.py"), encoding="utf-8").read()
src = src[:src.index("\nbuild_model()\nbuild_report()")]
sys.argv = [sys.argv[0], "/tmp/_unused"]
G = {"__name__": "lib"}
exec(compile(src, "build_pbip.py", "exec"), G)
ru, SRC, tr_dax, q = G["ru"], G["SRC"], G["tr_dax"], G["q"]
SELF = G["_SELF"]
td = os.path.join(root, "Demo_Agro.SemanticModel", "definition", "tables")

# 1. собрать карту имён по факту из файлов (включая добавленные вручную колонки)
for fn in sorted(os.listdir(td)):
    t = fn[:-5]
    if t == "_Measures":
        continue
    txt = open(os.path.join(td, fn), encoding="utf-8").read()
    for m in re.finditer(r"^\tcolumn (?:'((?:[^']|'')+)'|(\S+))", txt, re.M):
        c = (m.group(1) or m.group(2)).replace("''", "'")
        SELF.setdefault(t, {})
        if c not in SELF[t]:
            SELF[t][c] = ru(t, c)

def newname(t, c):
    return SELF[t][c]

for fn in sorted(os.listdir(td)):
    t = fn[:-5]
    p = os.path.join(td, fn)
    txt = open(p, encoding="utf-8").read()
    if t == "_Measures":
        out = tr_dax(txt)
    else:
        cols = [(m.group(1) or m.group(2)).replace("''", "'")
                for m in re.finditer(r"^\tcolumn (?:'((?:[^']|'')+)'|(\S+))", txt, re.M)]
        calc = set(re.findall(r"^\tcolumn (?:'(?:[^']|'')+'|\S+) =", txt, re.M) and
                   [(m.group(1) or m.group(2)).replace("''", "'") for m in re.finditer(r"^\tcolumn (?:'((?:[^']|'')+)'|(\S+)) =", txt, re.M)])
        head, _, _ = txt.partition("\tpartition ")
        lines = []
        for ln in head.split("\n"):
            m = re.match(r"^\tcolumn (?:'((?:[^']|'')+)'|(\S+))( = .*)?$", ln)
            if m:
                c = (m.group(1) or m.group(2)).replace("''", "'")
                expr = m.group(3)
                ln = "\tcolumn " + q(newname(t, c)) + (" = " + tr_dax(expr[3:], t) if expr else "")
            m = re.match(r"^(\t\tsourceColumn: )(.+)$", ln)
            if m:
                ln = m.group(1) + newname(t, m.group(2))
            m = re.match(r"^(\t\tsortByColumn: )(.+)$", ln)
            if m:
                ln = m.group(1) + q(newname(t, m.group(2).strip("'")))
            lines.append(ln)
        item, ren0 = SRC.get(t, (t, {}))
        back = {v: k for k, v in ren0.items()}
        pairs = ", ".join('{"%s", "%s"}' % (back.get(c, c), newname(t, c)) for c in cols if c not in calc)
        part = [f"\tpartition {q(t)} = m", "\t\tmode: import", "\t\tsource =", "\t\t\t\tlet",
                "\t\t\t\t    Source = PostgreSQL.Database(DbServer, DbName),",
                f'\t\t\t\t    Data = Source{{[Schema = "public", Item = "{item}"]}}[Data],',
                f"\t\t\t\t    Renamed = Table.RenameColumns(Data, {{{pairs}}})", "\t\t\t\tin", "\t\t\t\t    Renamed", ""]
        out = "\n".join(lines) + "\n".join(part)
    open(p, "w", encoding="utf-8", newline="\n").write(out)

# связи
rp = os.path.join(root, "Demo_Agro.SemanticModel", "definition", "relationships.tmdl")
def fix(m):
    side, tb, col = m.group(1), m.group(2), (m.group(3) or m.group(4))
    return f"\t{side}: {tb}.{q(newname(tb, col))}"
rtxt = open(rp, encoding="utf-8").read()
rtxt = re.sub(r"^\t(fromColumn|toColumn): (\w+)\.(?:'([^']+)'|(\w+))$", fix, rtxt, flags=re.M)
open(rp, "w", encoding="utf-8", newline="\n").write(rtxt)
print("done")
