export const meta = {
  name: 'kdd-analysis-plus-rich',
  description: 'Combined per-paper analysis + rich first-principles story for KDD 2026 (Haiku, 4 batches)',
  phases: [{ title: 'KDD papers', detail: 'analysis + rich story per paper' }],
}
const DIR = '/home/manishmehta/ui-projects/data-mining-conferences-2026'
const N = 4

const PROMPT = (b) => `Read the batch file and produce, for EACH paper, BOTH a compact analysis AND a rich
first-principles story. This is KDD 2026 (data mining / knowledge discovery / applied ML on data).

Batch file to READ: ${DIR}/data/kdd_batches/${b}.json  (list of papers: gid, title, abstract, venue).

For EACH paper produce these fields:
COMPACT (short, factual, grounded in the abstract):
  "problem"      : one line — the gap/pain the paper addresses (~15 words)
  "approach"     : one line — what they actually do (~18 words)
  "contribution" : one line — the concrete result/what it gives (~15 words)
  "primary_theme": a short noun-phrase theme (e.g. "Recommender systems", "Graph learning",
                   "LLM agents", "Anomaly detection", "Time series", "Fairness")
  "methods"      : array of 2-4 short method tags (lowercase, e.g. ["graph neural network","contrastive"])
RICH STORY (plain language, NO jargon unless unpacked in-line, NO cliche, first-principles, 2-4 sentences each):
  "bp" : THE BIG PICTURE — the real-world goal this serves and why it matters. Zoom out.
  "wh" : WHY IT'S HARD — the specific tension; why the obvious approach fails.
  "ap" : WHAT THEY DO — the mechanism in plain terms a newcomer can picture.
  "ww" : WHY IT WORKS — the first-principles reason the mechanism actually helps.
  "po" : THE PAYOFF — what it concretely buys, grounded in the abstract.

Write OUTPUT as JSON to: ${DIR}/data/kdd_out/${b}.json
An object keyed by gid (string) -> {"problem":...,"approach":...,"contribution":...,"primary_theme":...,"methods":[...],"bp":...,"wh":...,"ap":...,"ww":...,"po":...}.
Escape any inner double-quote as \\". Include every paper. Then reply: wrote ${b}.`

phase('KDD papers')
const items = Array.from({ length: N }, (_, i) => `b${String(i).padStart(3, '0')}`)
const results = await parallel(items.map((b) => () =>
  agent(PROMPT(b), { label: `kdd:${b}`, phase: 'KDD papers', model: 'haiku', agentType: 'general-purpose' })
))
log(`KDD analysis+rich: ${results.filter(Boolean).length}/${N} returned`)
return { ok: results.filter(Boolean).length, total: N }
