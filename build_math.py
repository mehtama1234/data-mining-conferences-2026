# -*- coding: utf-8 -*-
"""The mathematics of data mining, from first principles: the recurring mathematical
ideas across WWW/WSDM/SIGIR 2026, each with a plain 'what it is' and a deep 'why it
works', and every paper placed under the idea it leans on with its own math + why."""
import json, os, html
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
MATH = json.load(open(os.path.join(HERE, "data", "math.json")))
_wm = os.path.join(HERE, "data", "whymath.json")
WHYMATH = json.load(open(_wm)) if os.path.exists(_wm) else {}
_dw = os.path.join(HERE, "data", "deepwhy.json")
DEEPWHY = json.load(open(_dw)) if os.path.exists(_dw) else {}
_rc = os.path.join(HERE, "data", "rich.json")
RICH = json.load(open(_rc)) if os.path.exists(_rc) else {}
_cr = os.path.join(HERE, "data", "concepts_rich.json")
CONCEPTS = json.load(open(_cr)) if os.path.exists(_cr) else {}
_sy = os.path.join(HERE, "data", "synth_out.json")
SYNTH = json.load(open(_sy)) if os.path.exists(_sy) else {}
_fr = os.path.join(HERE, "data", "families_rich.json")
FAMILIES = json.load(open(_fr)) if os.path.exists(_fr) else {}
_fm = os.path.join(HERE, "data", "family_manifest.json")
FAMILY_MANIFEST = json.load(open(_fm)) if os.path.exists(_fm) else {"families": []}
analysis = json.load(open(os.path.join(HERE, "data", "analysis.json")))["papers"]
def esc(s): return html.escape(str(s or ""))

def story_html(gid):
    r = RICH.get(str(gid))
    if not r: return ""
    parts = [("bp","the big picture"),("wh","why it's hard"),("naive","the naive solution"),
             ("ap","the core idea"),("mech","how the mechanism runs"),
             ("math","mathematical concepts"),("dots","connecting the dots"),
             ("ww","why it works"),("po","the payoff"),("limits","limits and assumptions")]
    secs = "".join(f"<div class='sec {k}'><span class='lbl'>{lbl}</span><p>{esc(r.get(k))}</p></div>"
                   for k,lbl in parts if r.get(k))
    return f"<details class='story'><summary>the full first-principles story</summary>{secs}</details>"
title_of = {str(a.get("gid")): a["title"] for a in analysis}
venue_of = {str(a.get("gid")): a.get("venue","").replace("TheWebConf","WWW").split()[0] for a in analysis}

