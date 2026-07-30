"""
Merge the Phase-2 per-paper analysis (data/out/b*.json, written by the Haiku
workflow) back onto the papers, keyed by gid. Validates each batch, reports
coverage + any malformed batches, and writes data/analysis.json.
"""
import json, os, glob

HERE = os.path.dirname(os.path.abspath(__file__))
# rebuild gid -> paper map exactly as make_batches did
files = json.load(open(os.path.join(HERE, "data", "batch_manifest.json")))["files"]
papers = []
for fn in files:
    d = json.load(open(os.path.join(HERE, "data", fn)))
    for p in d["papers"]:
        if p.get("abstract"):
            papers.append({"venue": d["venue"], "title": p["title"], "doi": p.get("doi"),
                           "url": p.get("url")})
for i, p in enumerate(papers):
    p["gid"] = i
by_gid = {p["gid"]: p for p in papers}

analyses = {}
bad_batches = []
for f in sorted(glob.glob(os.path.join(HERE, "data", "out", "b*.json"))):
    try:
        arr = json.load(open(f))
        assert isinstance(arr, list)
        for a in arr:
            g = a.get("gid")
            if isinstance(g, int) and g in by_gid:
                analyses[g] = {k: a.get(k) for k in ("problem", "approach", "contribution", "primary_theme", "methods")}
    except Exception as e:
        bad_batches.append((os.path.basename(f), str(e)[:50]))

merged = []
for p in papers:
    a = analyses.get(p["gid"])
    if a:
        merged.append({**p, **a})

out = os.path.join(HERE, "data", "analysis.json")
json.dump({"n_papers": len(papers), "n_analyzed": len(merged),
           "coverage_pct": round(len(merged)*100/max(len(papers), 1), 1),
           "bad_batches": bad_batches, "papers": merged}, open(out, "w"), indent=1)
print(f"papers with abstracts: {len(papers)}")
print(f"analyzed & merged:     {len(merged)} ({len(merged)*100//max(len(papers),1)}%)")
print(f"malformed batches:     {len(bad_batches)} {bad_batches[:5]}")
# quick theme tally from the LLM's primary_theme labels
from collections import Counter
themes = Counter(m["primary_theme"] for m in merged if m.get("primary_theme"))
print(f"distinct LLM themes:   {len(themes)}; top:", [t for t, _ in themes.most_common(10)])
print("wrote data/analysis.json")
