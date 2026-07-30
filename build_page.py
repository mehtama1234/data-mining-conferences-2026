import json, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, "data", "themes.json")))
S = json.load(open(os.path.join(HERE, "data", "summary.json")))
def esc(s): return html.escape(str(s))
N = T["n_papers"]

def methodbars():
    ms = S["methods"]; mx = max(m["n"] for m in ms)
    return "".join(f"<div class='bar'><span class='bl'>{esc(m['tag'])}</span>"
                   f"<span class='bt'><span class='bf' style='width:{m['n']/mx*100:.1f}%;background:#4FA8B8'></span></span>"
                   f"<span class='bv'>{m['n']}</span></div>" for m in ms)

def bars():
    mx = max(t["n"] for t in T["themes"])
    out = ""
    for t in T["themes"]:
        www = t["by_venue"].get("WWW 2026", 0); wsdm = t["by_venue"].get("WSDM 2026", 0); sig = t["by_venue"].get("SIGIR 2026", 0)
        out += (f"<div class='bar'><span class='bl'>{esc(t['theme'])}</span>"
                f"<span class='bt'>"
                f"<span class='bf w' style='width:{www/mx*100:.1f}%'></span>"
                f"<span class='bf s' style='width:{wsdm/mx*100:.1f}%'></span>"
                f"<span class='bf g' style='width:{sig/mx*100:.1f}%'></span></span>"
                f"<span class='bv'>{t['n']}<span class='bp'> · {t['pct']}%</span></span></div>")
    return out

def themecards():
    out = ""
    for t in T["themes"][:12]:
        ex = "".join(f"<li>{esc(e['title'])} <span class='vtag'>{esc(e['venue'].split()[0])}</span></li>" for e in t["examples"][:3])
        out += (f"<div class='tcard'><div class='th'><span class='tn'>{esc(t['theme'])}</span>"
                f"<span class='tc'>{t['n']}</span></div><ul class='tex'>{ex}</ul></div>")
    return out