CG = [
 {"key":"matching","title":"Matching and allocating who gets what",
  "tags":["matching and allocating who gets what","combining many weak signals into a strong one"],
  "intro":"The web constantly has to decide who gets what — which ad, which item, which slot — often through auctions and assignments that must balance many parties at once.",
  "why":"It works because these allocation problems have a well-defined best arrangement — the one creating the most total value while respecting everyone's limits — and there are honest rules (like charging each winner the right price) that make each party's own best move also the move that leads there. The math lines the incentives up with the outcome."},
 {"key":"cause","title":"Separating cause from coincidence",
  "tags":["separating cause from coincidence"],
  "intro":"Data is full of things that merely happen together, but to act well you need what actually causes an outcome — the lever you can pull, not the coincidence you happened to notice.",
  "why":"It works because if you can compare like with like — the same kind of person with and without the one thing you changed — then any leftover difference in outcome must be due to that change, not to who they already were. That careful comparison is exactly what turns a correlation into a cause you can safely act on."},
 {"key":"information","title":"Measuring surprise and information",
  "tags":["measuring surprise and information","measuring information"],
  "intro":"Underneath search and compression sits a way to measure how surprising an outcome is, and therefore how much information it carries — a rare event tells you a lot, a certain one tells you nothing.",
  "why":"It works because information has a natural, hard-to-cheat measure: the more unlikely a message, the more it narrows down the possibilities, and the fewer bits you need on average to send common things and more for rare ones. Systems that spend effort in proportion to surprise put their attention exactly where the uncertainty — and the payoff — actually is."},
 {"key":"network","title":"Spreading information across a network",
  "tags":["spreading information across a network"],
  "intro":"When the data is a web of connections — who follows whom, what's bought with what, which fact links to which — a thing's meaning comes largely from its neighbours, so you let evidence flow along the links.",
  "why":"It works because in real networks connected things tend to be alike — friends share tastes, linked pages share topics — so a node can borrow evidence from its neighbours, and letting that evidence spread a few steps sharpens every guess using the crowd around it. It only fails when the links carry no real signal."},
 {"key":"similarity","title":"Turning meaning into nearness",
  "tags":["measuring similarity as nearness in a space","keeping only the few dimensions that matter","grouping similar things together"],
  "intro":"A great deal of this field begins by placing every item — a word, a product, a person — as a point in a space, arranged so that things people treat as alike sit close together. Meaning becomes geometry.",
  "why":"It works because once similar things are placed near each other, the vague question 'what is like this?' becomes the precise, cheap question 'what is nearby?' — and nearness is easy to measure and behaves sensibly. The deeper trick it exploits: relationships too tangled to define by hand turn into simple distances once the layout is learned well, and only a few directions in that space usually carry the real meaning."},
 {"key":"rank","title":"Ranking by a learned score",
  "tags":["ranking things by a learned score"],
  "intro":"Search, recommendation, and advertising all come down to the same act: give every candidate a score for how well it fits the moment, then sort and show the top few.",
  "why":"It works because you almost never need the exact scores — only their order. A rough score that merely gets the ordering right already floats the best results to the top, so the real problem is far easier than pinning down a true number for every item, and small scoring errors that don't change the order don't matter at all."},
 {"key":"sequence","title":"Predicting what comes next",
  "tags":["predicting the next item in a sequence"],
  "intro":"Behaviour and language arrive as ordered streams — the pages you visited, the words in a sentence — and the useful move is to predict the next item from what came before.",
  "why":"It works because the recent past genuinely constrains the near future: what you clicked last shapes what you'll click next, the last few words shape the next word. So a system that captures those local dependencies can predict well without holding the entire history in mind at once."},
 {"key":"probability","title":"Estimating chances from data",
  "tags":["estimating probabilities from data","smart random sampling and averaging"],
  "intro":"Much of the field is really estimating how likely something is — a click, a fraud, the next word — by learning those chances from mountains of past behaviour.",
  "why":"It works because with enough independent observations the fraction of times something happened is a trustworthy estimate of how often it will happen again — and the more you've seen, the tighter that estimate becomes. It also means a few well-chosen random samples can stand in for a huge population, because their average reliably reflects the whole."},
 {"key":"attention","title":"Focusing on what's relevant",
  "tags":["weighting the parts that are most relevant","weighing the parts that are most relevant"],
  "intro":"Not every part of an input matters equally, so the system learns to put its weight on the pieces relevant to the moment and quietly ignore the rest.",
  "why":"It works because in most inputs the useful signal is sparse — a few words, a few past actions carry the meaning — so a method that learns to weight those few heavily and downplay the rest keeps the signal and throws away the noise, doing far more with the same data."},
 {"key":"optimize","title":"Finding the least-wrong settings",
  "tags":["finding the settings with least error","following the slope downhill to improve","learning the settings with least error"],
  "intro":"Almost every learned system is tuned the same way: define a single number for how wrong it currently is, then adjust its internal settings to make that number as small as possible.",
  "why":"It works because the slope of how-wrong tells you exactly which small adjustment reduces the error, so nudging that way over and over can only improve, and it settles where no small change helps. When the error surface is bowl-shaped that settling point is the best possible; even when it is rugged, this reliably reaches a good one."},
 {"key":"learn","title":"Learning from examples and comparison",
  "tags":["learning a function from examples","learning by comparison of similar and different","learning from examples by resolving uncertainty"],
  "intro":"When the rule connecting input to output is too tangled to write down, you show the system many examples — or many pairs of what is similar and what is different — and let it settle on a rule that reproduces them.",
  "why":"It works because of a bargain between simplicity and coverage: when the true pattern is far simpler than the data and the examples cover the territory, a rule forced to fit them all has little room left to be wrong on new cases. Learning by comparison works because 'pull similar things together, push different ones apart' is enough to recover the hidden structure without anyone labelling it."},
]

