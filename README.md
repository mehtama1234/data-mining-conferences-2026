# Data-mining conferences 2026 — WWW · WSDM · SIGIR

A first-principles analysis of **1,802 papers** from the 2026 data-mining / web / IR
conferences whose proceedings are open (WWW/TheWebConf, WSDM, SIGIR).

**Live:** https://mehtama1234.github.io/data-mining-conferences-2026/

- **index.html** — the theme landscape (by venue) + LLM-tagged technique bars
- **explorer.html** — searchable explorer of analyzed papers, each with problem/approach/contribution
- **compare.html** — how WWW vs WSDM vs SIGIR differ (over-indexing)
- **deep.html** — a first-principles "deep read": the field as one journey (organize → find →
  anticipate → understand → guard → scale), with every stage, sub-theme, and paper explained
  in plain, no-jargon language.

Data: Semantic Scholar + DBLP. Per-paper analysis and plain-language rewrites by an LLM (Haiku).

Deep-analysis standard: [FIRST_PRINCIPLES_GOAL.md](FIRST_PRINCIPLES_GOAL.md). The current pipeline has
separate generation passes for per-paper deep essays, recurring mathematical concepts, whole-field
synthesis, and theme/subtheme paper-family essays.

Pipeline: `ingest*.py → mine_themes.py → make_batches.py → prep_families.py → (Haiku workflows:
rich_workflow.js, kdd_workflow.js, concepts_workflow.js, family_workflow.js, synth_workflow.js) →
merge_*.py → summarize.py → compare_venues.py → build_*.py → validate_deep_content.py`.

`validate_deep_content.py` is the quality gate for the deep pass. It fails if any paper, concept,
synthesis, or family essay is still missing the required first-principles fields or is too short.
Use `deep_status.py` during generation to see compact progress across papers, concepts, families,
and synthesis. Use `deep_todo.py` to list the exact paper batches, concept keys, and family keys
that still need the deep schema.
