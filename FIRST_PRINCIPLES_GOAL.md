# Deep First-Principles Analysis Goal

Build the site as a deeply explanatory map of the conference, not a collection of paper summaries. The goal is not to make the explanations longer. The goal is to make them structurally deeper: every page should teach the reader how to think about the problem from the ground up, why the mathematical idea had to appear, and how separate papers are different attempts to solve the same underlying difficulty.

The reader is smart and curious, but should not need prior knowledge of math, machine learning jargon, benchmark jargon, causal-inference jargon, optimization jargon, information-retrieval jargon, recommendation jargon, graph jargon, privacy jargon, or systems jargon. Every technical idea must be rebuilt from ordinary language before it is named.

## Working Objective

Maintain the data-mining site as one connected first-principles explanation system:

- papers explain the concrete task, the failed beginner solution, the mechanism, the mathematical idea, and the limits
- themes explain the shared real-world pressure that makes many papers appear together
- subthemes explain the narrower problem shape inside a theme
- concepts explain the mathematical tool that keeps reappearing and why it fits the world
- paper families explain how sibling papers are different answers to the same underlying difficulty

The reader should be able to move from one paper to its concept, family, and theme, then return to the paper with a better sense of why the method was natural. The output fails if it reads like isolated paper summaries, a list of method names, or a longer version of the abstract.

The quality bar is: deep conceptual explanation, plain everyday language, no cliches, no unexplained jargon, no benchmark-only framing, and real connecting-the-dots across papers.

## What The Analysis Must Teach

For every paper, theme, subtheme, mathematical concept, and paper family, explain:

- the real-world thing being built, protected, measured, predicted, retrieved, ranked, generated, or optimized
- why the problem exists before any method is introduced
- what a smart beginner would try first
- exactly why that naive attempt fails
- the paper's central move in concrete mechanical terms
- what goes in, what gets transformed, what is compared or scored, and what comes out
- the mathematical principle underneath the method, explained without assuming notation
- why that mathematical principle fits the problem
- what structure in the world the math is exploiting
- how this paper connects to sibling papers, neighboring subthemes, and the broader field
- what assumptions must hold, and what the abstract does not prove

The explanation is incomplete if it only says what the authors did. It must also explain why the problem is naturally difficult before the method exists, why simpler ideas fail, and why the chosen mathematical structure is a good fit.

## Per-Paper Standard

Each paper should read like a small conceptual lesson. It should not simply restate the abstract. The explanation should start from the underlying object: a user need, a document collection, a graph of relationships, a stream over time, a ranking decision, a privacy constraint, a fraud pattern, an auction, a language model answer, or a recommendation moment.

For each paper, the reader should be able to answer these questions after reading:

- What ordinary-world problem is this paper trying to handle?
- What would someone naturally try first?
- What exactly breaks in that simple attempt?
- What information does the paper keep, compare, move, compress, rank, predict, hide, or generate?
- What mathematical idea makes that move possible?
- Why is that math a better language for the problem than a hand-written rule?
- What sibling papers are solving the same deeper problem with a different surface vocabulary?
- What must be true about the data, users, model, or setting for the claim to be trustworthy?

The paper-level story should include:

- `bp`: big picture
- `wh`: why it is hard
- `naive`: the naive solution and why it fails
- `ap`: the core idea
- `mech`: how the mechanism runs step by step
- `math`: the mathematical concepts being used
- `dots`: how it connects to themes, subthemes, and paper families
- `ww`: why it works
- `po`: payoff
- `limits`: limits and assumptions

Minimum depth: each field should contain a real explanation, not a label. The `math`, `mech`, `dots`, and `limits` fields are the main anti-shallow fields. They should name the moving parts, describe how they interact, and avoid merely repeating method names from the abstract.

## Theme, Subtheme, And Paper-Family Standard

A theme or family should answer: why do these papers belong together?

For each family, explain the shared problem shape, the repeated failure mode, the recurring mathematical tools, and what changed in 2026. The family explanation should make the reader see that superficially different papers are often solving the same deeper problem: measuring nearness, sorting candidates, estimating chances, spreading evidence through a network, separating cause from coincidence, following a slope downhill, matching scarce resources, compressing detail, handling time, or defending against adversaries.

Themes and subthemes must not be umbrella labels. They should act like connective tissue across papers. A good family explanation says:

- Here is the common real-world pressure that keeps appearing.
- Here is the naive strategy that many papers are trying to move beyond.
- Here is the recurring mathematical move.
- Here is why that move appears in many different-looking papers.
- Here are the papers that represent different branches of the same idea.
- Here is what changed this year: scale, data type, reliability requirement, user setting, privacy constraint, evaluation target, or deployment pressure.