placed = set(); groups = {c["key"]: [] for c in CG}
for gid, mv in MATH.items():
    tags = set(mv.get("tags") or [])
    for c in CG:
        if tags & set(c["tags"]):
            groups[c["key"]].append((gid, mv)); placed.add(gid); break

def concept_html(c):
    ps = groups[c["key"]]
    rows = ""
    for gid, mv in ps:
        why = WHYMATH.get(gid, ""); v = venue_of.get(gid, "")
        rows += (f"<div class='pr'><div class='pt'>{esc(title_of.get(gid,''))}<span class='vt {esc(v)}'>{esc(v)}</span></div>"
                 f"<div class='mp'><span class='pk'>uses</span> {esc(mv['plain'])}</div>"
                 + (f"<div class='mp wy'><span class='pk wk'>why it works</span> {esc(why)}</div>" if why else "")
                 + (f"<details class='dw'><summary>the deeper reason</summary><div class='dwb'>{esc(DEEPWHY.get(gid,''))}</div></details>" if DEEPWHY.get(gid) else "")
                 + story_html(gid)
                 + "</div>")
    cr = CONCEPTS.get(c["key"])
    if cr and cr.get("idea"):
        head = (f"<p class='intro'>{esc(cr['idea'])}</p>"
                f"<div class='whybox'><div class='wt'>Why it works — the principle</div><p>{esc(cr.get('why') or c['why'])}</p></div>"
                + (f"<div class='mathbox'><div class='wt mt'>The mathematical principle</div><p>{esc(cr['math'])}</p></div>" if cr.get('math') else "")
                + (f"<div class='familybox'><div class='wt ft'>The paper family</div><p>{esc(cr['family'])}</p></div>" if cr.get('family') else "")
                + (f"<div class='dotsbox'><div class='wt dt'>Connecting the dots across these {len(ps)} papers</div><p>{esc(cr['dots'])}</p></div>" if cr.get('dots') else "")
                + (f"<div class='picture'><span class='pl'>picture it</span> {esc(cr['picture'])}</div>" if cr.get('picture') else ""))
    else:
        head = (f"<p class='intro'>{c['intro']}</p>"
                f"<div class='whybox'><div class='wt'>Why it works — the principle</div><p>{esc(c['why'])}</p></div>")
    return (f"<section><div class='anum'>{len(ps)} papers</div><h2>{esc(c['title'])}</h2>"
            f"{head}<div class='papers'>{rows}</div></section>")

concepts_html = "".join(concept_html(c) for c in CG if groups[c["key"]])

def family_html(item):
    key = item.get("key", "")
    fam = FAMILIES.get(key, {})
    if not fam:
        return ""
    return (
        "<details class='fam'>"
        f"<summary><span>{esc(item.get('theme', key))}</span></summary>"
        f"<div class='familybox'><div class='wt ft'>the shared problem shape</div><p>{esc(fam.get('problem_shape'))}</p></div>"
        f"<div class='mathbox'><div class='wt mt'>the mathematical principle</div><p>{esc(fam.get('mathematical_principle'))}</p></div>"
        f"<div class='whybox'><div class='wt'>why this math matters</div><p>{esc(fam.get('why_math_matters'))}</p></div>"
        f"<div class='dotsbox'><div class='wt dt'>how the papers in this family differ</div><p>{esc(fam.get('paper_family'))}</p></div>"
        f"<div class='familybox'><div class='wt ft'>what changed in 2026</div><p>{esc(fam.get('what_changed'))}</p></div>"
        f"<div class='whybox lim'><div class='wt'>limits and assumptions</div><p>{esc(fam.get('limits'))}</p></div>"
        "</details>"
    )

families_html = "".join(family_html(f) for f in FAMILY_MANIFEST.get("families", []))

def _mb(s):  # escape, then render **bold** -> <b> and *italic* -> <i>
    s = esc(s)
    parts = s.split("**")
    s = "".join(p if i % 2 == 0 else f"<b>{p}</b>" for i, p in enumerate(parts))
    parts = s.split("*")
    return "".join(p if i % 2 == 0 else f"<i>{p}</i>" for i, p in enumerate(parts))

