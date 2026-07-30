"""
Split papers-with-abstracts into batch files for the Phase-2 Haiku workflow.
Each batch is a small JSON of {id, title, abstract(truncated)} the analysis agent
reads and returns per-paper problem/approach/contribution for.
"""
import json, os, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
BATCH_DIR = os.path.join(HERE, "data", "batches")
OUT_DIR = os.path.join(HERE, "data", "out")
os.makedirs(BATCH_DIR, exist_ok=True); os.makedirs(OUT_DIR, exist_ok=True)

# which venue files to batch (default WWW+WSDM; pass filenames to override)
files = sys.argv[1:] or ["www-2026-papers.json", "wsdm-2026-papers.json"]
papers = []
for fn in files:
    path = os.path.join(HERE, "data", fn)
    if not os.path.exists(path):
        print("skip missing", fn); continue
    d = json.load(open(path))
    for p in d["papers"]:
        if p.get("abstract"):                       # only papers we can actually analyze
            papers.append({"id": p["paperId"] if p.get("paperId") else (p.get("doi") or p["title"][:60]),
                           "venue": d["venue"], "title": p["title"],
                           "abstract": p["abstract"][:1400]})

# stable id -> also keep a global index
for i, p in enumerate(papers):
    p["gid"] = i

SIZE = 15
n_batches = (len(papers) + SIZE - 1) // SIZE
# clear old batches
for f in glob.glob(os.path.join(BATCH_DIR, "*.json")): os.remove(f)
for b in range(n_batches):
    chunk = papers[b*SIZE:(b+1)*SIZE]
    json.dump(chunk, open(os.path.join(BATCH_DIR, f"b{b:03d}.json"), "w"), indent=1)

json.dump({"n_papers": len(papers), "n_batches": n_batches, "size": SIZE, "files": files},
          open(os.path.join(HERE, "data", "batch_manifest.json"), "w"), indent=1)
print(f"{len(papers)} papers with abstracts -> {n_batches} batches of {SIZE} in {BATCH_DIR}")
