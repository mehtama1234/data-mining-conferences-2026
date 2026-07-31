export const meta = {
  name: 'kdd-analysis-plus-deep',
  description: 'Combined per-paper analysis + very deep first-principles story for KDD 2026 (Haiku, 4 batches)',
  phases: [{ title: 'KDD papers', detail: 'analysis + deep story per paper' }],
}
const DIR = '/home/manishmehta/ui-projects/data-mining-conferences-2026'
const N = 4
// Resume controls. Leave ONLY empty to run everything; otherwise list batches like ['b000','b003'].
const ONLY = []
const WAVE_SIZE = 4

const PROMPT = (b) => `Read the batch file and produce, for EACH paper, BOTH a compact analysis AND a very deep
first-principles story. This is KDD 2026 (data mining / knowledge discovery / applied ML on data).
Use this goal as the standard for depth: ${DIR}/FIRST_PRINCIPLES_GOAL.md

Batch file to READ: ${DIR}/data/kdd_batches/${b}.json  (list of papers: gid, title, abstract, venue).

For EACH paper produce these fields:
COMPACT (short, factual, grounded in the abstract):
  "problem"      : one line — the gap/pain the paper addresses (~15 words)
  "approach"     : one line — what they actually do (~18 words)
  "contribution" : one line — the concrete result/what it gives (~15 words)
  "primary_theme": a short noun-phrase theme (e.g. "Recommender systems", "Graph learning",
                   "LLM agents", "Anomaly detection", "Time series", "Fairness")
  "methods"      : array of 2-4 short method tags (lowercase, e.g. ["graph neural network","contrastive"])
DEEP STORY (plain language, no jargon unless unpacked immediately, no cliche, grounded in the abstract):
  "bp"     : BIG PICTURE, 120-180 words. The real-world system/question this serves before naming the method.
  "wh"     : WHY IT IS HARD, 120-180 words. The central tension and why the obvious/simple approach breaks.
  "naive"  : THE NAIVE SOLUTION, 90-140 words. What a smart beginner would try first and where it fails.
  "ap"     : CORE IDEA, 120-180 words. The paper's central move in concrete mechanical terms.
  "mech"   : HOW THE MECHANISM RUNS, 180-260 words. What goes in, what is transformed/scored/learned, what comes out.
  "math"   : MATHEMATICAL CONCEPTS, 180-260 words. Explain the important math from everyday first principles and why it matters here.
  "dots"   : CONNECTING THE DOTS, 120-180 words. Link this paper to neighboring KDD/data-mining paper families and recurring ideas.
  "ww"     : WHY IT WORKS, 140-220 words. The deeper reason this improves over the naive attempt.
  "po"     : PAYOFF, 80-130 words. What capability/result it buys, grounded in the abstract.
  "limits" : LIMITS AND ASSUMPTIONS, 80-130 words. What must be true and what the abstract does not prove.

Write OUTPUT as JSON to: ${DIR}/data/kdd_out/${b}.json
An object keyed by gid (string) -> {"problem":...,"approach":...,"contribution":...,"primary_theme":...,"methods":[...],"bp":...,"wh":...,"naive":...,"ap":...,"mech":...,"math":...,"dots":...,"ww":...,"po":...,"limits":...}.
Escape any inner double-quote as \\". Include every paper. Then reply: wrote ${b}.`

phase('KDD papers')
const items = ONLY.length ? ONLY : Array.from({ length: N }, (_, i) => `b${String(i).padStart(3, '0')}`)
const results = []
for (let i = 0; i < items.length; i += WAVE_SIZE) {
  const wave = items.slice(i, i + WAVE_SIZE)
  log(`KDD wave ${i / WAVE_SIZE + 1}: ${wave.join(', ')}`)
  results.push(...await parallel(wave.map((b) => () =>
    agent(PROMPT(b), { label: `kdd:${b}`, phase: 'KDD papers', model: 'haiku', agentType: 'general-purpose' })
  )))
}
log(`KDD analysis+deep: ${results.filter(Boolean).length}/${items.length} returned`)
return { ok: results.filter(Boolean).length, total: items.length }
