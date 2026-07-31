# -*- coding: utf-8 -*-
"""
Build the first-principles "deep read" of Data Mining 2026: how the field connects
people to information — from organizing what's known, through search and recommendation,
to language-model-based answering, all guarded against fraud and fairness failures,
all run at scale. Plain-language framing (written here), every paper placed under its act
with its one-line contribution (from the LLM analysis). No jargon in the framing.
"""
import json, os, re, html
from subtheme_framing import FRAMING
HERE = os.path.dirname(os.path.abspath(__file__))

# Load analysis and raw papers, join abstracts
analysis = json.load(open(os.path.join(HERE, "data", "analysis.json")))["papers"]
PLAIN = json.load(open(os.path.join(HERE, "data", "plain.json"))) if os.path.exists(os.path.join(HERE, "data", "plain.json")) else {}
RICH = json.load(open(os.path.join(HERE, "data", "rich.json"))) if os.path.exists(os.path.join(HERE, "data", "rich.json")) else {}

def story_html(gid):
    r = RICH.get(str(gid))
    if not r: return ""
    parts = [("bp", "the big picture"), ("wh", "why it's hard"), ("ap", "what they do"),
             ("ww", "why it works"), ("po", "the payoff")]
    secs = "".join(f"<div class='sec {k}'><span class='lbl'>{lbl}</span><p>{esc(r.get(k))}</p></div>"
                   for k, lbl in parts if r.get(k))
    return f"<details class='story'><summary>read the full first-principles story</summary>{secs}</details>"
papers_raw = []
for fn in ["www-2026-papers.json", "wsdm-2026-papers.json", "sigir-2026-papers.json"]:
    path = os.path.join(HERE, "data", fn)
    if os.path.exists(path):
        papers_raw.extend(json.load(open(path))["papers"])

def esc(s): return html.escape(str(s or ""))

# join analysis (problem/approach/contribution) with abstract by title
abst = {p["title"].lower(): (p.get("abstract") or "") for p in papers_raw}
for a in analysis:
    a["abstract"] = abst.get(a["title"].lower(), "")

# theme taxonomy (same as mine_themes) — assign each paper one theme
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
C = {t: [re.compile(p, re.I) for p in pats] for t, pats in THEMES.items()}

PRIORITY = ["Fraud & Anomaly Detection","Misinformation & Trust","Recommender Systems","Advertising & E-commerce","Retrieval-Augmented (RAG)","LLM Agents & Tool Use","Information Retrieval & Search","Knowledge Graphs","Social Networks & Influence","Time Series & Spatiotemporal","Graph Learning & Mining","Multimodal & Vision-Language","Generative & Diffusion","Text Mining & NLP","Self-Supervised & Contrastive","LLMs & Language Models","Causal Inference","Privacy, Federated & Security","Fairness, Bias & Responsible AI","Explainability & Interpretability","Reinforcement Learning","Efficiency & Scalability"]

def theme_of(a):
    text = (a["title"] + " " + a["abstract"]).lower()
    for t in PRIORITY:
        if any(x.search(text) for x in C[t]):
            return t
    return "Other"

for a in analysis:
    a["theme"] = theme_of(a)

