"""Build KDD batches for the combined analysis+rich Haiku pass.
Only papers WITH abstracts (50 of 136). gids start at 2000 to avoid colliding
with the existing 0..1486 from WWW/WSDM/SIGIR."""
import json, os, glob

HERE = os.path.dirname(os.path.abspath(__file__))
BDIR = os.path.join(HERE, "data", "kdd_batches")
os.makedirs(BDIR, exist_ok=True)
os.makedirs(os.path.join(HERE, "data", "kdd_out"), exist_ok=True)

papers = json.load(open(os.path.join(HERE, "data", "kdd-2026-papers.json")))["papers"]
withab = [p for p in papers if (p.get("abstract") or "").strip()]
GID0 = 2000
batch = []
for i, p in enumerate(withab):
    batch.append({"gid": GID0 + i, "venue": "KDD 2026", "title": p["title"],
                  "abstract": (p["abstract"] or "")[:1400],
                  "doi": p.get("doi"), "url": p.get("url"),
                  "pdf": p.get("pdf"), "arxiv": p.get("arxiv")})

SIZE = 13
for f in glob.glob(os.path.join(BDIR, "*.json")):
    os.remove(f)
n = (len(batch) + SIZE - 1) // SIZE
for b in range(n):
    json.dump(batch[b*SIZE:(b+1)*SIZE], open(os.path.join(BDIR, f"b{b:03d}.json"), "w"), indent=1)
# keep a manifest of the full metadata (for merge to recover doi/url by gid)
json.dump({p["gid"]: p for p in batch}, open(os.path.join(HERE, "data", "kdd_meta.json"), "w"), indent=1)
print(f"{len(withab)} KDD papers with abstracts -> {n} batches of {SIZE} (gids {GID0}..{GID0+len(withab)-1})")
