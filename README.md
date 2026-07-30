# Data-mining conferences 2026 — WWW · WSDM · SIGIR

A first-principles analysis of **1,802 papers** from the 2026 data-mining / web / IR
conferences whose proceedings are open (WWW/TheWebConf, WSDM, SIGIR).

**Live:** https://mehtama1234.github.io/data-mining-conferences-2026/

- **index.html** — the theme landscape (by venue) + LLM-tagged technique bars
- **explorer.html** — searchable explorer of 1,487 papers, each with problem/approach/contribution
- **compare.html** — how WWW vs WSDM vs SIGIR differ (over-indexing)
- **deep.html** — a first-principles "deep read": the field as one journey (organize → find →
  anticipate → understand → guard → scale), with every stage, sub-theme, and paper explained
  in plain, no-jargon language.

Data: Semantic Scholar + DBLP. Per-paper analysis and plain-language rewrites by an LLM (Haiku).
Pipeline: `ingest*.py → mine_themes.py → make_batches.py → (Haiku workflow) → merge_*.py →
summarize.py → compare_venues.py → build_*.py`.
