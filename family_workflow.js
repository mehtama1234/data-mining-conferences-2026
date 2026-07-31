export const meta = {
  name: 'dm-paper-families',
  description: 'Deep first-principles paper-family essays for data-mining themes/subthemes (Haiku)',
  phases: [{ title: 'Paper families', detail: 'one Haiku agent per theme family' }],
}

const DIR = '/home/manishmehta/ui-projects/data-mining-conferences-2026'
const JOBS = [
  'llms-language-models',
  'efficiency-scalability',
  'information-retrieval-search',
  'recommender-systems',
  'social-networks-influence',
  'self-supervised-contrastive',
  'generative-diffusion',
  'llm-agents-tool-use',
  'multimodal-vision-language',
  'explainability-interpretability',
  'fairness-bias-responsible-ai',
  'retrieval-augmented-rag',
  'graph-learning-mining',
  'time-series-spatiotemporal',
  'privacy-federated-security',
  'advertising-e-commerce',
  'misinformation-trust',
  'text-mining-nlp',
  'knowledge-graphs',
  'reinforcement-learning',
  'causal-inference',
  'fraud-anomaly-detection',
]
// Resume controls. Leave ONLY empty to run all families; otherwise list keys from deep_todo.py.
const ONLY = []
const WAVE_SIZE = 4

const PROMPT = (k) => `You are writing a deep, plain-language PAPER FAMILY explanation for one theme/subtheme
in data mining / web / information retrieval / recommendation.

READ:
- Depth standard: ${DIR}/FIRST_PRINCIPLES_GOAL.md
- Family evidence: ${DIR}/data/family_in/${k}.json

The family evidence gives the theme name, paper count, venue spread, title examples, and representative
papers with problem / approach / contribution / methods. Use those papers as evidence. Do not invent
methods or results not supported by the file.

Your job is to explain why these papers are siblings from first principles. The reader should not need
math, ML, benchmark, causal-inference, optimization, retrieval, recommendation, graph, privacy, or systems
background. If you must use a technical term, unpack it immediately in everyday language.

Write SEVEN parts:
  "problem_shape" = 160-240 words. The shared real-world problem shape that makes this a family.
  "naive_failure" = 120-180 words. What a smart beginner would try across this family and why it fails.
  "mathematical_principle" = 180-260 words. The important math idea behind the family, in plain language:
    what is being measured, compared, ranked, predicted, sampled, optimized, matched, constrained, compressed,
    protected, or trusted.
  "why_math_matters" = 160-240 words. Why that math is not decoration: what structure in the world it exploits
    and why the papers need it.
  "paper_family" = 180-260 words. Connect specific representative papers to the shared family logic; explain
    how superficially different papers are versions of the same deeper move.
  "what_changed" = 100-160 words. What the 2026 version of this family seems to be doing differently.
  "limits" = 100-160 words. What assumptions must hold, where the family breaks, and what the evidence does not prove.

Style rules: no cliche, no hype, no method-name worship. Prefer concrete everyday language. The output must be
valid JSON written to ${DIR}/data/family_out/${k}.json as:
{"problem_shape":"...","naive_failure":"...","mathematical_principle":"...","why_math_matters":"...","paper_family":"...","what_changed":"...","limits":"..."}
Escape inner double-quotes as \\". Then reply: wrote ${k}.`

phase('Paper families')
const jobs = ONLY.length ? ONLY : JOBS
const results = []
for (let i = 0; i < jobs.length; i += WAVE_SIZE) {
  const wave = jobs.slice(i, i + WAVE_SIZE)
  log(`family wave ${i / WAVE_SIZE + 1}: ${wave.join(', ')}`)
  results.push(...await parallel(wave.map((k) => () =>
    agent(PROMPT(k), { label: `family:${k}`, phase: 'Paper families', model: 'haiku', agentType: 'general-purpose' })
  )))
}
log(`DM paper families: ${results.filter(Boolean).length}/${jobs.length} returned`)
return { ok: results.filter(Boolean).length, total: jobs.length }
