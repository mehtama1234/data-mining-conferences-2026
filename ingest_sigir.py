"""
Ingest SIGIR 2026 — DBLP has it (~685) but Semantic Scholar has no venue entry,
so: parse titles + DOIs from the DBLP proceedings page, then batch-fetch abstracts
from S2 by DOI. Gives us titles for all, abstracts for whatever S2 has by DOI.
"""
import json, os, re, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DBLP = "https://dblp.org/db/conf/sigir/sigir2026.html"

def get(url, hdr=None):
    req = urllib.request.Request(url, headers=hdr or {"User-Agent": "Mozilla/5.0 research"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")

# 1. DBLP: titles + DOIs
html = get(DBLP)
# each inproceedings entry: <span class="title" itemprop="name">TITLE.</span> ... doi.org/DOI
entries = re.split(r'class="entry inproceedings"', html)[1:]
papers = []
for e in entries:
    mt = re.search(r'<span class="title"[^>]*>(.*?)</span>', e, re.S)
    if not mt: continue
    title = re.sub(r"<[^>]+>", "", mt.group(1)).strip().rstrip(".")
    md = re.search(r'https?://doi\.org/([^"<]+)', e)
    doi = md.group(1) if md else None
    if title:
        papers.append({"title": title, "doi": doi, "abstract": None})
# de-dup
seen, uniq = set(), []
for p in papers:
    k = p["title"].lower()
    if k not in seen: seen.add(k); uniq.append(p)
print(f"DBLP SIGIR 2026: {len(uniq)} papers ({sum(1 for p in uniq if p['doi'])} with DOI)", flush=True)

# 2. S2 batch abstracts by DOI
dois = [p["doi"] for p in uniq if p["doi"]]
by_doi = {}
BATCH = 100
for i in range(0, len(dois), BATCH):
    chunk = dois[i:i+BATCH]
    ids = ["DOI:" + d for d in chunk]
    for attempt in range(6):
        try:
            req = urllib.request.Request(
                "https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,abstract,externalIds",
                data=json.dumps({"ids": ids}).encode(), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=90) as r:
                res = json.loads(r.read())
            for item in res:
                if item and item.get("abstract"):
                    d = (item.get("externalIds") or {}).get("DOI")
                    if d: by_doi[d.lower()] = item["abstract"]
            print(f"  S2 batch {i//BATCH+1}: +{sum(1 for x in res if x and x.get('abstract'))} abstracts", flush=True)
            break
        except Exception as ex:
            time.sleep(6*(attempt+1)); print(f"    retry ({str(ex)[:40]})", flush=True)
    time.sleep(2)

for p in uniq:
    if p["doi"] and p["doi"].lower() in by_doi:
        p["abstract"] = by_doi[p["doi"].lower()]
wa = sum(1 for p in uniq if p["abstract"])
out = os.path.join(HERE, "data", "sigir-2026-papers.json")
json.dump({"venue": "SIGIR 2026", "n_papers": len(uniq), "with_abstract": wa, "papers": uniq},
          open(out, "w"), indent=1)
print(f"-> {len(uniq)} papers, {wa} abstracts ({wa*100//max(len(uniq),1)}%) -> {out}", flush=True)