synth_block = ""
if SYNTH.get("thread"):
    synth_block = (
        "<section class='synth'>"
        "<div class='anum'>the whole field in one page</div>"
        "<h2>A few ideas, one machine</h2>"
        f"<p class='synth-thread'>{_mb(SYNTH['thread'])}</p>"
        f"<div class='dotsbox'><div class='wt dt'>how the ideas fit together</div><p>{_mb(SYNTH['arc'])}</p></div>"
        f"<p class='aha'>{_mb(SYNTH['punchline'])}</p>"
        "</section>")
NA = len(MATH)
tc = Counter(t for v in MATH.values() for t in v["tags"])
bars = "".join(f"<div class='bar'><span class='bl'>{esc(t)}</span><span class='bt'><span class='bf' style='width:{n/tc.most_common(1)[0][1]*100:.0f}%'></span></span><span class='bv'>{n}</span></div>" for t,n in tc.most_common())

P = f"""<meta charset="utf-8">
<title>Data mining 2026 · the mathematics, and why it works</title>
<style>
:root{{--bg:#0E1420;--bg2:#141D2C;--ink:#EAEEF4;--soft:#B4BFD0;--dim:#8493A8;--faint:#5A6577;--line:rgba(150,170,205,.14);--accent:#4FA8B8;--amber:#E3A63A;--rose:#E0748A;--viol:#9B8CE0;--serif:"Iowan Old Style",Palatino,Georgia,serif;--sans:-apple-system,system-ui,"Segoe UI",Roboto,Arial,sans-serif;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.75;font-size:17px}}
.wrap{{max-width:820px;margin:0 auto;padding:0 24px}}
p{{color:var(--soft);margin:0 0 16px}}b{{color:var(--ink)}}em{{color:#fff;font-style:italic}}a{{color:var(--accent)}}
.kick{{font-family:var(--mono);font-size:11.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--accent);padding-top:56px}}
h1{{font-family:var(--serif);font-size:clamp(32px,6vw,52px);line-height:1.05;margin:12px 0 0;color:#fff;letter-spacing:-.02em}}
.dek{{font-size:20px;color:var(--soft);margin-top:18px;max-width:64ch;font-family:var(--serif);line-height:1.5}}
.lead{{font-family:var(--serif);font-size:21px;line-height:1.5;color:#fff;margin:18px 0}}
section{{padding:44px 0;border-top:1px solid var(--line)}}
.anum{{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);margin-bottom:6px}}
h2{{font-family:var(--serif);font-size:29px;margin:0 0 12px;color:#fff}}
.intro{{font-size:16.5px}}
.whybox{{background:var(--bg2);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:12px;padding:14px 18px;margin:6px 0 4px}}
.whybox .wt{{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin-bottom:6px}}.whybox p{{margin:0;font-size:15.5px;color:var(--ink)}}
.mathbox{{background:var(--bg2);border:1px solid var(--line);border-left:3px solid #D8BE5F;border-radius:12px;padding:14px 18px;margin:6px 0 4px}}
.mathbox .wt.mt{{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#D8BE5F;margin-bottom:6px}}.mathbox p{{margin:0;font-size:15.5px;color:var(--ink)}}
.familybox{{background:var(--bg2);border:1px solid var(--line);border-left:3px solid #7EC7D8;border-radius:12px;padding:14px 18px;margin:6px 0 4px}}
.familybox .wt.ft{{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#7EC7D8;margin-bottom:6px}}.familybox p{{margin:0;font-size:15.5px;color:var(--ink)}}
.dotsbox{{background:var(--bg2);border:1px solid var(--line);border-left:3px solid var(--viol);border-radius:12px;padding:14px 18px;margin:6px 0 4px}}
.dotsbox .wt.dt{{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--viol);margin-bottom:6px}}.dotsbox p{{margin:0;font-size:15.5px;color:var(--ink)}}
.picture{{font-size:15px;color:var(--soft);font-style:italic;margin:8px 0 4px;padding-left:14px;border-left:2px solid var(--amber)}}
.picture .pl{{font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--amber);font-style:normal;margin-right:8px}}
.fam{{border:1px solid var(--line);border-radius:10px;margin:10px 0;background:rgba(150,170,205,.025);overflow:hidden}}
.fam summary{{cursor:pointer;list-style:none;padding:12px 16px;font-family:var(--serif);font-size:18px;color:#fff}}
.fam summary::-webkit-details-marker{{display:none}}.fam summary::before{{content:'▸ ';font-family:var(--mono);color:var(--accent)}}.fam[open] summary::before{{content:'▾ '}}
.fam .whybox,.fam .mathbox,.fam .familybox,.fam .dotsbox{{margin:8px 14px 12px}}
.fam .lim{{border-left-color:#A7B0BF}}
.synth{{background:linear-gradient(180deg,rgba(79,168,184,.06),rgba(79,168,184,0));border:1px solid var(--line);border-radius:16px;padding:22px 24px;margin:8px 0 30px}}
.synth h2{{margin:2px 0 12px}}
.synth-thread{{font-size:17px;color:var(--ink);line-height:1.6}}
.papers{{margin-top:16px}}
.pr{{padding:10px 0;border-bottom:1px solid rgba(150,170,205,.06)}}
.pt{{font-family:var(--serif);font-size:15.5px;color:#fff}}
.vt{{font-family:var(--mono);font-size:9px;color:#0E1420;background:var(--accent);border-radius:4px;padding:1px 5px;margin-left:6px;vertical-align:1px}}.vt.WSDM{{background:var(--viol)}}.vt.SIGIR{{background:var(--amber)}}
.mp{{font-size:13.5px;color:var(--dim);margin-top:3px;padding-left:82px;text-indent:-82px}}.mp.wy{{color:var(--soft)}}
.pk{{display:inline-block;width:74px;font-family:var(--mono);font-size:9px;letter-spacing:.04em;text-transform:uppercase;color:var(--faint);text-align:right;margin-right:8px}}.pk.wk{{color:var(--accent)}}
.dw{{margin:5px 0 0 82px}}.dw summary{{font-family:var(--mono);font-size:10.5px;letter-spacing:.03em;color:var(--accent);cursor:pointer;list-style:none}}.dw summary::-webkit-details-marker{{display:none}}.dw summary::before{{content:'▸ ';color:var(--faint)}}.dw[open] summary::before{{content:'▾ '}}
.dwb{{font-size:13.5px;color:var(--soft);margin-top:6px;padding:10px 14px;background:rgba(79,168,184,.05);border-left:2px solid var(--line);border-radius:0 8px 8px 0;line-height:1.6}}
.story{{margin:5px 0 0 82px}}.story>summary{{font-family:var(--mono);font-size:10.5px;letter-spacing:.03em;color:var(--accent);cursor:pointer;list-style:none}}.story>summary::-webkit-details-marker{{display:none}}.story>summary::before{{content:'▸ ';color:var(--faint)}}.story[open]>summary::before{{content:'▾ '}}
.story .sec{{margin:8px 0;padding-left:12px;border-left:1px solid var(--line)}}
.story .sec .lbl{{font-family:var(--mono);font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;display:block;margin-bottom:2px}}
.story .sec.bp .lbl{{color:var(--accent)}}.story .sec.wh .lbl{{color:var(--rose)}}.story .sec.naive .lbl{{color:#D38D63}}.story .sec.ap .lbl{{color:var(--viol)}}.story .sec.mech .lbl{{color:#7EC7D8}}.story .sec.math .lbl{{color:#D8BE5F}}.story .sec.dots .lbl{{color:#B69CF0}}.story .sec.ww .lbl{{color:var(--amber)}}.story .sec.po .lbl{{color:#6FCF97}}.story .sec.limits .lbl{{color:#A7B0BF}}
.story .sec p{{margin:0;color:var(--ink);font-size:13.5px;line-height:1.6}}
.bar{{display:flex;align-items:center;gap:12px;margin:5px 0;font-family:var(--mono);font-size:12px}}
.bl{{width:300px;color:var(--soft);text-align:right;flex:0 0 auto}}.bt{{flex:1;height:14px;background:rgba(150,170,205,.06);border-radius:4px;overflow:hidden}}.bf{{display:block;height:100%;background:#4FA8B8}}.bv{{width:40px;color:var(--ink)}}
@media(max-width:640px){{.bl{{width:150px;font-size:10.5px}}.mp{{padding-left:0;text-indent:0}}}}
.aha{{font-family:var(--serif);font-size:23px;line-height:1.45;color:#fff;border-left:3px solid var(--accent);padding-left:20px;margin:14px 0}}
.src{{font-family:var(--mono);font-size:12px;color:var(--faint);margin-top:28px;padding-top:16px;border-top:1px solid var(--line)}}
</style>
<div class="wrap">
<header style="padding:0 0 8px">
  <div class="kick">Data mining 2026 · the mathematics · why it works · first principles</div>
  <h1>A few ideas, and why they hold.</h1>
  <p class="dek">Search, recommendation, graphs, language, trust — the data-mining field looks like many problems. Underneath, nearly all of it runs on a short list of mathematical ideas. This is that list — and for each, not just <em>what</em> it is but <b>why it actually works</b>: the principle that makes it sound. Every 2026 paper is placed under the idea it leans on, with a plain note on the math it uses and why that math holds.</p>
  <p class="lead">How do you turn a person's want, and a web too vast to read, into numbers a computer can score, compare, and be right about?</p>
  <p>That is what all of this math is for. A search, a recommendation, a fraud check — each has to become a familiar mathematical question before a computer can answer it. Read the ideas below and you'll see the same handful recur across wildly different papers: turn meaning into nearness, rank by a rough score, estimate a chance from data, spread evidence across a network, focus on what's relevant, minimise how-wrong, and — increasingly — learn the rule from examples. And crucially, <em>why each one is trustworthy</em>, not just what it does.</p>
  <div style="margin-top:14px"><div style="font-family:var(--mono);font-size:11px;color:var(--faint);margin-bottom:8px">HOW OFTEN EACH IDEA APPEARS (across {NA} papers; a paper can use several)</div>{bars}</div>
</header>
{synth_block}
<section>
  <div class="anum">{len(FAMILY_MANIFEST.get('families', []))} paper families</div>
  <h2>The family map</h2>
  <p class="intro">The concept list below explains the reusable mathematical tools. The family map explains why papers that look different on the surface belong together. Each family is organized around a shared pressure: what the system is trying to connect, rank, explain, protect, retrieve, generate, or control; what the naive method gets wrong; and which mathematical principle makes the family work.</p>
  {families_html}
</section>
{concepts_html}
<section>
  <div class="anum">Connecting the dots</div>
  <h2>Different problems, the same few guarantees</h2>
  <p>Line the ideas up and the surprise is how few there are, and how each rests on a plain guarantee. Ranking works because only order matters. Similarity works because meaning becomes distance. Estimating chances works because averages of enough observations don't lie. Spreading across a network works because neighbours are alike. Minimising error works because a slope always points the way down. Different problems, the same handful of reasons to trust the answer.</p>
  <p>And one idea now runs through all the others: learning the rule from examples. But look closely and it doesn't replace the older math — it rides on it. A learned recommender still turns meaning into nearness and still ranks by a score; a learned language system still estimates chances and focuses on what's relevant. The 2026 story isn't that data mining stopped being mathematical — it's that a learned layer now sits on the same small, well-understood toolkit the field has always trusted.</p>
  <p class="aha">Every good answer this field gives is one of a few mathematical questions in disguise — what's nearest, what ranks highest, how likely, what actually causes it — and each is trusted for a reason you can state in a sentence. Know the few reasons and the whole field stops being magic.</p>
  <p class="src">Each paper's core mathematical idea and the reason it works were read from its abstract by a language model, named from a fixed plain vocabulary; the framing of each idea is written from first principles. See the papers in the <a href="deep.html">deep read</a> · the <a href="explorer.html">explorer</a> · the <a href="index.html">landscape</a> · venue characters in the <a href="compare.html">comparison</a>.</p>
</section>
</div>
"""
open(os.path.join(HERE, "site", "math.html"), "w", encoding="utf-8").write(P)
print("wrote site/math.html ·", len(P)//1024, "KB · placed:", len(placed), "of", NA, "· FFFD:", P.count("�"))
