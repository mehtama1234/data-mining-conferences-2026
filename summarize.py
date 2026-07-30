"""
Summarize the per-paper analysis: normalize the LLM's method tags + fine-grained
themes into clean, canonical aggregates for the site.
"""
import json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "data", "analysis.json")))
ps = d["papers"]

# --- normalize method tags (merge obvious variants) --------------------------
CANON = {
 r"^llms?$|large language model": "LLM",
 r"gnn|graph neural|^graph$": "graph neural nets",
 r"^rag$|retrieval[- ]aug": "RAG",
 r"contrastive": "contrastive learning",
 r"multi[- ]?agent|^agent$|agentic": "agents",
 r"reinforcement|^rl$": "reinforcement learning",
 r"multimodal|multi[- ]modal": "multimodal",
 r"mixture[- ]of[- ]experts|^moe$": "mixture-of-experts",
 r"diffusion": "diffusion",
 r"knowledge graph|^kg$": "knowledge graph",
 r"reasoning|chain[- ]of[- ]thought|^cot$": "reasoning",
 r"distill": "distillation",
 r"fairness|debias": "fairness",
 r"federated": "federated learning",
 r"adversarial": "adversarial",
 r"transformer": "transformer",
 r"attention": "attention",
 r"embedding": "embeddings",
 r"clustering": "clustering",
 r"benchmark|dataset|evaluation": "benchmark/eval",
 r"prompt": "prompting",
 r"fine[- ]?tun|lora|peft|adapter": "fine-tuning/PEFT",
 r"recommendation|recommender": "recommendation",
 r"retrieval|ranking|dense retriev": "retrieval/ranking",
}
def canon(tag):
    t = str(tag).lower().strip()
    for pat, name in CANON.items():
        if re.search(pat, t):
            return name
    return None

method_counts = Counter()
for p in ps:
    seen = set()
    for tag in (p.get("methods") or []):
        c = canon(tag)
        if c and c not in seen:
            method_counts[c] += 1; seen.add(c)

# --- consolidate fine-grained themes into canonical families -----------------
FAMILIES = {
 "Recommendation": r"recommend",
 "Retrieval & Ranking": r"retriev|ranking|search|\bir\b",
 "LLM methods & training": r"\bllm\b|language model|fine[- ]?tun|prompt|instruction|alignment|rlhf",
 "LLM agents": r"agent",
 "RAG & knowledge": r"\brag\b|retrieval[- ]aug|knowledge graph|knowledge base",
 "Graph learning": r"graph|\bgnn\b|node|link predict",
 "Recsys: sequential/session": r"sequential|session|next[- ]item",
 "Fairness & responsible": r"fair|bias|responsib|ethic|privacy|debias",
 "Security & robustness": r"attack|adversar|security|robust|poison|inversion",
 "Multimodal": r"multimodal|vision[- ]language|image[- ]text",
 "Recsys: cold-start/cross-domain": r"cold[- ]?start|cross[- ]?domain",
 "Time series & anomaly": r"time series|forecast|anomaly|spatio",
 "Misinformation & social": r"misinform|fake|rumor|social|influence|opinion",
 "Reasoning & QA": r"reasoning|question answer|\bqa\b",
 "Efficiency": r"efficient|scalab|acceler|distill|compress|quantiz",
 "Evaluation & benchmarks": r"benchmark|evaluation|dataset|survey",
}
fam_counts = Counter()
for p in ps:
    th = (p.get("primary_theme") or "").lower()
    matched = False
    for fam, pat in FAMILIES.items():
        if re.search(pat, th):
            fam_counts[fam] += 1; matched = True; break
    if not matched:
        fam_counts["Other"] += 1

OUT = {
 "n_analyzed": len(ps),
 "methods": [{"tag": t, "n": n} for t, n in method_counts.most_common(28)],
 "theme_families": [{"family": f, "n": n} for f, n in fam_counts.most_common()],
}
json.dump(OUT, open(os.path.join(HERE, "data", "summary.json"), "w"), indent=1)
print("top methods:", ", ".join(f"{m['tag']}({m['n']})" for m in OUT["methods"][:16]))
print("\ntheme families:")
for f in OUT["theme_families"]:
    print(f"  {f['n']:>4}  {f['family']}")
print("wrote data/summary.json")
