import json, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
V = json.load(open(os.path.join(HERE, "data", "venue_profiles.json")))
def esc(s): return html.escape(str(s))
P_ = V["profiles"]

# hand-written character lines, grounded in the computed over-indexing
CHAR = {
 "WWW 2026": ("The whole web — and its dark side.",
   "The broadest venue, and the one that owns the web's adversarial edge: it over-indexes on trust &amp; safety — fraud, misinformation, privacy, security — and on the graph and federated methods used to police a web too big to trust."),
 "WSDM 2026": ("Small, sharp, methods-first.",
   "The most method-forward of the three: for its size it leans hard into causal inference, recommendation, and the newest generative tools (diffusion, reasoning) applied to search and mining — a venue that prizes technique over breadth."),
 "SIGIR 2026": ("Retrieval, through and through.",
   "The retrieval venue, unmistakably: ranking, retrieval-augmented generation, benchmarks and the distillation tricks that make search efficient. Where the other two roam the web, SIGIR stays focused on finding the right thing and returning it fast."),
}
COLOR = {"WWW 2026": "#4FA8B8", "WSDM 2026": "#9B8CE0", "SIGIR 2026": "#E3A63A"}

def liftbadges(items, key, col):
    return "".join(f"<span class='lb'>{esc(i[key])} <b style='color:{col}'>×{i['lift']}</b></span>" for i in items[:6])

def topthemes(p, col):
    mx = max((t["pct"] for t in p["top_themes"]), default=1)
    return "".join(f"<div class='mini-bar'><span class='mbl'>{esc(t['theme'])}</span>"
                   f"<span class='mbt'><span class='mbf' style='width:{t['pct']/mx*100:.0f}%;background:{col}'></span></span>"
                   f"<span class='mbv'>{t['pct']}%</span></div>" for t in p["top_themes"][:6])

def col(v):
    p = P_[v]; col = COLOR[v]; head, body = CHAR[v]
    return f"""<div class="vcol" style="border-top:3px solid {col}">
      <div class="vname">{esc(v.replace(' 2026',''))}</div>
      <div class="vn">{p['n_papers']} papers</div>
      <div class="vchar">{head}</div>
      <p class="vbody">{body}</p>
      <div class="vsec">over-indexes on — topics</div>
      <div class="lbs">{liftbadges(p['distinct_themes'],'theme',col)}</div>
      <div class="vsec">over-indexes on — techniques</div>
      <div class="lbs">{liftbadges(p['distinct_methods'],'tag',col)}</div>
      <div class="vsec">what it's mostly about</div>
      {topthemes(p, col)}
    </div>"""

