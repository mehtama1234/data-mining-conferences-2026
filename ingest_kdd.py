"""
Ingest KDD 2026 (SIGKDD). The conference is August 2026, so proceedings are still
filling: S2 has ~136 papers but only ~32% abstracts. We pull the S2 list (for DOIs),
then BACKFILL missing abstracts from OpenAlex (by DOI, reconstructing the abstract from
its inverted index). Output matches the WWW/WSDM/SIGIR format so the rest of the
pipeline (mine_themes, batches, per-paper Haiku) is unchanged.
"""
import json, os, time, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
S2 = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
FIELDS = "title,abstract,externalIds,openAccessPdf,url"
OA = "https://api.openalex.org/works/doi:"
MAILTO = "mehtama1@gmail.com"  # OpenAlex polite pool

def get(url, tries=6, timeout=45):
    for a in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return json.loads(r.read())
        except Exception as e:
            code = getattr(e, "code", None)
            if code == 404:
                return None
            time.sleep(4 * (a + 1))
    return None

def s2_bulk(venue, year):
    papers, token, page = [], None, 0
    while True:
        params = {"venue": venue, "year": year, "fields": FIELDS}
        if token: params["token"] = token
        d = get(S2 + "?" + urllib.parse.urlencode(params))
        if not d: break
        for p in (d.get("data") or []):
            ext = p.get("externalIds") or {}
            papers.append({
                "paperId": p.get("paperId"), "title": (p.get("title") or "").strip(),
                "abstract": p.get("abstract"), "doi": ext.get("DOI"), "arxiv": ext.get("ArXiv"),
                "pdf": (p.get("openAccessPdf") or {}).get("url") or None, "url": p.get("url"),
            })
        page += 1
        print(f"  S2 page {page}: {len(papers)} / {d.get('total')}", flush=True)
        token = d.get("token")
        if not token or not d.get("data"): break
        time.sleep(3)
    return papers

def oa_abstract(doi):
    d = get(OA + urllib.parse.quote(doi) + "?mailto=" + MAILTO)
    if not d: return None
    inv = d.get("abstract_inverted_index")
    if not inv: return None
    pos = {}
    for word, idxs in inv.items():
        for i in idxs: pos[i] = word
    return " ".join(pos[i] for i in sorted(pos)) or None

papers = s2_bulk("Knowledge Discovery and Data Mining", "2026")
# de-dup by title
seen, uniq = set(), []
for p in papers:
    k = p["title"].lower()
    if k and k not in seen: seen.add(k); uniq.append(p)

before = sum(1 for p in uniq if (p.get("abstract") or "").strip())
print(f"  S2 gave {len(uniq)} papers, {before} with abstracts. Backfilling from OpenAlex…", flush=True)
filled = 0
for i, p in enumerate(uniq):
    if (p.get("abstract") or "").strip() or not p.get("doi"):
        continue
    ab = oa_abstract(p["doi"])
    if ab and len(ab) > 40:
        p["abstract"] = ab; filled += 1
    if i % 20 == 0:
        print(f"    …{i}/{len(uniq)} scanned, +{filled} filled", flush=True)
    time.sleep(0.3)

wa = sum(1 for p in uniq if (p.get("abstract") or "").strip())
out = os.path.join(HERE, "data", "kdd-2026-papers.json")
json.dump({"venue": "KDD 2026", "n_papers": len(uniq), "with_abstract": wa, "papers": uniq},
          open(out, "w"), indent=1)
print(f"\n  -> {len(uniq)} papers, {wa} abstracts ({wa*100//max(len(uniq),1)}%; +{filled} via OpenAlex) -> {out}")