P = f"""<meta charset="utf-8">
<title>Data Mining Conferences 2026 · the landscape</title>
<style>
:root{{--bg:#0E1420;--bg2:#141D2C;--panel:#18212F;--ink:#EAEEF4;--soft:#B4BFD0;--dim:#8493A8;--faint:#5A6577;
--line:rgba(150,170,205,.14);--accent:#4FA8B8;--amber:#E3A63A;--rose:#E0748A;--viol:#9B8CE0;--serif:"Iowan Old Style",Palatino,Georgia,serif;
--sans:-apple-system,system-ui,"Segoe UI",Roboto,Arial,sans-serif;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.7;font-size:17px}}
.wrap{{max-width:900px;margin:0 auto;padding:0 24px}}
p{{color:var(--soft);margin:0 0 16px}}b{{color:var(--ink)}}em{{color:#fff;font-style:italic}}
.mono{{font-family:var(--mono)}}
.kick{{font-family:var(--mono);font-size:11.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--accent)}}
h1{{font-family:var(--serif);font-size:clamp(32px,6vw,52px);line-height:1.05;margin:14px 0 0;color:#fff;letter-spacing:-.02em}}
h2{{font-family:var(--serif);font-size:27px;margin:0 0 6px;color:#fff}}
.dek{{font-size:19px;color:var(--soft);margin-top:18px;max-width:64ch}}
section{{padding:42px 0;border-top:1px solid var(--line)}}
.eye{{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--dim);margin-bottom:12px}}
.stat{{display:flex;gap:26px;flex-wrap:wrap;margin:22px 0 6px}}
.stat .sn{{font-family:var(--serif);font-size:34px;color:#fff;line-height:1}}.stat .sl{{font-family:var(--mono);font-size:11px;color:var(--dim);margin-top:6px}}
.note{{background:var(--bg2);border:1px solid var(--line);border-left:3px solid var(--amber);border-radius:12px;padding:14px 18px;margin:18px 0}}
.note .nt{{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--amber);margin-bottom:6px}}.note p{{margin:0;font-size:14.5px;color:var(--soft)}}
.why{{background:var(--bg2);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:12px;padding:16px 20px;margin:18px 0}}
.why h3{{margin:0 0 6px;font-size:12.5px;font-family:var(--mono);letter-spacing:.05em;text-transform:uppercase;color:var(--accent)}}.why p{{margin:0;font-size:15px;color:var(--soft)}}
.bar{{display:flex;align-items:center;gap:12px;margin:7px 0;font-family:var(--mono);font-size:12.5px}}
.bar .bl{{width:220px;color:var(--soft);text-align:right;flex:0 0 auto}}
.bar .bt{{flex:1;height:18px;background:rgba(150,170,205,.06);border-radius:5px;overflow:hidden;display:flex}}
.bar .bf{{display:block;height:100%}}.bar .bf.w{{background:#4FA8B8}}.bar .bf.s{{background:#9B8CE0}}.bar .bf.g{{background:#E3A63A}}
.bar .bv{{width:82px;color:var(--ink)}}.bar .bp{{color:var(--faint)}}
@media(max-width:640px){{.bar .bl{{width:130px;font-size:11px}}}}
.leg{{font-family:var(--mono);font-size:12px;color:var(--faint);margin-top:12px}}
.leg .sw{{display:inline-block;width:11px;height:11px;border-radius:2px;vertical-align:middle;margin:0 5px 0 14px}}
.tgrid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px}}
@media(max-width:640px){{.tgrid{{grid-template-columns:1fr}}}}
.tcard{{background:var(--bg2);border:1px solid var(--line);border-radius:12px;padding:14px 16px}}
.th{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px}}
.tn{{font-family:var(--serif);font-size:16px;color:#fff}}.tc{{font-family:var(--mono);font-size:13px;color:var(--accent)}}
.tex{{margin:0;padding-left:0;list-style:none}}
.tex li{{font-size:12.5px;color:var(--dim);margin:4px 0;line-height:1.45}}
.vtag{{font-family:var(--mono);font-size:9.5px;color:var(--faint);border:1px solid var(--line);border-radius:8px;padding:0 5px;margin-left:3px}}
.aha{{font-family:var(--serif);font-size:21px;line-height:1.4;color:#fff;border-left:3px solid var(--accent);padding-left:18px;margin:8px 0}}
.src{{font-family:var(--mono);font-size:12px;color:var(--faint);margin-top:28px;padding-top:16px;border-top:1px solid var(--line)}}.src a{{color:var(--accent);text-decoration:none}}
</style>
<div class="wrap">
<header style="padding:60px 0 8px">
  <div class="kick">Data-mining conferences 2026 · WWW · WSDM · SIGIR</div>
  <h1>What the data-mining world is working on in 2026.</h1>
  <p class="dek">A theme map of <b>{N:,} papers</b> from the three 2026 data-mining / web / IR conferences whose proceedings are already open: <b>WWW / TheWebConf</b> ({T['venues'].get('WWW 2026',0)}), <b>WSDM</b> ({T['venues'].get('WSDM 2026',0)}) and <b>SIGIR</b> ({T['venues'].get('SIGIR 2026',0)}). Built over real abstracts, so the themes are grounded in what papers actually say — not just their titles.</p>
  <div class="stat">
    <div><div class="sn">{N:,}</div><div class="sl">papers</div></div>
    <div><div class="sn">{T['with_abstract']*100//N}%</div><div class="sl">with abstracts</div></div>
    <div><div class="sn">{len(T['themes'])}</div><div class="sl">research themes</div></div>
    <div><div class="sn">3</div><div class="sl">of the KDD family (more to come)</div></div>
  </div>
  <div class="note"><div class="nt">scope — the KDD family, and what's next</div>
  <p><b>KDD 2026</b> itself isn't published yet (it's an August conference). These siblings <em>are</em> out and — unlike IEEE venues — carry {T['with_abstract']*100//N}% abstracts, so a grounded analysis is possible now. As the year goes on, <b>KDD, RecSys, CIKM, ICDM</b> publish and can join this same map. Two layers here: a deterministic theme landscape below, <b>and</b> a per-paper read where a language model pulled the problem · approach · contribution out of all {S['n_analyzed']:,} abstracts — <a href="explorer.html">explore it</a>, or see <a href="compare.html">how the three venues differ</a>.</p></div>
</header>

<section>
  <div class="eye">The landscape · one bar per theme, split by venue</div>
  <h2>LLMs have swallowed the field</h2>
  <p>Every paper is matched to the research themes its title + abstract touch (a paper can span several). The single biggest story is unmissable: <b>{T['themes'][0]['pct']:.0f}% of papers touch large language models</b> — more than recommenders, graphs, and search, the classic pillars of this community, and it shows up across all three venues:</p>
  <div style="margin-top:14px">{bars()}</div>
  <div class="leg"><span class="sw" style="background:#4FA8B8"></span>WWW / TheWebConf<span class="sw" style="background:#9B8CE0"></span>WSDM<span class="sw" style="background:#E3A63A"></span>SIGIR</div>
  <div class="why"><h3>How to read this honestly</h3><p>Themes overlap — a paper on "an efficient LLM recommender" counts in three. "Efficiency &amp; Scalability" is a cross-cutting quality rather than a topic, which is why it ranks so high. The signal that matters: the classic data-mining pillars (recommenders, graphs, IR, social networks) are all still strong, but <em>every one of them now has an LLM version</em> — the LLM theme cuts across the whole conference.</p></div>
</section>

<section>
  <div class="eye">The techniques · read out of {S['n_analyzed']:,} abstracts by an LLM</div>
  <h2>What they're actually building with</h2>
  <p>Beyond topics, we had a language model read every abstract and tag the <em>techniques</em> each paper uses. This is the real toolkit of the field in 2026 — and it confirms the story from the other side: large language models are the single most-used tool, but retrieval, graphs, multimodal fusion, contrastive learning and the newer wave of agents / RAG / reasoning are all right behind:</p>
  <div style="margin-top:14px">{methodbars()}</div>
</section>

<section>
  <div class="eye">Inside the themes · real papers</div>
  <h2>What each theme actually contains</h2>
  <p>A few real titles from the top themes, so the buckets aren't abstract:</p>
  <div class="tgrid">{themecards()}</div>
</section>

<section>
  <div class="eye">Go deeper · every paper, read</div>
  <h2>Explore all {S['n_analyzed']:,} papers by what they contribute</h2>
  <p>An LLM read each of the {S['n_analyzed']:,} papers with an abstract and pulled out its <b>problem</b>, its <b>approach</b>, and what it <b>contributes</b> — in one line each. Search and filter the whole set: type a topic, a method, a phrase; filter by venue.</p>
  <p style="margin-top:6px"><a href="explorer.html" style="display:inline-block;font-family:var(--mono);font-size:14px;color:#0E1420;background:var(--accent);border-radius:9px;padding:10px 22px;text-decoration:none;font-weight:600">→ open the paper explorer</a> <a href="deep.html" style="display:inline-block;font-family:var(--mono);font-size:14px;color:#0E1420;background:var(--accent);border-radius:9px;padding:10px 22px;text-decoration:none;font-weight:600">→ the deep read: the field as one story</a></p>
</section>

<section>
  <div class="eye">The one-line read</div>
  <p class="aha">Data mining in 2026 is still built on its old pillars — recommendation, graphs, search, social networks — but a large-language-model layer now runs through all of them, and the community's second obsession is making it efficient, fair, and trustworthy enough to ship.</p>
  <p class="src">Data: Semantic Scholar + DBLP (WWW, WSDM, SIGIR 2026; {T['with_abstract']*100//N}% abstract coverage). Two layers: a transparent deterministic keyword taxonomy over title+abstract (<span class="mono">mine_themes.py</span>), and a per-paper LLM read of {S['n_analyzed']:,} abstracts for problem/approach/contribution/technique (<span class="mono">Haiku workflow → merge_analysis.py → summarize.py</span>). KDD / RecSys / CIKM / ICDM 2026 join as their proceedings open.</p>
</section>
</div>
"""
open(os.path.join(HERE, "site", "index.html"), "w", encoding="utf-8").write(P)
print("wrote site/index.html ·", len(P)//1024, "KB · FFFD:", P.count("�"))