When explaining a family, avoid listing papers one by one. Instead, organize the family around the hidden shared problem. For example, search, recommendation, and retrieval papers often look different on the surface, but many are really about choosing a small useful set from a huge pile under uncertainty. Graph, social, and knowledge papers often ask how evidence should travel through links. Causal, fairness, and policy papers often ask how to avoid confusing correlation with the thing that actually changes an outcome.

For every paper family, include the family from first principles:

- the shared object in the world: users, items, documents, graphs, examples, private records, decisions, delays, attacks, or scarce resources
- the pressure that makes the family hard
- the simple approach and the exact way it breaks
- the mathematical principle that appears because of that pressure
- why the principle matters, not just what it is called
- how papers split into branches of the same idea
- the assumptions and failure modes shared by the family

For every subtheme, explain what becomes more difficult than in the parent theme: scale, noise, missing evidence, delayed feedback, privacy, adversarial behavior, scarce labels, cost, ambiguity, or conflicting goals. Then explain the mathematical move that this added difficulty forces.

## Math Standard

Do not say "uses optimization" and stop. Explain what optimization is doing here: choosing settings, routes, rankings, assignments, or model behavior by defining what counts as wrong and repeatedly reducing that wrongness.

Do not say "uses probability" and stop. Explain what uncertainty is being estimated, what repeated observations make reliable, and why probability is the right language for the problem.

Do not say "uses graph learning" and stop. Explain what the nodes are, what the links mean, why neighbors carry evidence, and when that assumption breaks.

Every mathematical concept must answer three questions:

- What problem forced this idea into existence?
- What is the idea in everyday language?
- Why does this idea work for this family of papers?

Also explain the shape of the mathematical object in plain language:

- If the paper compares things, explain what "closeness" means and what gets lost when closeness is compressed into a number.
- If the paper ranks things, explain what counts as a better order and whose preference or goal defines "better."
- If the paper estimates probability, explain what is uncertain, what evidence changes the estimate, and where false certainty can enter.
- If the paper learns from examples, explain what pattern is being reused and why reuse may fail outside the examples.
- If the paper uses a graph, explain what counts as a node, what counts as a link, what information flows along links, and when links mislead.
- If the paper claims causality, explain the difference between two things moving together and one thing changing the other.
- If the paper uses privacy or security math, explain what information is intentionally hidden and what useful signal is still allowed through.
- If the paper uses efficiency or systems ideas, explain what scarce resource is being saved: time, memory, communication, human labeling, energy, or money.

The important concept behind a mathematical principle is usually a tradeoff. Name the tradeoff explicitly: accuracy versus cost, personalization versus privacy, speed versus completeness, fairness versus historical signal, exploration versus exploitation, compression versus detail, simple explanation versus predictive power, or local evidence versus global consistency.

For every mathematical concept, explain the important idea behind the principle:

- why the concept is needed at all
- what ordinary operation it performs, such as comparing, counting, averaging, scoring, matching, smoothing, routing, preserving, hiding, or compressing
- what mistake it is designed to avoid
- what mistake it can still introduce
- why many different-looking papers independently reach for it

Examples:

- Optimization means deciding what "wrong" means and changing controllable knobs to make that wrongness smaller.
- Probability means changing belief when evidence is partial, noisy, repeated, delayed, or biased.
- Similarity means choosing which differences matter and which can be ignored.
- Ranking means deciding whose goal defines a better order when only a few choices can be shown.
- Graph reasoning means deciding when relationships let evidence travel and when links lie.
- Causal inference means asking what would change if an action changed while tempting alternative explanations were held apart.
- Privacy math means controlling which useful signal may cross a boundary and which private fact must not be reconstructed from that signal.
- Systems math means budgeting scarce time, memory, communication, energy, money, or human attention.

## Rejection Criteria

Reject and regenerate any output that does these things:

- defines the paper only by its method name
- says "improves performance" without explaining what practical failure is reduced
- says "uses optimization/probability/graphs/attention/causality" without rebuilding the idea in everyday language
- lists papers without explaining the shared problem underneath them
- explains a benchmark result but not the real-world task the benchmark is standing in for
- uses jargon as a shortcut instead of translating it
- gives a payoff without limits or assumptions
- sounds like a generic abstract that could fit many papers

## Style

Use plain, concrete language. Avoid cliches, hype, and method-name worship. Banned unless unpacked immediately: embedding, latent space, token, gradient, low-rank, attention, contrastive, regularization, distribution shift, SOTA, benchmark, ablation, robust, framework, paradigm, leverage, causal effect, confounder, convex, differentiable, optimization, scalability.

Prefer everyday explanations: measuring closeness, sorting a pile, following a slope downhill, spreading evidence through a network, estimating chances from repeated cases, comparing like with like, balancing constraints, saving only the important parts, filling gaps from neighbors, and checking what must be true for the answer to be trusted.
