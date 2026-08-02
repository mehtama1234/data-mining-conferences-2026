# Plain-language course spine shared by the generated data-mining pages.

COURSE_TITLE = "The Simple Search And Data Mining Course Spine"

COURSE_DEK = (
    "A long, plain essay for reading WWW, WSDM, SIGIR, and the wider data-mining "
    "conference set as one course: how people ask for information, how systems "
    "find and rank possible answers, why recommendations are not just search, "
    "why trust matters, and why these ideas matter in law, medicine, science, "
    "education, agents, business, and public life."
)

COURSE_SECTIONS = [
    {
        "kicker": "Start Here",
        "title": "The whole subject in one everyday question",
        "body": [
            "Data mining, web search, and information retrieval all start with one plain problem: there is too much information, and a person needs the right piece now. The information may be a web page, a product, a paper, a patient record, a legal case, a video, a post, a route, a document inside a company, or a fact that an agent needs before it acts.",
            "The computer does not begin with understanding. It begins with records: words, clicks, links, users, items, timestamps, images, ratings, citations, purchases, and logs. The work is to turn those records into evidence. Which records are related? Which ones answer the current need? Which ones should come first? Which ones are misleading, private, unfair, or unsafe?",
            "That is why first principles matter. A paper name or method name is not enough. The useful questions are simpler: what is being searched, what counts as relevant, what evidence is available, what is missing, what can be compared, what is being ranked, and what harm happens if the system is wrong?"
        ],
    },
    {
        "kicker": "The Main Loop",
        "title": "Find candidates, score them, order them, learn from what happened",
        "body": [
            "Most of this field follows one loop. First gather possible answers. Then score each one for the current person and need. Then order them. Then watch what happened: did the person click, read, buy, save, ignore, complain, or come back?",
            "Search does this when a query arrives. A first pass finds candidate documents. A second pass gives each candidate a better score. A final list appears. Recommendation does this without an explicit query: the system treats a person's history and current situation as the question. Advertising does it with money and auctions added. Agents do it when they retrieve memory or tools before answering.",
            "The loop is powerful because it turns a vague human need into smaller questions a computer can handle: what might help, which one looks best, and did the behavior afterward suggest that the choice worked?"
        ],
    },
    {
        "kicker": "Relevance",
        "title": "Relevance means this helps this person now",
        "body": [
            "Relevance is the heart of SIGIR. In everyday words, a result is relevant if it helps the person with the need they have right now. That sounds simple, but it is hard because the need is often hidden. The query may be short, ambiguous, misspelled, local, time-sensitive, or shaped by what the person already knows.",
            "The same words can mean different things. A doctor searching for 'jagged edge lung scan' needs something different from a student searching for the same phrase. A lawyer looking for precedent needs authority and exact wording. A shopper may care about price, delivery, brand, and trust. A researcher may want the newest paper, the most cited paper, or the paper that explains the idea best.",
            "This is why search is not just string matching. It is an evidence problem. The system must infer the need from words, context, past behavior, document signals, links, and feedback, then decide which result is most likely to help."
        ],
    },
    {
        "kicker": "Ranking",
        "title": "Ranking asks which useful thing should come first",
        "body": [
            "Ranking is the act of putting possible answers in order. It matters because people rarely inspect everything. The first few results shape what they learn, buy, believe, and do. A system can contain the right answer and still fail if it buries that answer too low.",
            "The first principle is that exact scores are usually less important than order. If one document scores 0.82 and another 0.79, the numbers themselves are not the point. The point is which one should be above the other. That is why ranking methods often learn from comparisons: this result was preferred over that one, this item was clicked before that item, this answer solved the need better than the alternative.",
            "Ranking also carries responsibility. The top result gets attention, sales, influence, and trust. So ranking is never only technical. It is also social and economic. It decides who is visible and what counts as credible."
        ],
    },
    {
        "kicker": "Similarity",
        "title": "Meaning becomes nearness",
        "body": [
            "A modern search or recommendation system often turns words, documents, users, products, and images into lists of numbers. The plain idea is this: place things in a space so that things with similar meaning sit near each other. Then finding a related item becomes finding a nearby point.",
            "This matters because people do not always use the same words as the answer. A query about 'cheap flights with flexible dates' may need documents that say 'low fare calendar'. A paper about 'retrieval augmented generation' may be useful for someone searching 'how to ground an LLM answer'. If meaning is stored as nearness, the system can find matches that word matching alone would miss.",
            "The risk is that nearness can be wrong. If the learned space has bad examples, bias, stale data, or missing context, it can place the wrong things together. So the first-principles question is always: near according to what evidence, for which purpose, and with what failure cost?"
        ],
    },
    {
        "kicker": "Recommendation",
        "title": "Recommendation is search without a typed question",
        "body": [
            "A recommender still answers a question, but the question is hidden. Instead of 'show me headphones', the system sees behavior: views, clicks, purchases, skips, watch time, follows, likes, and sessions. It asks what the person is likely to want next.",
            "The simplest idea is crowd evidence. If people with similar behavior liked an item, this person may like it too. A newer idea uses sequence: what someone did recently often matters more than what they did years ago. The system tries to understand the current mood, not just the long-term profile.",
            "Recommendation matters beyond entertainment and shopping. It shapes news, jobs, education, social feeds, research discovery, and which tools an agent decides to call. It can help people find useful things, but it can also trap them in narrow loops, overfit to short-term behavior, or reward content that gets attention without being good."
        ],
    },
    {
        "kicker": "Graphs",
        "title": "Connections are data",
        "body": [
            "Many data-mining problems are not just lists of items. They are webs of relationships. People follow people. Papers cite papers. Products are bought together. Pages link to pages. Users belong to groups. Facts connect entities. In these cases, the connections are not extra decoration. They are part of the meaning.",
            "A graph is just a way to store things and the links between them. The first principle is that linked things often share evidence. A paper cited by many useful papers may itself be useful. A suspicious account connected to many suspicious accounts deserves scrutiny. A product bought with another product may fit the same need.",
            "This appears everywhere: biology networks, supply chains, fraud rings, knowledge graphs, social media, road networks, citation maps, and agent memory. The practical question is whether the links are honest evidence or misleading shortcuts."
        ],
    },
    {
        "kicker": "Language Models",
        "title": "A language model can read, but it still needs evidence",
        "body": [
            "Large language models changed this field because they can read and write fluently. They can turn a messy question into a clearer one, summarize documents, explain results, generate answers, and act as part of a larger system. But fluency is not the same as truth.",
            "That is why retrieval is now even more important, not less. A model that answers from memory can sound confident and be wrong. A model that first looks up relevant evidence has a better chance of being grounded. This is the simple idea behind retrieval-augmented generation: find evidence first, answer from that evidence second.",
            "SIGIR becomes central in the agent era for this reason. Agents need memory, tools, documents, and facts. Every time an agent searches its memory or chooses which tool documentation to read, it is doing retrieval. Bad retrieval means bad action."
        ],
    },
    {
        "kicker": "Evaluation",
        "title": "A system is good only if it helps",
        "body": [
            "Evaluation asks whether the system actually helped. This is harder than it sounds. A click is evidence, but not perfect evidence. People click misleading headlines. They skip good results if the title is unclear. They may be satisfied without clicking. They may click because a bad result was placed first.",
            "So evaluation needs care. Offline tests use saved judgments or behavior logs. Online tests compare systems with real users. Benchmarks make methods easier to compare, but they can also become too narrow. A system can score well on a benchmark and still fail for a real person with a messy need.",
            "The first-principles test is simple: did the system reduce the user's work, improve the decision, protect against harm, and stay useful under real conditions?"
        ],
    },
    {
        "kicker": "Trust",
        "title": "The web is adversarial",
        "body": [
            "The field cannot assume the data is honest. Spammers try to rank higher. Fraud rings create fake behavior. Misinformation spreads. Bots imitate people. Sellers game reviews. Attackers try to extract private information. Bad feedback can teach the system the wrong lesson.",
            "Trust and safety work asks how to keep the loop from being poisoned. It looks for strange patterns, protects private data, checks claims, measures bias, explains decisions, and asks whether a change really caused an outcome or merely moved with it.",
            "This matters because search and recommendation are public infrastructure now. They shape what people know. A broken system does not only make a technical mistake. It can mislead patients, voters, students, customers, scientists, and policy makers."
        ],
    },
    {
        "kicker": "Why It Matters",
        "title": "The bigger picture across fields",
        "body": [
            "These ideas matter anywhere people face too much information. In medicine, retrieval finds patient evidence, trial results, symptoms, and similar cases. In law, it finds precedent and exact language. In science, it finds related work and missed connections. In education, it finds the explanation that fits the learner. In companies, it finds internal knowledge. In agents, it finds memory and tools before action.",
            "The same simple questions keep returning. What is the need? What evidence is available? What counts as relevant? Which candidates should be considered? Which should come first? What feedback can be trusted? What harm happens if the system is wrong?",
            "That is the value of reading WWW, WSDM, SIGIR, and KDD as one course. They are not only about web pages or papers. They are about how modern society routes attention, evidence, trust, and action through machines."
        ],
    },
]

