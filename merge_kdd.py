"""Merge KDD combined analysis+rich output into analysis.json + rich.json.
Idempotent: strips any existing gid>=2000 rows first, then re-adds."""
import json, os, glob, re

HERE = os.path.dirname(os.path.abspath(__file__))
meta = json.load(open(os.path.join(HERE, "data", "kdd_meta.json")))
A = json.load(open(os.path.join(HERE, "data", "analysis.json")))
RP = os.path.join(HERE, "data", "rich.json")
RICH = json.load(open(RP)) if os.path.exists(RP) else {}

def clean(s):
    return re.sub(r"\s+", " ", (s or "").replace('\\"', '"').replace("**", "")).strip()

out, bad = {}, []
for f in sorted(glob.glob(os.path.join(HERE, "data", "kdd_out", "b*.json"))):
    try:
        out.update(json.load(open(f)))
    except Exception as e:
        bad.append((os.path.basename(f), str(e)[:60]))

# drop existing KDD rows (idempotent)
A["papers"] = [p for p in A["papers"] if not (2000 <= p.get("gid", -1) <= 2999)]
for k in list(RICH):
    if k.isdigit() and 2000 <= int(k) <= 2999:
        del RICH[k]

added = 0
for gid, v in out.items():
    m = meta.get(str(gid), {})
    doi = m.get("doi")
    A["papers"].append({
        "venue": "KDD 2026", "title": m.get("title", ""), "doi": doi,
        "url": m.get("url") or (("https://doi.org/" + doi) if doi else ""),
        "gid": int(gid),
        "problem": clean(v.get("problem")), "approach": clean(v.get("approach")),
        "contribution": clean(v.get("contribution")), "primary_theme": clean(v.get("primary_theme")),
        "methods": [clean(x) for x in (v.get("methods") or [])][:4],
    })
    if v.get("bp"):
        RICH[str(gid)] = {k: clean(v.get(k)) for k in ("bp", "wh", "ap", "ww", "po")}
    added += 1

A["n_analyzed"] = len(A["papers"])
A["n_papers"] = max(A.get("n_papers", 0), len(A["papers"]))
json.dump(A, open(os.path.join(HERE, "data", "analysis.json"), "w"), indent=1)
json.dump(RICH, open(RP, "w"), indent=1)
print(f"added {added} KDD papers -> analysis.json now {len(A['papers'])} papers; rich.json {len(RICH)}")
if bad:
    print("BAD batches (re-run these):", bad)