# ---- the six acts, with plain-language framing --------------
ACTS = [
 {"n": "I", "title": "Organize what's known",
  "themes": ["Graph Learning & Mining","Knowledge Graphs","Social Networks & Influence","Time Series & Spatiotemporal","Self-Supervised & Contrastive"],
  "problem": "The web isn't a library with a tidy catalog; it's a churning, unlabeled tangle — billions of pages, clicks, purchases, and connections, with no built-in structure. Before you can find or recommend or reason about any of it, you have to turn that mess into something a computer can work with: a map of what exists and how it all connects. The hard part is that the connections <em>are</em> the meaning — who links to whom, what's bought with what, which fact relates to which — and there are far too many to write down by hand.",
  "approach": "Represent everything as relationships. Store the world as a giant web of things and the links between them, and learn a compact string of numbers for each item so that similar things end up near each other. Special care goes to the shape of the connections themselves — friend networks, webs of facts — because how things are wired together carries as much meaning as the things being wired."},
 {"n": "II", "title": "Find the needle",
  "themes": ["Information Retrieval & Search"],
  "problem": "Once the world is organized, the everyday act is search: a person has a need, and somewhere in billions of items sit the few that answer it. This is harder than it sounds — the words a person uses rarely match the words in the answer, what counts as relevant depends on who's asking, and the whole thing has to come back in a fraction of a second.",
  "approach": "Match by meaning, not just by words: turn both the question and every candidate into those number-strings and find the nearest ones, then carefully re-order the survivors so the best rises to the top. Much of this year's work is making that matching sharper and the ordering fairer and faster."},
 {"n": "III", "title": "Anticipate the want",
  "themes": ["Recommender Systems","Advertising & E-commerce"],
  "problem": "Often people don't search at all — they scroll, and expect the right thing to already be there. The system has to guess what someone wants before they ask, using nothing but their past behavior and everyone else's. Guess well and it feels like magic; guess badly and it's noise — and it must keep working for brand-new people and brand-new items it has never seen before.",
  "approach": "Learn from the crowd — if people like you liked something, you probably will too — and increasingly from the order and timing of what each person did, to catch a shifting mood. This is where the field touches the business of the web most directly: the same machinery that recommends what to watch also places the ads that pay for it."},
 {"n": "IV", "title": "Understand and answer",
  "themes": ["LLMs & Language Models","LLM Agents & Tool Use","Retrieval-Augmented (RAG)","Text Mining & NLP","Generative & Diffusion","Multimodal & Vision-Language"],
  "problem": "For decades these systems handed back a list of links and left the understanding to you. The new expectation is that the machine reads your need in plain language, reasons about it, and returns an actual <em>answer</em> — drawn from the organized world, and correct. That asks for something the field didn't used to have: real command of language, and a way to keep the answer tied to fact rather than confidently made up.",
  "approach": "This is where large language models — systems trained on enormous amounts of text that can read and write fluently — have swept in, and they now reach into nearly every corner of the field. The main trick for keeping them honest is to let them look things up first and answer only from what they found; the frontier is chaining several such steps into systems that plan and act on their own. (The look-it-up-first pattern is called retrieval-augmented generation; the act-on-their-own systems, agents.)"},
 {"n": "V", "title": "Guard the commons",
  "themes": ["Fairness, Bias & Responsible AI","Privacy, Federated & Security","Misinformation & Trust","Fraud & Anomaly Detection","Explainability & Interpretability","Causal Inference"],
  "problem": "Everything above is powerful and consequential, and the web is adversarial. The same systems that recommend and answer can also discriminate, leak private data, spread lies, or be gamed by fraudsters — and when a system decides who sees what, being unfair or wrong has real human cost. A field that shapes what billions of people read can't only ask does it work; it has to ask is it fair, private, honest, and safe.",
  "approach": "A whole counter-current of the research is defensive: catching fraud and coordinated abuse, spotting false information, protecting privacy (including learning from data without ever gathering it all in one place), measuring and removing unfair bias, and making a system's decisions clear enough to trust. A related thread asks not just what <em>predicts</em> an outcome but what actually <em>causes</em> it — the difference between a coincidence and a lever you can safely pull."},
 {"n": "VI", "title": "Do it at scale",
  "themes": ["Efficiency & Scalability","Reinforcement Learning"],
  "problem": "None of this matters if it can't run for billions of people, on real machines, right now. A method that's accurate but too slow or too heavy to deploy is a paper, not a product — and the newest language models are enormous. So a constant pressure runs underneath everything: make it smaller, faster, cheaper, without losing what made it good.",
  "approach": "Shrink and speed up — compress big models, teach small ones to imitate large ones, cut the work each request costs — and build systems that spread across many machines. It's the least glamorous stage and the one that decides whether any of the rest ever reaches a person."},
]

def paper_row(a):
    venue = a.get("venue", "").replace("TheWebConf", "WWW").split()[0]
    venue_tag = f"<span class='vt {esc(venue)}'>{esc(venue)}</span>"
    pl = PLAIN.get(str(a.get("gid")))
    if pl:
        body = (f"<div class='ppa'><span class='pk'>problem</span> {esc(pl['p'])}</div>"
                f"<div class='ppa'><span class='pk ap'>approach</span> {esc(pl['a'])}</div>")
    else:
        body = f"<div class='pc'>{esc(a.get('contribution') or a.get('problem') or '')}</div>"
    return f"<div class='pr'><div class='pt'>{esc(a['title'])}</div>{venue_tag}{body}{story_html(a.get('gid'))}</div>"

placed = set()
def act_papers(themes):
    rows = []
    for t in themes:
        group = [a for a in analysis if a["theme"] == t and a["title"] not in placed]
        if not group: continue
        for a in group: placed.add(a["title"])
        rows.append((t, group))
    return rows

def act_html(act):
    groups = act_papers(act["themes"])
    ncount = sum(len(g) for _, g in groups)
    inner = ""
    for t, group in groups:
        inner += f"<div class='sub'>{esc(t)} <span class='sn'>{len(group)}</span></div>"
        fr = FRAMING.get(t)
        if fr:
            inner += f"<p class='subframe'><b>Problem.</b> {fr[0]} <b>Approach.</b> {fr[1]}</p>"
        inner += "".join(paper_row(a) for a in group)
    return f"""<section id="act{act['n']}">
  <div class="anum">Stage {act['n']} · {ncount} papers</div>
  <h2>{esc(act['title'])}</h2>
  <p class="prob"><b>The problem.</b> {act['problem']}</p>
  <p class="appr"><b>The approach.</b> {act['approach']}</p>
  <div class="papers">{inner}</div>
</section>"""

