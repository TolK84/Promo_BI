#!/usr/bin/env python3
"""Меняет в Demo_Agro.Report только ссылки на поля (Property/queryRef) на русские имена. Всё остальное не трогает.
   python3 rename_report.py <папка проекта>"""
import json, os, re, sys
root = os.path.abspath(sys.argv[1])
src = open(os.path.join(root, "build_pbip.py"), encoding="utf-8").read()
src = src[:src.index("\nbuild_model()\nbuild_report()")]
sys.argv = [sys.argv[0], "/tmp/_unused"]
G = {"__name__": "lib"}
exec(compile(src, "build_pbip.py", "exec"), G)
SELF = G["_SELF"]
n_changed = 0

def conv(o, scope):
    global n_changed
    if isinstance(o, list):
        return [conv(x, scope) for x in o]
    if not isinstance(o, dict):
        if isinstance(o, str):
            m = re.fullmatch(r"(\w+)\.(\w+)", o)
            if m and m.group(1) in SELF and m.group(2) in SELF[m.group(1)]:
                n_changed += 1
                return f"{m.group(1)}.{SELF[m.group(1)][m.group(2)]}"
        return o
    sc = dict(scope)
    for f in o.get("From", []) if isinstance(o.get("From"), list) else []:
        if isinstance(f, dict) and "Name" in f and "Entity" in f:
            sc[f["Name"]] = f["Entity"]
    old_qr = o.get("queryRef")
    out = {}
    for k, v in o.items():
        out[k] = conv(v, sc)
    # Property рядом с SourceRef
    ex = o.get("Expression")
    if "Property" in o and isinstance(ex, dict) and isinstance(ex.get("SourceRef"), dict):
        sr = ex["SourceRef"]
        ent = sr.get("Entity") or sc.get(sr.get("Source"))
        if ent in SELF and o["Property"] in SELF[ent]:
            out["Property"] = SELF[ent][o["Property"]]
            n_changed += 1
    if isinstance(old_qr, str) and out.get("queryRef") != old_qr and out.get("nativeQueryRef") == old_qr.split(".", 1)[1]:
        out["nativeQueryRef"] = out["queryRef"].split(".", 1)[1]
    return out

for dp, _, fs in os.walk(os.path.join(root, "Demo_Agro.Report", "definition")):
    for fn in fs:
        if fn.endswith(".json"):
            p = os.path.join(dp, fn)
            d = json.load(open(p, encoding="utf-8"))
            nd = conv(d, {})
            if nd != d:
                open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(nd, ensure_ascii=False, indent=2) + "\n")
print("замен:", n_changed)
