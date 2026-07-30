"""
Ingest WWW/TheWebConf 2026 + WSDM 2026 from Semantic Scholar — WITH abstracts.

Unlike ICASSP (IEEE-gated, ~18% abstracts), these carry 87-99% abstracts, so a
real per-paper analysis is possible. We pull title + abstract + DOI + arXiv +
open-PDF for every paper, per venue, paging the bulk endpoint with the
continuation token and backing off on the 429 rate limit.
"""
import json, os, time, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
FIELDS = "title,abstract,externalIds,openAccessPdf,url"

VENUES = {
 "WWW 2026":  {"venue": "The Web Conference", "year": "2026", "short": "www"},
 "WSDM 2026": {"venue": "WSDM",               "year": "2026", "short": "wsdm"},
}

def fetch(venue, year, token=None):
    params = {"venue": venue, "year": year, "fields": FIELDS}
    if token: params["token"] = token
    url = BASE + "?" + urllib.parse.urlencode(params)
    for attempt in range(7):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.loads(r.read())
        except Exception as e:
            wait = 5 * (attempt + 1)
            print(f"    retry {attempt+1} after {wait}s ({str(e)[:50]})", flush=True)
            time.sleep(wait)
    raise RuntimeError("failed after retries")

for label, cfg in VENUES.items():
    papers, token, page = [], None, 0
    print(f"== {label} ==", flush=True)
    while True:
        d = fetch(cfg["venue"], cfg["year"], token)
        for p in (d.get("data") or []):
            ext = p.get("externalIds") or {}
            papers.append({
                "paperId": p.get("paperId"), "title": (p.get("title") or "").strip(),
                "abstract": p.get("abstract"), "doi": ext.get("DOI"), "arxiv": ext.get("ArXiv"),
                "pdf": (p.get("openAccessPdf") or {}).get("url") or None, "url": p.get("url"),
            })
        page += 1
        print(f"  page {page}: total {len(papers)} / {d.get('total')}", flush=True)
        token = d.get("token")
        if not token or not (d.get("data")): break
        time.sleep(3)
    # de-dup by title
    seen, uniq = set(), []
    for p in papers:
        k = p["title"].lower()
        if k and k not in seen: seen.add(k); uniq.append(p)
    wa = sum(1 for p in uniq if p["abstract"])
    out = os.path.join(HERE, "data", f"{cfg['short']}-2026-papers.json")
    json.dump({"venue": label, "n_papers": len(uniq), "with_abstract": wa, "papers": uniq},
              open(out, "w"), indent=1)
    print(f"  -> {len(uniq)} papers, {wa} abstracts ({wa*100//max(len(uniq),1)}%) -> {out}\n", flush=True)
print("done")
