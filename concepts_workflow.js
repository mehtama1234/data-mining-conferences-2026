export const meta = {
  name: 'dm-rich-concepts',
  description: 'Rich first-principles conceptual essays for the recurring math ideas (Haiku, per concept)',
  phases: [{ title: 'Concept essays', detail: 'one Haiku agent per math concept' }],
}
const DIR = '/home/manishmehta/ui-projects/data-mining-conferences-2026'
const KEYS = ['matching','cause','information','network','similarity','rank','sequence','probability','attention','optimize','learn']

const PROMPT = (k) => `You are writing the definitive plain-language, first-principles explanation of ONE recurring
mathematical idea that shows up across data-mining / web / information-retrieval research.

READ this file: ${DIR}/data/concept_in/${k}.json
It has: key, title, intro + why (a short earlier draft — you must go DEEPER and RICHER than these),
n_total (how many papers lean on this idea), and papers[] (real papers under it, each with a
plain 'uses' note). The papers are your evidence for connecting the dots.

Write FOUR parts. Rules that matter more than anything:
- NO JARGON. If a technical term is unavoidable, unpack it in plain words in the same breath.
  Prefer everyday words and physical/again-from-scratch intuition over named techniques.
- NO CLICHE, no hype, no "in today's world". Every sentence must carry a real idea.
- FIRST PRINCIPLES: build the idea up from scratch — what problem in the world would make a
  thoughtful person INVENT this? Do not assume the reader has seen it before.
- CONNECT THE DOTS: part 3 must draw on the ACTUAL papers[] in the file — show how this one idea
  wears many disguises across them, so the reader sees the single thread under many different papers.
- Go deeper than the provided intro/why; treat those only as a floor you must exceed.

The four parts:
  "idea"    = THE IDEA, FROM SCRATCH: the real-world need that forces this idea into existence, and
              what the idea actually IS once you strip away all notation. 5-8 sentences.
  "why"     = WHY IT WORKS: the underlying reason/guarantee that makes it valid — not a slogan, the
              actual mechanism of why it can't-not-work (and where it breaks). 4-6 sentences.
  "dots"    = CONNECTING THE DOTS: how this single idea recurs across the specific papers in this
              group — the shared move under superficially different problems. Ground it in papers[].
              5-8 sentences.
  "picture" = ONE concrete everyday analogy that makes the idea click. 2-3 sentences.

Write OUTPUT as JSON to this exact path: ${DIR}/data/concept_out/${k}.json
A single object: {"idea":"...","why":"...","dots":"...","picture":"..."}.
Escape any double-quote inside a value as \\" so the JSON parses. Then reply: wrote ${k}.`

phase('Concept essays')
const results = await parallel(KEYS.map((k) => () =>
  agent(PROMPT(k), { label: `concept:${k}`, phase: 'Concept essays', model: 'haiku', agentType: 'general-purpose' })
))
log(`DM concept essays: ${results.filter(Boolean).length}/${KEYS.length} returned`)
return { ok: results.filter(Boolean).length, total: KEYS.length }