acts_rendered = "".join(act_html(a) for a in ACTS)
# any leftover (Other / themes not in an act)
leftover = [a for a in analysis if a["title"] not in placed]
if leftover:
    rows = "".join(paper_row(a) for a in leftover)
    acts_rendered += f"""<section><div class="anum">Also · {len(leftover)} papers</div>
    <h2>Everything else</h2><p class="prob">Papers that sit across or between the stages above — the field's long tail.</p>
    <div class="papers">{rows}</div></section>"""

toc = "".join(f"<a href='#act{a['n']}'><b>{a['n']}.</b> {esc(a['title'])}</a>" for a in ACTS)

P = f"""<meta charset="utf-8">
<title>Data Mining 2026 · the deep read</title>
<style>
:root{{--bg:#0E1420;--bg2:#141D2C;--ink:#EAEEF4;--soft:#B4BFD0;--dim:#8493A8;--faint:#5A6577;--line:rgba(150,170,205,.14);--accent:#4FA8B8;--amber:#E3A63A;--rose:#E0748A;--viol:#9B8CE0;--serif:"Iowan Old Style",Palatino,Georgia,serif;--sans:-apple-system,system-ui,"Segoe UI",Roboto,Arial,sans-serif;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.75;font-size:17px}}
.wrap{{max-width:820px;margin:0 auto;padding:0 24px}}
p{{color:var(--soft);margin:0 0 16px}}b{{color:var(--ink)}}em{{color:#fff;font-style:italic}}.mono{{font-family:var(--mono)}}a{{color:var(--accent)}}
.kick{{font-family:var(--mono);font-size:11.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--accent);padding-top:56px}}
h1{{font-family:var(--serif);font-size:clamp(32px,6vw,52px);line-height:1.05;margin:12px 0 0;color:#fff;letter-spacing:-.02em}}
.dek{{font-size:20px;color:var(--soft);margin-top:18px;max-width:64ch;font-family:var(--serif);line-height:1.5}}
.lead{{font-family:var(--serif);font-size:21px;line-height:1.5;color:#fff;margin:18px 0}}
section{{padding:44px 0;border-top:1px solid var(--line)}}
.anum{{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);margin-bottom:6px}}
h2{{font-family:var(--serif);font-size:30px;margin:0 0 14px;color:#fff}}
.prob,.appr{{font-size:16.5px}}
.toc{{font-family:var(--mono);font-size:13px;color:var(--dim);margin:22px 0 0;line-height:2}}.toc a{{color:var(--soft);text-decoration:none;display:block}}.toc a:hover{{color:var(--accent)}}.toc b{{color:var(--accent);font-weight:400}}
.papers{{margin-top:20px}}
.sub{{font-family:var(--mono);font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:var(--amber);margin:22px 0 8px;border-bottom:1px solid var(--line);padding-bottom:5px}}.sub .sn{{color:var(--faint);margin-left:4px}}
.subframe{{font-size:14.5px;color:var(--soft);margin:0 0 12px;padding:10px 14px;background:var(--bg2);border:1px solid var(--line);border-left:2px solid var(--amber);border-radius:9px}}.subframe b{{color:var(--amber);font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;text-transform:uppercase}}
.pr{{padding:9px 0;border-bottom:1px solid rgba(150,170,205,.07);display:flex;flex-wrap:wrap;align-items:baseline;gap:8px}}
.pt{{font-family:var(--serif);font-size:16.5px;color:#fff;line-height:1.3;flex:1 1 auto}}
.vt{{font-family:var(--mono);font-size:9.5px;letter-spacing:.05em;color:#fff;background:var(--accent);border-radius:4px;padding:2px 6px;flex:0 0 auto;text-transform:uppercase}}
.vt.WWW{{background:var(--accent)}}
.vt.WSDM{{background:var(--viol)}}
.vt.SIGIR{{background:var(--amber)}}
.pc{{font-size:14px;color:var(--soft);flex:1 1 100%}}
.ppa{{font-size:13.5px;color:var(--soft);margin-top:3px;padding-left:70px;text-indent:-70px;line-height:1.5;flex:1 1 100%}}
.pk{{display:inline-block;width:62px;font-family:var(--mono);font-size:9.5px;letter-spacing:.05em;text-transform:uppercase;color:var(--rose);text-align:right;margin-right:8px}}.pk.ap{{color:var(--accent)}}
.pm{{font-family:var(--mono);font-size:11px;color:var(--faint);flex:1 1 100%}}
.story{{flex:1 1 100%;margin-top:5px}}
.story>summary{{font-family:var(--mono);font-size:10.5px;letter-spacing:.04em;color:var(--accent);cursor:pointer;list-style:none;padding:2px 0}}
.story>summary::-webkit-details-marker{{display:none}}
.story>summary::before{{content:"▸ ";color:var(--accent)}}.story[open]>summary::before{{content:"▾ "}}.story[open]>summary{{color:var(--dim)}}
.story .sec{{margin:9px 0 9px 8px;padding-left:12px;border-left:1px solid var(--line)}}
.story .sec .lbl{{font-family:var(--mono);font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;display:block;margin-bottom:2px}}
.story .sec.bp .lbl{{color:var(--accent)}}.story .sec.wh .lbl{{color:var(--rose)}}.story .sec.ap .lbl{{color:var(--viol)}}.story .sec.ww .lbl{{color:var(--amber)}}.story .sec.po .lbl{{color:#6FCF97}}
.story .sec p{{margin:0;color:var(--ink);font-size:13.5px;line-height:1.6}}
.aha{{font-family:var(--serif);font-size:23px;line-height:1.45;color:#fff;border-left:3px solid var(--accent);padding-left:20px;margin:14px 0}}
.src{{font-family:var(--mono);font-size:12px;color:var(--faint);margin-top:28px;padding-top:16px;border-top:1px solid var(--line)}}
</style>
<div class="wrap">
<header style="padding:0 0 8px">
  <div class="kick">Data mining 2026 · the deep read · first principles</div>
  <h1>From a tangled web to one true answer.</h1>
  <p class="dek">All {len(analysis)} technical papers of WWW, WSDM and SIGIR 2026, arranged not as a list of topics but as one story — the journey the field takes to connect a person to information, from organizing the raw chaos, through search and recommendation, to language models that read and answer, all while guarding against fraud, bias, and lies, and making it all run for billions at once.</p>
  <p class="lead">How do you connect a person to the right information — and, increasingly, the right <em>answer</em> — out of a web too vast to read and too unreliable to trust?</p>
  <p>That's the whole of data mining and web information systems on one line. Everything below is a piece of the answer. The field has six jobs: first it must <em>organize</em> what exists into something machine-readable; then it must handle the daily acts of <em>search</em> and <em>recommendation</em>; increasingly it <em>understands</em> and <em>answers</em> in natural language; it has to <em>guard</em> against abuse, fraud, bias, and misinformation; and it must do all of this <em>at scale</em>. Six stages, one pipeline — and this year, a single new thread (large language models, in all their forms) running through nearly every one.</p>
  <div class="toc">{toc}</div>
</header>
{acts_rendered}
<section>
  <div class="anum">Connecting the dots</div>
  <h2>One pipeline, one layer</h2>
  <p>Lay the six stages end to end and the whole conference is a single pipeline: the field has to <b>organize</b> the world's information, then handle the everyday acts of <b>search</b> and <b>recommendation</b>, increasingly <b>understand</b> and <b>answer</b> in natural language, <b>guard</b> against the adversaries, and do all of it <b>at scale</b>. Each stage exists because the one before it left a problem unsolved — you can't search or recommend what you haven't organized, you can't answer before you've searched, you can't trust an answer that isn't defended.</p>
  <p>And one change cuts across all six. The oldest data-mining systems were built from explicit rules and hand-tuned statistics — if this pattern appears, do that. Over the last decade, that layer was replaced by learned representations: we stopped writing rules and started teaching systems to learn patterns from examples. This year, one tool shows up in every stage: large language models, systems trained on enormous text that can read, reason, and write fluently. They now touch search, recommendation, entities, graphs, generation, defense, and cost. The single most-common research move across these {len(analysis)} papers is to ask: "what if we let an LLM see this problem?"</p>
  <p class="aha">Data mining has always been the art of connecting a person to information they need out of too much information they don't. Its 2026 turn is the same art learning to read fluently and answer directly — statistics and search and the shapes of graphs still at the core, but a machine that increasingly understands language and can reason about what it finds.</p>
  <p class="src">All {len(analysis)} WWW, WSDM, and SIGIR 2026 technical papers (from official proceedings; {sum(1 for a in analysis if a.get('abstract'))*100//len(analysis)}% with abstracts), each read for its contribution by a language model; stages and framing written from first principles. Browse/search them in the <a href="explorer.html">explorer</a> · overview in the <a href="index.html">landscape</a> · see how the <a href="compare.html">venues differ</a>.</p>
</section>
</div>
"""
open(os.path.join(HERE, "site", "deep.html"), "w", encoding="utf-8").write(P)
placed_n = len(placed) + len(leftover)
print("wrote site/deep.html ·", len(P)//1024, "KB · placed:", placed_n, "of", len(analysis), "· FFFD:", P.count(chr(0xFFFD)))
