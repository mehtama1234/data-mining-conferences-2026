"""
Per-venue character: what WWW vs WSDM vs SIGIR 2026 each emphasize.
The signal isn't raw counts (WWW is biggest) — it's what each venue OVER-indexes
on relative to the pooled average (lift = venue's within-venue rate / global rate).
We do this for both keyword themes and the LLM-tagged techniques.
"""
import json, os, re
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TH = json.load(open(os.path.join(HERE, "data", "themes.json")))
AN = json.load(open(os.path.join(HERE, "data", "analysis.json")))

VENUES = ["WWW 2026", "WSDM 2026", "SIGIR 2026"]
venue_total = TH["venues"]                                  # papers per venue (all)

# --- theme rates + lift ------------------------------------------------------
theme_profile = {v: {} for v in VENUES}
for t in TH["themes"]:
    global_rate = t["n"] / TH["n_papers"]
    for v in VENUES:
        cn = t["by_venue"].get(v, 0)
        rate = cn / venue_total[v]
        theme_profile[v][t["theme"]] = {"n": cn, "rate": rate,
                                        "lift": round(rate / global_rate, 2) if global_rate else 0}

# --- technique tags per venue (normalize like summarize.py) ------------------
CANON = {
 r"^llms?$|large language model": "LLM", r"gnn|graph neural|^graph$": "graph neural nets",
 r"^rag$|retrieval[- ]aug": "RAG", r"contrastive": "contrastive learning",
 r"multi[- ]?agent|^agent$|agentic": "agents", r"reinforcement|^rl$": "reinforcement learning",
 r"multimodal|multi[- ]modal": "multimodal", r"mixture[- ]of[- ]experts|^moe$": "mixture-of-experts",
 r"diffusion": "diffusion", r"knowledge graph|^kg$": "knowledge graph",
 r"reasoning|chain[- ]of[- ]thought|^cot$": "reasoning", r"distill": "distillation",
 r"fairness|debias": "fairness", r"federated": "federated learning", r"adversarial": "adversarial",
 r"transformer": "transformer", r"attention": "attention", r"embedding": "embeddings",
 r"clustering": "clustering", r"benchmark|dataset|evaluation": "benchmark/eval", r"prompt": "prompting",
 r"fine[- ]?tun|lora|peft|adapter": "fine-tuning/PEFT", r"recommendation|recommender": "recommendation",
 r"retrieval|ranking|dense retriev": "retrieval/ranking",
}
def canon(tag):
    t = str(tag).lower().strip()
    for pat, name in CANON.items():
        if re.search(pat, t): return name
    return None

venue_meth = defaultdict(Counter); venue_analyzed = Counter(); global_meth = Counter()
for p in AN["papers"]:
    v = p["venue"]; venue_analyzed[v] += 1
    seen = set()
    for tag in (p.get("methods") or []):
        c = canon(tag)
        if c and c not in seen:
            venue_meth[v][c] += 1; global_meth[c] += 1; seen.add(c);
tot_analyzed = sum(venue_analyzed.values())

def method_lift(v):
    out = []
    for m, gn in global_meth.items():
        if gn < 15: continue
        grate = gn / tot_analyzed
        vrate = venue_meth[v][m] / max(venue_analyzed[v], 1)
        out.append({"tag": m, "n": venue_meth[v][m], "lift": round(vrate/grate, 2) if grate else 0})
    return out

profiles = {}
for v in VENUES:
    themes_sorted = sorted(theme_profile[v].items(), key=lambda kv: -kv[1]["rate"])
    themes_distinct = sorted([{"theme": k, **val} for k, val in theme_profile[v].items() if val["n"] >= 8],
                             key=lambda x: -x["lift"])
    m = method_lift(v)
    top_methods = sorted(m, key=lambda x: -x["n"])[:10]
    distinct_methods = sorted([x for x in m if x["n"] >= 6], key=lambda x: -x["lift"])[:8]
    profiles[v] = {
        "n_papers": venue_total[v], "n_analyzed": venue_analyzed[v],
        "top_themes": [{"theme": k, "n": val["n"], "pct": round(val["rate"]*100, 1)} for k, val in themes_sorted[:8]],
        "distinct_themes": themes_distinct[:6],
        "top_methods": top_methods,
        "distinct_methods": distinct_methods,
    }

json.dump({"venues": VENUES, "profiles": profiles}, open(os.path.join(HERE, "data", "venue_profiles.json"), "w"), indent=1)
for v in VENUES:
    p = profiles[v]
    print(f"\n=== {v}  ({p['n_papers']} papers) ===")
    print("  over-indexes (themes):", ", ".join(f"{t['theme']}×{t['lift']}" for t in p["distinct_themes"][:4]))
    print("  over-indexes (methods):", ", ".join(f"{m['tag']}×{m['lift']}" for m in p["distinct_methods"][:5]))
print("\nwrote data/venue_profiles.json")
