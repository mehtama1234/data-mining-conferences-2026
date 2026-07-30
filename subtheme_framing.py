# -*- coding: utf-8 -*-
"""Plain-language, first-principles framing for each data-mining sub-theme:
the specific problem it solves and the approach it uses. No jargon (terms grounded
once), no cliche. Keyed by the exact theme names used in build_deep.py."""

FRAMING = {
 "LLMs & Language Models": (
  "A system meant to understand a person has to actually grasp language — its ambiguity, its context, the endless ways to say the same thing — which the old keyword-matching approaches never truly did.",
  "Use models trained on enormous amounts of human writing, which have soaked up how language works, then adapt and steer them toward a particular job."),
 "LLM Agents & Tool Use": (
  "A model that only produces text can answer a question but can't *do* anything — run the query, check the database, book the thing. Real tasks take several steps, decisions, and actions in the world.",
  "Let the model plan a sequence of steps and reach for outside tools between them — a search, a calculator, a database — so it can act, see what happened, and adjust. A worker, not just an oracle."),
 "Retrieval-Augmented (RAG)": (
  "A language model only knows what it absorbed while training; ask it something recent or specific and it will answer confidently and be wrong.",
  "Before it answers, have it look the facts up in a trusted source and write its reply from what it found — anchoring the fluent guesser in real evidence."),
 "Recommender Systems": (
  "With millions of items and no search query, the system has to guess what each person wants from behavior alone — and keep working for brand-new people and items it's never seen.",
  "Learn from the whole crowd (people like you liked this) and from the order and timing of each person's actions, to predict the next thing they'll want."),
 "Graph Learning & Mining": (
  "Much of the world is a web of connections — friends, links, purchases — where the connections themselves carry the meaning, but ordinary tools expect neat rows and columns, not tangles.",
  "Learn directly on the network, letting each thing's meaning be shaped by its neighbors, so the structure becomes something you can compute with and predict from."),
 "Knowledge Graphs": (
  "Facts scattered through text are useless to a machine until they're organized as explicit, connected statements it can look up and reason over — and the world's facts are vast, messy, and always changing.",
  "Build a structured web of things and the relationships between them, and learn to fill in, correct, and query it as new facts arrive."),
 "Information Retrieval & Search": (
  "A person has a need, and somewhere in billions of documents sit the few that answer it — but their words rarely match the document's, and the answer has to come back instantly.",
  "Compare by meaning rather than exact words, then carefully order the survivors so the most useful one rises to the top."),
 "Fairness, Bias & Responsible AI": (
  "A system trained on human data inherits human prejudice, and when it decides who sees a job ad or gets a loan, that bias becomes real discrimination at scale.",
  "Measure where outcomes come out unfairly across groups of people, and adjust the data or the model so it treats them evenhandedly instead of quietly encoding old biases."),
 "Privacy, Federated & Security": (
  "These systems run on deeply personal data, and both gathering it and learning from it can expose people — while attackers actively try to steal or poison it.",
  "Learn without ever pooling everyone's data in one place, add guarantees that no single person can be picked out, and harden the system against attack."),
 "Misinformation & Trust": (
  "The same platforms that spread news also spread lies, at a speed and scale no human fact-checker can keep up with — and falsehoods often travel faster than the truth.",
  "Learn the signals that tell credible from deceptive content, and how each spreads, so false information can be flagged or slowed before it takes hold."),
 "Fraud & Anomaly Detection": (
  "Among billions of ordinary actions, a tiny fraction are fraud, spam, or abuse — and the people behind them constantly change tactics to blend in.",
  "Learn what normal looks like well enough that the rare, coordinated, or out-of-pattern behavior stands out on its own, even as the patterns keep shifting."),
 "Social Networks & Influence": (
  "On a network of billions, ideas, behaviors, and moods spread person to person in ways that move elections, markets, and health — but the dynamics hide inside the tangle of connections.",
  "Model how influence flows across the network and how communities form, to understand and anticipate what spreads, and why."),
 "Causal Inference": (
  "Data is full of things that happen together, but acting on a coincidence that isn't a cause leads you astray — copying what people who quit happened to click won't stop anyone quitting.",
  "Separate what merely comes *with* an outcome from what actually *drives* it, so a system can predict the effect of an action it has never tried."),
 "Time Series & Spatiotemporal": (
  "Much of the world's data is a stream unfolding over time and place — traffic, demand, movement — and the question that matters is simply: what happens next?",
  "Learn the rhythms in the history, and the way places and moments pull on each other, to forecast the future and notice the instant something breaks the pattern."),
 "Text Mining & NLP": (
  "Most of what people write is loose, unstructured prose, and turning that flood into something a machine can sort, summarize, or answer from is a hard problem in itself.",
  "Teach systems to pull the meaning out of text — the mood, the names, the topics, the answer — and to condense or sort it at a scale no human could read."),
 "Multimodal & Vision-Language": (
  "The web isn't only words — it's images and video woven together with text — and a system that reads only the words misses half of what's there.",
  "Learn a shared understanding across pictures and language, so the system can connect what's shown to what's said and reason across both at once."),
 "Self-Supervised & Contrastive": (
  "Powerful models are hungry for labeled examples, but labeling is slow and costly, and almost all real data arrives with no labels at all.",
  "Let the data teach itself — hide part of it and have the model predict the rest, or learn what counts as similar and different — building rich understanding from raw, unlabeled material."),
 "Generative & Diffusion": (
  "Beyond finding or judging things that already exist, there's rising demand to *create* new ones — a plausible image, a stand-in dataset, a missing piece of a record.",
  "Train models that learn the shape of real data well enough to produce convincing new examples of it, often by starting from noise and refining it toward something real."),
 "Explainability & Interpretability": (
  "The most accurate systems are black boxes — they hand you an answer but not a reason — and you can't trust, fix, or be accountable for a decision you can't understand.",
  "Build tools that reveal *why* a system decided what it did — which inputs mattered, what it's really keying on — so a person can check it and know when to trust it."),
 "Efficiency & Scalability": (
  "A method that's brilliant but too slow, too large, or too costly to run for billions of people in real time never leaves the lab — and the newest models are enormous.",
  "Shrink and speed things up — compress big models, teach small ones to imitate large ones, cut the work each request costs — without giving up what made them good."),
 "Advertising & E-commerce": (
  "The web mostly runs on ads and online sales, where the system must match the right offer to the right person at the right moment, and where tiny improvements turn into enormous money.",
  "Predict what someone will click or buy, and design the auctions and pricing that decide what they see — balancing the interests of the person, the seller, and the platform."),
 "Reinforcement Learning": (
  "Some choices only pay off later and can only be judged by what follows — what to show now to keep someone engaged for months — so there's no fixed right answer to copy.",
  "Let the system learn by trying, watching the reward its choices earn over time, and steering toward the strategies that pay off in the long run."),
 "Other": (
  "Work that sits across or between the field's main problems.",
  "A mix of methods drawn from the rest of the field."),
}