HTML = f"""<meta charset="utf-8">
<title>Data Mining 2026 · three venues, three characters</title>
<style>
:root{{--bg:#0E1420;--bg2:#141D2C;--ink:#EAEEF4;--soft:#B4BFD0;--dim:#8493A8;--faint:#5A6577;
--line:rgba(150,170,205,.14);--accent:#4FA8B8;--amber:#E3A63A;--viol:#9B8CE0;--serif:"Iowan Old Style",Palatino,Georgia,serif;
--sans:-apple-system,system-ui,"Segoe UI",Roboto,Arial,sans-serif;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.6;font-size:16px}}
.wrap{{max-width:1040px;margin:0 auto;padding:0 22px 60px}}
a{{color:var(--accent);text-decoration:none}}
.kick{{font-family:var(--mono);font-size:11.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--accent);padding-top:56px}}
h1{{font-family:var(--serif);font-size:clamp(30px,5.5vw,48px);line-height:1.06;margin:12px 0 0;color:#fff}}
.dek{{font-size:18px;color:var(--soft);margin:16px 0 0;max-width:66ch}}
.sub{{font-family:var(--mono);font-size:12px;color:var(--dim);margin-top:10px}}
.cols{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-top:34px}}
@media(max-width:820px){{.cols{{grid-template-columns:1fr}}}}
.vcol{{background:var(--bg2);border:1px solid var(--line);border-radius:14px;padding:18px 18px 20px}}
.vname{{font-family:var(--serif);font-size:24px;color:#fff}}
.vn{{font-family:var(--mono);font-size:12px;color:var(--dim);margin-bottom:10px}}
.vchar{{font-family:var(--serif);font-size:18px;color:#fff;font-style:italic;margin-bottom:8px}}
.vbody{{font-size:14px;color:var(--soft);margin:0 0 14px}}
.vsec{{font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin:14px 0 7px}}
.lbs{{display:flex;flex-wrap:wrap;gap:6px}}
.lb{{font-family:var(--mono);font-size:11.5px;color:var(--soft);background:#0C1119;border:1px solid var(--line);border-radius:20px;padding:3px 9px}}
.mini-bar{{display:flex;align-items:center;gap:8px;margin:5px 0;font-family:var(--mono);font-size:11px}}
.mbl{{width:96px;color:var(--dim);text-align:right;flex:0 0 auto;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.mbt{{flex:1;height:12px;background:rgba(150,170,205,.06);border-radius:4px;overflow:hidden}}.mbf{{display:block;height:100%}}
.mbv{{width:34px;color:var(--soft)}}
.synth{{border-top:1px solid var(--line);margin-top:40px;padding-top:34px}}
.synth h2{{font-family:var(--serif);font-size:26px;color:#fff;margin:0 0 8px}}
.synth p{{color:var(--soft);margin:0 0 14px}}
.aha{{font-family:var(--serif);font-size:20px;line-height:1.4;color:#fff;border-left:3px solid var(--accent);padding-left:18px;margin:8px 0}}
.src{{font-family:var(--mono);font-size:12px;color:var(--faint);margin-top:26px;padding-top:16px;border-top:1px solid var(--line)}}
</style>
<div class="wrap">
  <div class="kick">Data-mining conferences 2026 · cross-venue</div>
  <h1>Three venues, three characters.</h1>
  <p class="dek">WWW, WSDM and SIGIR all draw from the same data-mining world, but each has a distinct personality. To find it we don't count raw topics (WWW is simply the biggest) — we measure what each venue <b>over-indexes on</b>: the topics and techniques that appear at a higher rate there than across the three combined. The <b>×</b> numbers are that lift.</p>
  <div class="sub"><a href="index.html">← the landscape</a> · <a href="course.html">plain course spine</a> · <a href="explorer.html">the paper explorer</a></div>
  <div class="cols">{col("WWW 2026")}{col("WSDM 2026")}{col("SIGIR 2026")}</div>

  <div class="synth">
    <h2>Reading the three side by side</h2>
    <p>Line them up and a clean division of labor appears. <b style="color:#4FA8B8">WWW</b> is the web's town square <em>and</em> its police force — it takes the whole ecosystem, and disproportionately the parts that go wrong: fraud, misinformation, privacy, security, and the graph and federated machinery used to handle a web too large to trust. <b style="color:#9B8CE0">WSDM</b>, the smallest, is the methods lab — for its size it punches far above its weight on causal inference, recommendation, and the freshest generative tooling (diffusion, reasoning), caring more about <em>how</em> than about <em>how much</em>. <b style="color:#E3A63A">SIGIR</b> is the retrieval specialist — ranking, retrieval-augmented generation, benchmarks, and the distillation that keeps search fast; where the others wander the web, SIGIR stays on the single problem of finding the right thing.</p>
    <p>What they share is the thing eating every venue: large language models sit near the top of all three. The difference is the frame each puts around the LLM — WWW asks whether it can be trusted, WSDM asks what new method it enables, SIGIR asks how it retrieves.</p>
    <p class="aha">Same field, three lenses: WWW watches the web, WSDM sharpens the method, SIGIR finds the answer — and all three now do it with a language model in the loop.</p>
    <p class="src">Over-indexing = a venue's within-venue rate for a topic/technique divided by the pooled rate across all three (× lift). Topics from the keyword taxonomy; techniques from the per-paper LLM analysis of 1,487 abstracts. Code: <span class="mono">compare_venues.py</span>.</p>
  </div>
</div>
"""
for rel in ("compare.html", os.path.join("site", "compare.html")):
    path = os.path.join(HERE, rel)
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    open(path, "w", encoding="utf-8").write(HTML)
print("wrote compare.html and site/compare.html ·", len(HTML)//1024, "KB · FFFD:", HTML.count("�"))
