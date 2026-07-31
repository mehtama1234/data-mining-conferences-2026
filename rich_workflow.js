export const meta = {
  name: 'dm-rich-firstprinciples',
  description: 'Rich first-principles no-jargon per-paper writeups for data-mining 2026 (Haiku, 100 batches)',
  phases: [{ title: 'Rich writeups', detail: 'one Haiku agent per 15-paper batch' }],
}

// GOTCHA (proven): Workflow args don't bind -> HARDCODE.
const DIR = '/home/manishmehta/ui-projects/data-mining-conferences-2026'
const N = 100

const PROMPT = (b) => `You are writing for a curious, smart reader who is NOT a specialist in this subfield.
Read the batch file and produce a RICH, first-principles, plain-language explanation of EACH paper.

Batch file to READ: ${DIR}/data/batches/${b}.json
It is a JSON list of papers, each with: gid, title, abstract, venue, theme.

For EACH paper, write five short parts. Rules that matter more than anything:
- NO JARGON. If you must use a technical term, unpack it in the same breath in plain words.
  Banned unless immediately explained: "embedding", "latent space", "token", "gradient",
  "low-rank", "attention", "contrastive", "regularization", "distribution shift", "SOTA",
  "leverage", "novel", "robust", "framework", "paradigm". Prefer everyday words.
- NO CLICHE, no hype, no "in today's fast-paced world". Say concrete things.
- FIRST PRINCIPLES: explain the *why*, the mechanism, the intuition — not just what was done.
- CONNECT THE DOTS: part 1 must zoom OUT to the real-world thing we're ultimately trying to
  make work, so a newcomer sees why this paper exists at all.
- Ground every claim in THIS paper's abstract. Do not invent numbers or methods not present.

The five parts (each 2-4 sentences, plain prose, no lists inside):
  "bp" = THE BIG PICTURE: the real-world goal this serves and why it matters. Zoom out.
  "wh" = WHY IT'S HARD: the specific tension — why the obvious/naive approach fails here.
  "ap" = WHAT THEY DO: the actual idea/mechanism, in plain mechanical terms a newcomer can picture.
  "ww" = WHY IT WORKS: the first-principles reason this mechanism actually helps — the intuition.
  "po" = THE PAYOFF: what it concretely buys (capability, result), grounded in the abstract.

Write the OUTPUT as JSON to this exact path: ${DIR}/data/rich_out/${b}.json
The JSON is an object keyed by the paper's gid (as a string) -> {"bp":...,"wh":...,"ap":...,"ww":...,"po":...}.
Include every paper in the batch. Then reply with just: wrote ${b} (COUNT papers).`

phase('Rich writeups')
const items = Array.from({ length: N }, (_, i) => `b${String(i).padStart(3, '0')}`)
const results = await parallel(items.map((b) => () =>
  agent(PROMPT(b), { label: `rich:${b}`, phase: 'Rich writeups', model: 'haiku', agentType: 'general-purpose' })
))
const ok = results.filter(Boolean).length
log(`rich pass done: ${ok}/${N} batch agents returned`)
return { ok, total: N }
