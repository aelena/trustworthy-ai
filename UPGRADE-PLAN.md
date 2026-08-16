# Upgrade plan

*Opened 16 August 2026, after a six-month gap since the last substantive change.*

A body of knowledge that is not reviewed on a cadence is a body of knowledge that quietly becomes wrong. This file exists so that staleness is visible instead of implicit, and so the next review has somewhere to start.

## Done in this pass

- **`tai-lab/` and `.github/workflows/` published.** Both had been sitting untracked. An entire working companion application was absent from the repository.
- **Licensing made explicit.** MIT for `code/` and `tai-lab/`; CC BY 4.0 for the prose in `pages/`. A body of knowledge nobody may legally reuse is not doing its job.
- **EU AI Act timeline corrected** in `pages/agentic_safety.md` and `pages/transparency.md`. This was the most consequential piece of staleness in the repository — see below.
- **Repository hygiene**: `.gitignore` (there was none), `.gitattributes`, badges, and the status block in the README.

### On the AI Act correction

The material described the high-risk regime without dates. Read in August 2026 that implied the 2 August 2026 deadline was live, which it is not.

The Digital Omnibus on AI entered into force on 27 July 2026 and deferred the high-risk obligations to **2 December 2027** for stand-alone systems and **2 August 2028** for systems embedded in products. The Article 50 transparency duties were **not** deferred and apply from August 2026.

Sources: [Council of the EU press release](https://www.consilium.europa.eu/en/press/press-releases/2026/05/07/artificial-intelligence-council-and-parliament-agree-to-simplify-and-streamline-rules/) · [DLA Piper analysis](https://knowledge.dlapiper.com/dlapiperknowledge/globalemploymentlatestdevelopments/2026/The-Digital-AI-Omnibus-Proposed-deferral-of-high-risk-AI-obligations-under-the-AI-Act) · [Data Protection Report](https://www.dataprotectionreport.com/2026/07/the-eu-ai-act-when-does-it-become-enforceable-now/) · [European Commission](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)

Verify against a primary source before relying on any of this in an engagement. Timelines in this area have already moved once.

## Needs your judgement

These require decisions or knowledge I should not invent.

| Area | What to check | Why it matters |
|---|---|---|
| **Agentic safety** | `pages/agentic_safety.md` is the fastest-moving page in the repository and the most recently written. Six months is a long time here. Threat taxonomy, sandboxing patterns and the tool-use failure modes all deserve a re-read. | It is also the page most likely to be read by a buyer, because it is the topic everyone is currently confused about. |
| **Frontier model evaluations** | The evaluation section predates the current generation of model cards and public eval suites. Check whether the frameworks cited are still the ones people use. | Cited-but-superseded frameworks are the fastest way to look out of date. |
| **NIST AI RMF** | The Generative AI Profile is cited as "the 2024 profile". Confirm whether it has been revised. | One-line fix if so. |
| **OWASP Top 10 for LLM Applications** | Cited as v2025. Check for a newer revision. | One-line fix if so. |
| **ISO/IEC 42001** | Certification practice has had a year to mature. Worth a paragraph on what auditors are actually asking for now, which is the kind of detail that separates this from a link farm. | Directly useful to the advisory positioning. |
| **`code/` modules** | Five substantial modules (adversarial testing, bias, differential privacy, eval frameworks, explainability). No tests, no CI, no dependency pinning. | Currently they read as illustrative rather than runnable. Deciding which they are is a positioning choice. |

## Structural suggestions

**Put a review date on each page.** A one-line front matter — `last-reviewed: 2026-08` — makes staleness visible per page instead of per repository, and turns the next review into a sorted worklist rather than a re-read of everything.

**Decide what `code/` is for.** Either it is illustrative, in which case say so at the top of each module and stop worrying about it, or it is a toolkit, in which case it needs tests, pinned dependencies and CI. The ambiguity is the only thing that is actually a problem.

**Consider the packaged version.** ~25 pages of structured material on a subject with rising regulatory pressure is a plausible paid PDF, and the `c-tiktoken/book/` build pipeline in the adjacent repository would carry over almost unchanged. Deliberately not done here — it is a positioning decision, not a maintenance task.

## Review cadence

Quarterly is the right rhythm for this material: fast enough that the agentic-safety and regulatory sections do not embarrass anyone, slow enough that it does not become a second job.

Next review: **November 2026.**
