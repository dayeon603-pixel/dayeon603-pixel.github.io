"""CV content: hero, papers, leadership, honors, contact. Every line traces to a file Dayeon holds."""
from __future__ import annotations

HERO = """
<header class="hero"><div class="wrap">
<div>
<h1>Dayeon Kang</h1>
<p class="lede">I build AI systems and physical models, then test them until they break. One question runs through the work: does a system know when it is about to be wrong?</p>
<p>My first result on that question came from MetaMirage. Across 7 frontier language models, the ones that answered best were the worst at noticing a trap. Since then I have carried the same habit into everything else: register the pass mark, run the test, report the number that came back.</p>
<p>I run Arbiter, my registered company in Korea, which builds software that signs and records automated decisions. I chair the Seongnam Youth Council, where I turn the same questions into draft ordinances.</p>
<p>This page says what is built, what is only simulated and what is still a plan. Much of the company code sits in private repositories, and I can show it to reviewers on request.</p>
<div class="links"><a href="mailto:dayeon603@gmail.com">dayeon603@gmail.com</a><a href="https://github.com/dayeon603-pixel">GitHub</a><a href="https://orcid.org/0009-0006-4481-0277">ORCID</a><a href="https://arbiter.company">arbiter.company</a></div>
</div>
<div class="side"><img src="img/me.jpg" width="900" height="1236" alt="Portrait of Dayeon Kang"><p>Seongnam, Korea</p></div>
</div></header>
"""

PAPERS = [
    ("When Does One Temperature Suffice? The Sharpening Exponent as a Representational Mismatch", "Under review at IEEE ICASSP 2027. Single author."),
    ("Data Element Availability and the Condition-Dependent Axis of Medication-Safety Indicators", "Accepted as an e-poster at the Korean Society of Medical Informatics 2026 autumn conference. First author."),
    ("MetaMirage: A Mirage-Pair Benchmark for Metacognitive Monitoring in LLMs", "Submitted to the Google DeepMind and Kaggle AGI benchmark challenge, Metacognition track."),
    ("Closed-Form Optimal Streamwise Power Allocation in Liquid-Cooled Processors", "Manuscript. Extended abstract filed September 2026."),
    ("Localizing the Bottleneck in ARC-AGI-3: Dynamics are Learnable and Adaptable, but Goal Inference is the Binding Constraint", "Manuscript."),
    ("The Limits of Unlearning a Clean-Label Detection Backdoor: A Study on ESA's Streak-Detection De-poisoning Task", "Manuscript."),
    ("Structured Perturbation Stability: An Operator-Restricted Framework for Measuring Semantic Invariance in Transformer Architectures", "Unpublished manuscript."),
    ("Per-request energy attribution for large language model inference", "In draft."),
]

LEADERSHIP = [
    ("Chair, Seongnam Youth Council", "Since January 2025. Elected as a member by youth vote, then elected chair by the members."),
    ("Founder, Arbiter (아비터)", "Registered business in Korea."),
    ("Founder, Youths Unite", "International news reports and SDG education decks, published every two weeks."),
    ("Global Youth Goodwill Ambassador, Ethiopian Embassy programme", "16th cohort, February 2026 to January 2027. My SYNAPTIC writing on Ethiopia belongs to this term."),
]

HONORS = [
    ("2026 Korea Talent Award", "Selected for the central review interview, November 2026."),
    ("Global Logic and Reasoning Competition 2026", "Final Round qualifier."),
    ("8th Korea Code Fair Hackathon", "Reached the finals with team 영점, October 2026."),
    ("Embassy of the Philippines Award", "31st International Youth Diplomacy Forum (DIFOS), 2026."),
    ("Commendation, History category", "John Locke Essay Competition, 2025."),
    ("Speaker of the Gyeonggi Provincial Council Award", "5th Plastic-Free Competition, HOBY Korea, 2025."),
    ("Speaker of the Seoul Metropolitan Council Award", "4th Plastic-Free Competition, HOBY Korea, 2024."),
    ("Silver and Bronze, International Award for Young People", "Ministry of Gender Equality and Family, 2025 and 2024."),
    ("UN SDGs Global Leader", "KIECC UN SDG International Speech Competition, 2024."),
    ("Grand Prize, Top-Class Representative Figure", "ICAE International Conference on the Global Environment, 2024."),
]

FOOTER = """
<footer id="contact"><div class="wrap">
<h2>Say hello</h2>
<p><a href="mailto:dayeon603@gmail.com">dayeon603@gmail.com</a> or <a href="mailto:dayeon@arbiter.company">dayeon@arbiter.company</a></p>
<p><a href="https://github.com/dayeon603-pixel">github.com/dayeon603-pixel</a> · <a href="https://orcid.org/0009-0006-4481-0277">ORCID 0009-0006-4481-0277</a></p>
<p>Scripts and run records for anything on this page are available on request.</p>
</div></footer>
"""
