export const meta = {
  name: 'dm-deep-firstprinciples',
  description: 'Very deep first-principles no-jargon per-paper essays for data-mining 2026 (Haiku, 100 batches)',
  phases: [{ title: 'Deep writeups', detail: 'one Haiku agent per 15-paper batch' }],
}

// GOTCHA (proven): Workflow args don't bind -> HARDCODE.
const DIR = '/home/manishmehta/ui-projects/data-mining-conferences-2026'
const N = 100
// Resume controls. Leave ONLY empty to run everything; otherwise list batches like ['b000','b017'].
// WAVE_SIZE limits concurrent agents so the very-deep pass can run without flooding the runner.
const ONLY = []
const WAVE_SIZE = 8

const PROMPT = (b) => `You are writing for a curious, smart reader who is NOT a specialist in this subfield.
Read the batch file and produce a VERY DEEP, first-principles, plain-language explanation of EACH paper.

Batch file to READ: ${DIR}/data/batches/${b}.json
It is a JSON list of papers, each with: gid, title, abstract, venue, theme.
Depth standard to READ and follow: ${DIR}/FIRST_PRINCIPLES_GOAL.md

For EACH paper, write a real conceptual essay broken into ten named parts. Rules that matter more than anything:
- NO JARGON. If you must use a technical term, unpack it in the same breath in plain words.
  Banned unless immediately explained: "embedding", "latent space", "token", "gradient",
  "low-rank", "attention", "contrastive", "regularization", "distribution shift", "SOTA",
  "leverage", "novel", "robust", "framework", "paradigm". Prefer everyday words.
- NO CLICHE, no hype, no "in today's fast-paced world". Say concrete things.
- FIRST PRINCIPLES: start from the real object being modeled, the information available, the
  uncertainty, the constraint, and the failure mode. Do not start from the method name.
- DEEP MECHANISM: explain the moving parts step by step, as if the reader had to rebuild the
  idea from scratch after reading your explanation.
- MATHEMATICAL CONCEPTS: name the actual mathematical ideas being used, but define each in
  plain language and explain why that mathematical move fits this paper.
- CONNECT THE DOTS: connect this paper to at least two neighboring ideas in the conference
  when the abstract supports it: ranking, similarity, probability, graphs, sequences, causality,
  privacy, auctions, optimization, language models, recommendation, retrieval, fraud, fairness.
- Ground every claim in THIS paper's abstract. Do not invent numbers or methods not present.
- If the abstract is thin, say what can be inferred and what cannot. Do not fill gaps with generic filler.

The ten parts:
  "bp" = BIG PICTURE, 120-180 words. What real-world system or scientific question this serves. Explain why anyone needs this paper before naming the method.
  "wh" = WHY IT IS HARD, 120-180 words. The central tension and why the obvious/simple approach breaks.
  "naive" = THE NAIVE SOLUTION, 90-140 words. What a smart beginner would try first, and exactly where it fails.
  "ap" = CORE IDEA, 120-180 words. The paper's central move in concrete, mechanical terms.
  "mech" = HOW THE MECHANISM RUNS, 180-260 words. Step-by-step: what goes in, what is transformed, what is compared/scored/optimized, what comes out.
  "math" = MATHEMATICAL CONCEPTS, 180-260 words. The mathematical objects and ideas being used, explained from first principles and tied to this paper.
  "dots" = CONNECTING THE DOTS, 120-180 words. How this paper relates to recurring conference ideas and why it sits in the broader field.
  "ww" = WHY IT WORKS, 140-220 words. The causal/intuitive reason the mechanism should improve over the naive approach.
  "po" = PAYOFF, 80-130 words. What capability/result it buys, grounded in the abstract.
  "limits" = LIMITS AND ASSUMPTIONS, 80-130 words. What must be true for this to work and what the abstract does not prove.

Write the OUTPUT as JSON to this exact path: ${DIR}/data/rich_out/${b}.json
The JSON is an object keyed by the paper's gid (as a string) -> {"bp":...,"wh":...,"naive":...,"ap":...,"mech":...,"math":...,"dots":...,"ww":...,"po":...,"limits":...}.
Include every paper in the batch. Then reply with just: wrote ${b} (COUNT papers).`

phase('Deep writeups')
const items = ONLY.length ? ONLY : Array.from({ length: N }, (_, i) => `b${String(i).padStart(3, '0')}`)
const results = []
for (let i = 0; i < items.length; i += WAVE_SIZE) {
  const wave = items.slice(i, i + WAVE_SIZE)
  log(`deep wave ${i / WAVE_SIZE + 1}: ${wave.join(', ')}`)
  results.push(...await parallel(wave.map((b) => () =>
    agent(PROMPT(b), { label: `deep:${b}`, phase: 'Deep writeups', model: 'haiku', agentType: 'general-purpose' })
  )))
}
const ok = results.filter(Boolean).length
log(`deep pass done: ${ok}/${items.length} batch agents returned`)
return { ok, total: items.length }
