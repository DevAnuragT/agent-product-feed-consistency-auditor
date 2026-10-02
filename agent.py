#!/usr/bin/env python3
"""Deterministic local-only evidence checks."""
import json, math, sys
from pathlib import Path
DOMAIN = 'Product Feed Consistency Auditor'
RULES = [('missing_sku_count', 'missing SKU count', 'max', 0), ('invalid_price_count', 'invalid price count', 'max', 0), ('currency', 'feed currency', 'required', None), ('feed_age_hours', 'feed age', 'max', 24)]
def analyze(payload):
    if not isinstance(payload, dict): raise ValueError("payload must be an object")
    findings=[]; passed=0
    for field,label,kind,threshold in RULES:
        value=payload.get(field); ok=True
        missing=value is None or value=="" or value==[] or value=={}
        if kind == "required": ok=not missing
        elif kind == "true": ok=value is True
        elif kind in ("min","max"):
            ok=isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value)
            if ok: ok = value >= threshold if kind == "min" else value <= threshold
        elif kind in ("min_items","max_items"):
            ok=isinstance(value,list)
            if ok: ok = len(value) >= threshold if kind == "min_items" else len(value) <= threshold
        if ok: passed+=1
        else: findings.append({"rule":field,"label":label,"observed":value,"expected":f"{kind} {threshold}","action":f"Review and correct {label} evidence."})
    return {"domain":DOMAIN,"status":"pass" if passed == len(RULES) else "needs-review","score":{"passed":passed,"total":len(RULES)},"findings":findings,"checked_rules":[r[0] for r in RULES]}
if __name__ == "__main__":
    source=Path(sys.argv[1]) if len(sys.argv)>1 else None
    payload=json.loads(source.read_text(encoding="utf-8") if source else sys.stdin.read())
    print(json.dumps(analyze(payload),indent=2,sort_keys=True))
