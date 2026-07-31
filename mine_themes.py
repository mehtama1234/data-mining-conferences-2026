"""
Theme-mine WWW 2026 + WSDM 2026 over title + ABSTRACT.

These venues carry real abstracts (87-99%), so keyword matching runs over the full
title+abstract text — far more accurate than titles alone. We assign each paper to
one or more research themes from a data-mining/web taxonomy, unify across the two
venues, and surface per-theme example papers + per-venue breakdown. Deterministic
and transparent; a deeper per-paper LLM pass can layer on top later.
"""
import json, os, re
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = [("WWW 2026", "www-2026-papers.json"), ("WSDM 2026", "wsdm-2026-papers.json"), ("SIGIR 2026", "sigir-2026-papers.json"), ("KDD 2026", "kdd-2026-papers.json")]

THEMES = {
 "LLMs & Language Models": [r"\bllm\b", r"large language model", r"\bgpt\b", r"language model", r"instruction[- ]?tun", r"prompt", r"in[- ]?context learn", r"chatgpt", r"\bfoundation model"],
 "LLM Agents & Tool Use": [r"\bagent", r"tool[- ]?use", r"tool[- ]?call", r"multi[- ]?agent", r"agentic", r"planning.*llm", r"autonomous.*(agent|llm)"],
 "Retrieval-Augmented (RAG)": [r"retrieval[- ]?augmented", r"\brag\b", r"retrieval[- ]?augment", r"grounding.*retriev"],
 "Recommender Systems": [r"recommend", r"\bctr\b", r"click[- ]?through", r"collaborative filter", r"cold[- ]?start", r"session[- ]?based", r"sequential recommend", r"user preference"],
 "Graph Learning & Mining": [r"graph neural", r"\bgnn\b", r"graph mining", r"graph representation", r"node classif", r"link prediction", r"graph embedding", r"heterogeneous graph", r"subgraph", r"community detection"],
 "Knowledge Graphs": [r"knowledge graph", r"\bkg\b", r"entity linking", r"knowledge base", r"ontolog", r"triple.*embedding", r"kg completion"],
 "Information Retrieval & Search": [r"information retrieval", r"\bir\b", r"ranking", r"search engine", r"dense retriev", r"passage retriev", r"query", r"relevance", r"\bbert.*retriev"],
 "Fairness, Bias & Responsible AI": [r"fairness", r"\bbias\b", r"debias", r"discrimination", r"responsible", r"ethic", r"equit", r"disparate"],
 "Privacy, Federated & Security": [r"privacy", r"federated", r"differential privacy", r"secure", r"encryption", r"membership inference", r"\bcyber", r"malware"],
 "Misinformation & Trust": [r"misinformation", r"fake news", r"disinformation", r"rumor", r"fact[- ]?check", r"credibility", r"\btrust\b", r"toxic", r"hate speech", r"moderation"],
 "Fraud & Anomaly Detection": [r"fraud", r"anomaly detection", r"outlier", r"bot detection", r"spam", r"abuse detect"],
 "Social Networks & Influence": [r"social network", r"social media", r"influence", r"diffusion.*network", r"viral", r"opinion", r"user behav", r"engagement"],
 "Causal Inference": [r"causal", r"treatment effect", r"counterfactual", r"confound", r"uplift"],
 "Time Series & Spatiotemporal": [r"time series", r"spatio[- ]?temporal", r"traffic", r"mobility", r"trajectory", r"forecast", r"urban comput"],
 "Text Mining & NLP": [r"text mining", r"sentiment", r"topic model", r"named entity", r"text classif", r"summariz", r"question answer", r"\bnlp\b"],
 "Multimodal & Vision-Language": [r"multimodal", r"vision[- ]?language", r"image[- ]?text", r"cross[- ]?modal", r"\bvlm\b", r"visual question"],
 "Self-Supervised & Contrastive": [r"self[- ]?supervis", r"contrastive", r"pre[- ]?train", r"representation learning", r"\bssl\b"],
 "Generative & Diffusion": [r"diffusion model", r"generative", r"\bgan\b", r"variational autoencoder", r"flow[- ]?based", r"synthesis"],
 "Explainability & Interpretability": [r"explainab", r"interpretab", r"\bxai\b", r"attribution", r"saliency", r"transparen"],
 "Efficiency & Scalability": [r"efficient", r"scalab", r"acceleration", r"distill", r"compress", r"lightweight", r"real[- ]?time", r"latency", r"quantiz", r"pruning"],
 "Advertising & E-commerce": [r"advertis", r"\bads\b", r"auction", r"bidding", r"e[- ]?commerce", r"marketplace", r"pricing", r"revenue"],
 "Reinforcement Learning": [r"reinforcement learning", r"\brl\b", r"bandit", r"policy gradient", r"reward"],
}
COMPILED = {t: [re.compile(p, re.I) for p in pats] for t, pats in THEMES.items()}

def themes_of(text):
    return [t for t, pats in COMPILED.items() if any(p.search(text) for p in pats)]

all_papers = []
per_venue = {}
for label, fn in FILES:
    path = os.path.join(HERE, "data", fn)
    if not os.path.exists(path):
        print("skip missing", fn); continue
    d = json.load(open(path)); ps = d["papers"]
    per_venue[label] = len(ps)
    for p in ps:
        p["venue"] = label
        text = (p["title"] + " " + (p["abstract"] or "")).lower()
        p["themes"] = themes_of(text)
        all_papers.append(p)

N = len(all_papers)
theme_counts = Counter()
theme_venue = defaultdict(lambda: Counter())
theme_examples = defaultdict(list)
for p in all_papers:
    for t in p["themes"]:
        theme_counts[t] += 1
        theme_venue[t][p["venue"]] += 1
        if len(theme_examples[t]) < 6:
            theme_examples[t].append({"title": p["title"], "venue": p["venue"]})
uncat = sum(1 for p in all_papers if not p["themes"])

OUT = {
 "venues": per_venue, "n_papers": N,
 "with_abstract": sum(1 for p in all_papers if p["abstract"]),
 "n_uncategorized": uncat,
 "multi_theme": sum(1 for p in all_papers if len(p["themes"]) > 1),
 "themes": [{"theme": t, "n": n, "pct": round(n*100/N, 1),
             "by_venue": dict(theme_venue[t]), "examples": theme_examples[t]}
            for t, n in theme_counts.most_common()],
}
json.dump(OUT, open(os.path.join(HERE, "data", "themes.json"), "w"), indent=1)
print(f"{N} papers ({per_venue}) · {uncat} uncategorized")
for t, n in theme_counts.most_common():
    bv = " ".join(f"{v.split()[0]}:{c}" for v, c in theme_venue[t].items())
    print(f"  {n:>4} ({n*100//N:>2}%)  {t:<34} [{bv}]")
print("wrote data/themes.json")
