# Trustworthy AI

This repository tries to outline a comprehensive programme for setting up an in-house Trustworthy AI initiative or capability group. It's a wide and evolving topic that spans areas beyond technology itself, including ethics, law, social sciences and even philosophy. Therefore this lists the knowledge and capabilities the group of AI auditors should have. 

This takes inspiration from a large number of public papers (arxiv mostly) on the technical side of things, as well as document from regulators, think-tanks and other policy actors.

## Main structure

One could think of structuring this in two main tracks, the Technical (which covers some basics and includes adjacent areas in Security) and the Regulatory, which would include as well the ethical, social and philosophical. A third section covers specific skills for AI auditors.

## ToC

[Technical Track](#technical-track)
  - [AI / ML Fundamentals](#ai-and-ml-fundamentals)
  - [AI Development Lifecycle](#ai-development-lifecycle)
  - [Transparency and Explainability](#transparency-and-explainability)
  - [Reliability and Robustness](#reliability-and-robustness)
  - [The Security Aspect](#the-security-aspect)
    - [AI Security Fundamentals](#ai-security-fundamentals)
    - [Data Privacy and Security](#data-privacy-and-security-technical)
    - [AI Security and Adversarial AI](#ai-security-and-adversarial-ai)
  - [Model Validation and Testing](#model-validation-and-testing)
  - [On Syntethic data](#on-synthetic-data)

[Regulatory Track](#regulatory)
  - [Trustworthy AI](#trustworthy-ai)
  - [AI-Specific Regulations](#ai-specific-regulations)
  - [Data Privacy Protection](#data-privacy-protection)
  - [Synthetic Data Considerations](#synthetic-data-considerations)
  - [Governance](#governance)
    - [Ethical AI Principles](#ethical-ai-principles)
    - [Ethics Requirements](#ethics-requirements)
    - [AI Governance Frameworks](#ai-governance-frameworks)
    - [AI Safety](#ai-safety)
    - [Sustainability Considerations](#sustainability-considerations)

[On Auditing and Assessments](#auditing-and-assessments)
  - [Audit Planning and Scoping](#audit-planning-and-scoping)
  - [Risk management in AI Auditing](#risk-management-in-ai-auditing)
  - [Specialized AI Auditing Skills](#specialized-ai-auditing-skills)
  - [Bias Detection and Mitigation](#bias-detection-and-mitigation)
  - [Practical Skills and Tools](#practical-skills-and-tools)
    - [Programming for AI Auditing](#programming-for-ai-auditing)
    - [Visualization and Reporting](#visualization-and-reporting)
  - [Soft Skills for AI Auditors](#soft-skills-for-ai-auditors)

[Additional Stuff](#additional)
- [Tools, Templates, Checklists](#tools-templates-checklists)
- [Specialized Trainings](#specialized-trainings)
- [Other Books & Papers](#other-books--papers)
- [Vendor links](#vendor-links)

<br/>

__This document is necessarily work in progress and does not intend to be a final one stop shop__

<br/>

# Technical Track

## AI and ML Fundamentals

Get more than a passing familiarity with the underlying technology and main paradigms. 

- Introduction to AI and ML
  - [Basic concepts and terminology](https://medium.com/nlplanet/the-basic-concepts-and-terms-you-need-to-know-for-ai-and-ml-28eb07fd6c49)
- Types of ML and AI systems
  - Basic understanding of the types of Machine Learning: Supervised, Unsupervised, Semi-supervised, and Reinforcement Learning, Self-supervised, Online, Transfer etc
  - [Basic Algorithms](https://www.tableau.com/data-insights/ai/algorithms)
  - How AI, ML and Deep Learning are [related](./pages/ai_overview.md).
  - Neural networks ([FNN, RNN, CNN, LSTM](./pages/neural_networks_overview.md), [Transformer](https://arxiv.org/abs/1706.03762)) and [backpropagation](https://cklixx.people.wm.edu/teaching/math400/Annette-paper.pdf)
- Machine learning algorithms and techniques


## AI Development Lifecycle

Understand all the stages of the AI & ML Development Lifecycle and what each stage entails. [More detail here](./pages/aiml_dev_lifecycle.md)

- Data collection and preparation
- Labeling and augmentation
- Model selection and training - Choose the appropriate algorithm(s) based on the nature of the problem (e.g., classification, regression, clustering). This may involve selecting traditional machine learning models or deep learning architectures, depending on complexity and scale.
- Training phases
  - [Hyperparameter Tuning](https://arxiv.org/abs/2003.05689) : Adjust hyperparameters (e.g., learning rate, regularization factors) to optimize the model's performance. Techniques such as grid search, random search, or more advanced approaches like Bayesian optimization are often employed ([Hyperparameter Optimization For Compute Efficient Training](https://arxiv.org/abs/2306.08055), [Hyperparameters in Reinforcement Learning and How To Tune Them](https://arxiv.org/abs/2306.01324))
  - [Cross-Validation](./pages/cross_valid.md), to evaluate a model's performance and generalization ability. This allows to obtain a better estimate of a model's performance on previously unseen data compared to a classic train-test split. By testing the model on multiple subsets of data, cross-validation helps detect and prevent the classic issue of overfitting.
- Performance metrics - what were the performance metrics for the AI system.
  - [Metrics to evaluate ML algorithms](https://towardsdatascience.com/metrics-to-evaluate-your-machine-learning-algorithm-f10ba6e38234)
- Bias and Fairness testing
  - [Managing bias and unfairness in data for decision support](https://link.springer.com/article/10.1007/s00778-021-00671-8)
  - [Investigating Bias with a Synthetic Data Generator](https://arxiv.org/abs/2209.05889)
  - [Towards a Standard for Identifying and Managing Bias in Artificial Intelligence](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1270.pdf)
- Interpretability and Explainability
  - [Explaining Explanations: An Overview of Interpretability of Machine Learning](https://arxiv.org/pdf/1806.00069)
  - SHAP (Shapley Additive Explanations) - 
    - [original paper](https://arxiv.org/pdf/1705.07874) 
    - [site](https://shap.readthedocs.io/en/latest/)
  - LIME (Local Interpretable Model-agnostic Explanations)
    - [paper](https://arxiv.org/abs/1602.04938)
    - [paper with code](https://github.com/marcotcr/lime)
- Deployment and monitoring

## Transparency and Explainability

- Transparency and explainability - Techniques to make AI models more interpretable and their decisions more understandable, understand how models arrive at their decisions. Explainable AI (XAI) techniques: 
  - [Explainable Artificial Intelligence (XAI): What we know and what is left to attain Trustworthy Artificial Intelligence](https://www.sciencedirect.com/science/article/pii/S1566253523001148)
  - [XAI 2.0 paper](https://arxiv.org/abs/2310.19775)
  - [A Survey Of Methods For Explaining Black Box Models](https://arxiv.org/abs/1802.01933)
- [Algorithmic Transparency](https://en.wikipedia.org/wiki/Algorithmic_transparency) - Algorithmic transparency is high on the agenda for regulation (for example, [EU](https://algorithmic-transparency.ec.europa.eu/index_en), [EU Governance Framework for AT](https://www.europarl.europa.eu/RegData/etudes/STUD/2019/624262/EPRS_STU(2019)624262_EN.pdf), [UK](https://www.gov.uk/government/collections/algorithmic-transparency-recording-standard-hub)). As an auditor, ensure information about the algorithms used in AI systems is clear. Apart from techniques such as SHAP, LIME, XAI techniques (see above), basic lifecycle considerations apply, that is:   
  - Detailed records of algorithms used, decision criteria, data sources and preprocessing steps done, model architecture chosen and rationale and training procedures. Data lineage tools can support auditing this aspect of AI&ML models. 
  - For Black box models, providing query access to the model without exposing internal implementation
  - Transparency reports including regular updates on changes to AI systems and disclosure of known limitations or biases.

  More references [here](./pages/algo_trans.md)

- [Interpretability](https://www.managementsolutions.com/sites/default/files/minisite/static/22959b0f-b3da-47c8-9d5c-80ec3216552b/iax/pdf/explainable-artificial-intelligence-en-04.pdf) of AI/ML models
  - [An Overview](https://www.blog.trainindata.com/machine-learning-interpretability/)
  - [Distinguish](https://docs.aws.amazon.com/whitepapers/latest/model-explainability-aws-ai-ml/interpretability-versus-explainability.html) between Explainability and Interpretability
  - [The Mythos of Model Interpretability](https://arxiv.org/pdf/1606.03490)
  - [Making Sense of Machine Learning: A Review of Interpretation Techniques and Their Applications](https://www.mdpi.com/2076-3417/14/2/496)

- [Differential privacy](https://arxiv.org/abs/1412.7584)
- [Platform Observability](https://ojs.weizenbaum-institut.de/index.php/wjds/article/view/4_2_3) - this interesting paper seeks to go beyond Algorithmic Transparency to "_platform observability: a pragmatic and sociotechnical perspective aimed at securing structural, real-time access to the means of platform knowledge production_", applying the classic concept of Observability *as a pragmatic alternative to algorithm-centric models of platform transparency*. 

  As an auditor there are several [evidence gathering techniques](./pages/evidence_gather.md) available to you. 

## Reliability and Robustness
- Model performance evaluation - going beyond the [basic accuracy metrics](https://c3.ai/introduction-what-is-machine-learning/evaluating-model-performance/), such as precision, recall, F1-score, and AUC-ROC, to provide a holistic view of model performance
  - [cross-validation and other techniques](https://www.markovml.com/blog/model-evaluation-metrics) to ensure the model's performance is consistent across different subsets of data
- Error analysis and [debugging](https://www.markovml.com/blog/ml-model-debugging)
  - [Confusion Matrix Analysis](https://en.wikipedia.org/wiki/Confusion_matrix) which examines the types of errors (false positives, false negatives) to understand where the model struggles2.
  - Feature Importance: Analyzing which features contribute most to correct and incorrect predictions.
  - Error Patterns: Identifying systematic errors or biases in the model's predictions.
  - Debugging Techniques: Using techniques like gradient checking, learning curve analysis, and bias-variance decomposition to diagnose issues in model training and performance.
  -Interpretability Methods: Employing techniques like SHAP (SHapley Additive exPlanations) values or LIME (Local Interpretable Model-agnostic Explanations) to understand model decisions.
- Handling edge cases and outliers



## The Security aspect

### AI Security Fundamentals
- Threat modeling for AI systems
  - [MLSecOps](https://mlsecops.com/)
  - [Threat Modeling AI/ML Systems and Dependencies](https://learn.microsoft.com/en-us/security/engineering/threat-modeling-aiml)
  - [Threat Modelling and Risk Analysis for Large Language Model (LLM)-Powered Applications](https://arxiv.org/abs/2406.11007)

- Common attack vectors and vulnerabilities

### Data Privacy and Security (technical)

- Audit implementation of access controls, security measures, encryption techniques, and safeguards in place to protect data in AI/ML models. 
- How do AI systems manage data
- Anonymization techniques
- Securing data pipelines to prevent unauthorized access or breaches.

### AI Security and Adversarial AI

### Adversarial Attacks
- White Box & Black Box - https://deepgram.com/ai-glossary/adversarial-machine-learning
- Types of adversarial attacks - https://viso.ai/deep-learning/adversarial-machine-learning/
  - Evasion
  - Poisoning, data poisoning - a strategy where attackers inject corrupted data into the machine learning pipeline, causing the model to learn incorrect patterns and make erroneous predictions.
  - Model Extraction
- Understand techniques such as L-BFGS, FGSM, JSMA, Deepfool, [Carlini & Wagner Attack](https://arxiv.org/abs/1608.04644), how GANs can be used to generate adversarial attacks, Zeroth-order optimization attack and others.
- Generating and detecting [adversarial examples](https://arxiv.org/pdf/1712.07107)
  - Ability to create adversarial inputs for various types of AI models
  - Ability to assess AI models' resilience against adversarial attacks
- Defenses against adversarial attacks - understanding how techniques like adversarial training, defensive distillation and gradient masking/obfuscation work and are applied


### AI System Hardening
- Secure AI development practices
- Model and data protection techniques


<br/>

## On Synthetic data

- Understand the growing relevante of synthetic data
- Concerns around Synthetic Data Generation and Security
- Presence of Bias in Synthetic Data
- Validation and Testing with Synthetic Data 

<br/>

# Regulatory

## Trustworthy AI

[On the idea of TAI](./pages/trustworthy_ai.md)

-  [EU HLEG AI Guidelines](https://digital-strategy.ec.europa.eu/en/library/ethics-guidelines-trustworthy-ai)
- [China CAICT White Paper on TAI](http://www.caict.ac.cn/english/research/whitepapers/202110/P020211014399666967457.pdf)

## Legal and Regulatory Compliance

- Need to have an understanding of the different AI regulations or frameworks (e.g., [EU AI Act](https://www.europarl.europa.eu/topics/en/article/20230601STO93804/eu-ai-act-first-regulation-on-artificial-intelligence), [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)) referenced elsewhere in this document, in order to leverage them and understand which ones might apply in each specific audit scenario.
- Sector-specific AI regulations, use cases and applications.There are many of those. Some relevant examples:
  - [Financial Industry Regulatory Authority (FINRA) AI/ML Guidelines](https://www.finra.org/rules-guidance/key-topics/fintech/report/artificial-intelligence-in-the-securities-industry/ai-apps-in-the-industry). The notes to this document provide additional sector-specific links
  - AI in credit scoring and fraud detection, with its own set of biases and risks
  - Algorithmic trading and risk management
  - [In HR and Hiring](https://www.eeoc.gov/laws/guidance/americans-disabilities-act-and-use-software-algorithms-and-artificial-intelligence)
  - In Healthcare, with specializations such as AI in medical diagnosis and treatment planning and its plethora of accompanying ethical and data privacy considerations.
  - Manufactoring, IoT, such as AI in predictive maintenance and quality control or safety considerations for AI-powered robotics

## Data Privacy Protection
- [GDPR](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32016R0679), [CCPA](https://cppa.ca.gov/regulations/pdf/cppa_act.pdf) and other relevant data protection regulations
- Associated risks and Privacy-preserving AI techniques
  - [Privacy Risks of General-Purpose AI Systems](https://arxiv.org/abs/2407.02027)

## Model Validation and Testing

- Testing for performance
- Testing for reliability
- Testing for compliance with expected/stated outcomes

## [Synthetic Data Considerations](./pages/synth_data.md)

- Data Privacy and Synthetic Data
- Ethical and Regulatory Compliance in Synthetic Data Usage

## Governance

Good overview and understanding of the main topics around Ethics and Governance and what Regulators, think-tanks and industry groups of interest are putting out that affects the evaluation and assessments of models, and also guides the auditor be aligned in terms of compliance and potential certification of AI & ML models. 

Understand as well the social, economical, ethical and philosophical derivations of the technology.

- Accountability and responsibility

### Ethical AI Principles

Basic guidance such as that provided by the [OECD AI Policy Observatory](https://oecd.ai/en/) and its [AI Principles](https://oecd.ai/en/ai-principles) will help any organization put in place their own principles as well as offer a guide as to what aspects to look for and evaluate in AI/ML models. 

- Fairness and non-discrimination - Group and Individual Fairness, techniques to mitigate bias in training data and model outputs. Bias Detection and Mitigation and methods to identify and reduce unfair bias in AI systems.
  - [The Fairness and ML Book](https://fairmlbook.org/)
  - [A Survey on Bias and Fairness in Machine Learning](https://arxiv.org/abs/1908.09635)

- Data Privacy considerations. General sound privacy and data protection regulation and standard guidelines apply here; collect and use only the necessary data for AI system functionality, protect sensitive data.

### Ethics Requirements
  - [EU AI HLEG - High-level expert group on artificial intelligence](https://digital-strategy.ec.europa.eu/en/policies/expert-group-ai)
  - [IEEE Ethically Aligned Design](https://standards.ieee.org/wp-content/uploads/import/documents/other/ead_v2.pdf)
  - [Ethical Requirements for AI Systems](https://www.researchgate.net/publication/339886423_Ethical_Requirements_for_AI_Systems)


  

### AI Governance Frameworks
- Regulatory landscape and compliance requirements
  - [EU AI Act](https://www.europarl.europa.eu/topics/en/article/20230601STO93804/eu-ai-act-first-regulation-on-artificial-intelligence), a comprehensive first-of-its-kind regulation categorizing AI systems based on risk levels and imposing corresponding requirements
  - [General Data Protection Regulation (GDPR)](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=celex%3A32016R0679)
  - [The AIGA AI Governance Framework](https://ai-governance.eu/)
  - [Putting AI Ethics into Practice: The Hourglass Model of Organizational AI Governance](https://arxiv.org/abs/2206.00335) (paper)
  - [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework), which focuses on managing risks associated with AI systems and rovides guidance on governance, mapping, measuring, and managing AI risks / [standard (PDF)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
  - [OECD Principles on Artificial Intelligence](https://www.oecd.org/en/topics/policy-issues/artificial-intelligence.html), emphasizes human-centered values and fairness
  - [European Commission's Ethics Guidelines for Trustworthy AI](https://op.europa.eu/en/publication-detail/-/publication/d3988569-0434-11ea-8c1f-01aa75ed71a1), which is part of the EU's broader AI strategy
Emphasizes seven key requirements: human agency and oversight, technical robustness, privacy and data governance, transparency, diversity and fairness, societal well-being, and accountability
- Industry standards and best practices
  - [IEEE  Standard Model Process for Addressing Ethical Concerns during System Design  (IEEE Std 7000–2021)](https://ieeexplore.ieee.org/document/9536679)
  - [IEEE Global Initiative on Ethics of Autonomous and Intelligent Systems](https://standards.ieee.org/industry-connections/activities/ieee-global-initiative/), which provides a comprehensive set of ethical principles for AI development and covers areas such as transparency, accountability, and privacy protection ([pdf](https://ieee-sa.imeetcentral.com/p/eAAAAAAASwyHAAAAAFNa5fs))
  - [ISO Standards for AI](https://www.iso.org/sectors/it-technologies/ai)
  - [ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html)
  - [ISO/IEC 23894:2023](https://www.iso.org/standard/77304.html) for AI Risk Management
  - [ISO/IEC 23053:2022](https://www.iso.org/standard/74438.html)
- Organizational AI governance structures
  - [AIGA](https://ai-governance.eu/ai-governance-framework/the-ai-governance-lifecycle/)
  - [Defining organizational AI governance](https://link.springer.com/content/pdf/10.1007/s43681-022-00143-x.pdf) (open access journal article)
  - [Toward AI Governance: Identifying Best Practices and Potential Barriers and Outcomes](https://link.springer.com/article/10.1007/s10796-022-10251-y)



### AI Safety
- Risk assessment and mitigation strategies
- Fail-safe mechanisms and graceful degradation
- Long-term AI safety considerations
  - All of AI 6 AGI Existential Safety risks papers by [Roman V. Yampolskiy](https://scholar.google.com/citations?user=0_Rq68cAAAAJ&hl=en). It's a long list, and amazing reads. 

### Sustainability Considerations

<br/>


# Auditing and Assessments

## Audit Planning and Scoping
- Defining audit objectives and scope
- Risk assessment for AI systems
- Developing audit criteria and checklists

### Risk management in AI Auditing

- Identifying, assessing, and mitigating risks specific to AI models

### Audit Execution Techniques
- Data sampling and analysis
- Model evaluation and testing
- Documentation review and stakeholder interviews

### Reporting and Remediation
- Audit report writing
- Communicating findings and recommendations
- Follow-up and remediation tracking

### AI Auditing Tools and Platforms
- Overview of commercial and open-source auditing tools
- Hands-on experience with selected tools


## Specialized AI Auditing Skills

## Bias Detection and Mitigation
- [Types of AI bias](./pages/types_ai_bias.md)
- Bias measurement techniques
  - [De-biasing "bias" measurement](https://arxiv.org/abs/2205.05770)
- Strategies for reducing bias in AI systems
  - [Mitigating bias in artificial intelligence](https://www.sciencedirect.com/science/article/pii/S0167739X24000694)

### AI Performance Metrics
- Selecting appropriate evaluation metrics
- Benchmarking and comparative analysis
- Continuous monitoring of AI systems

### AI Documentation and Traceability
- Model cards and datasheets
- Version control for AI models and datasets
- Audit trail maintenance



## Practical Skills and Tools

### Programming for AI Auditing
- Basic Python for data analysis and model inspection
- Using libraries for fairness and explainability (such as [AI Fairness 360](https://aif360.res.ibm.com/) ([paper](https://arxiv.org/abs/1810.01943)) or SHAP)

### Visualization and Reporting
- Data visualization techniques for AI audit findings
- Creating effective audit reports and dashboards

## Soft Skills for AI Auditors

Many Soft Skills for AI Auditors overlap with those needed in strategy consulting, project management, and risk management, especially in high-stakes settings and/or C-levels. One thing for sure is AI auditors need to stay up-to-date with the latest AI technologies, methodologies, and regulatory changes, whereas it might not be the case in more traditional industries or sectors. 

- Communicating AI decisions to stakeholders


### Communication and Stakeholder Management
- Explaining technical concepts to non-technical audiences, or mixed audiences composed of including data scientists, ethicists, and domain experts.
- Communicating with stakeholders who may have varying levels of AI literacy and different concerns about AI/ML systems
- Negotiation and conflict resolution in audit scenarios
- Sector-specific knowledge

### Critical & Ethical Decision Making
- Ability to critically evaluate AI-generated outputs, identify potential biases, and exercise independent judgment in the context of AI without yielding to mental lazyness or AI authority syndrom.
- Develop a healthy skepticism towards AI-generated insights and answers. This point, and the previous one, will most often require solid foundational skills plus specialized domain knowledge. 
- Navigating ethical dilemmas in AI auditing, including biases, fairness, social and business impact 
- Balancing competing interests and priorities

<br/>

# Additional 

## Tools, Templates, Checklists

- [Self-Assessment list for Trustworthy AI (ALTAI)](https://ec.europa.eu/newsroom/dae/document.cfm?doc_id=68342) (direct PDF download)
- [Data Ethics Canvas](https://theodi.org/news-and-events/blog/data-ethics-canvas/)
- [AI Ethics Policy Template](https://www.aiguardianapp.com/ai-ethics-policy-template)
- [AI Ethics Toolkit](https://www.hum-dseg.org/ai-applied-ethics-toolkit)
- [Assessment List for Trustworthy AI (ALTAI)](https://op.europa.eu/en/publication-detail/-/publication/73552fcd-f7c2-11ea-991b-01aa75ed71a1)
- [NOREA Guiding Principles Trustworthy AI Investigations](https://www.norea.nl/uploads/bfile/a344c98a-e334-4cf8-87c4-1b45da3d9bc1)
- [UK A Guide to ICO Audit Artificial Intelligence (AI) Audits](https://ico.org.uk/media/for-organisations/documents/4022651/a-guide-to-ai-audits.pdf)
- [AI Incident Database](https://incidentdatabase.ai/)
- [LatticeFlow's](https://latticeflow.ai/solutions/ai-assessments/) - for example involved in the [EU AI Act compliance assessment](https://opentools.ai/news/eu-ai-act-compliance-checker-reveals-tech-giants-weak-spots?utm_source=opentoolsai-newsletter&utm_medium=newsletter&utm_campaign=ai-compliance-shocker&_bhlid=6fb422971ae5f7227094d0d7914074df7eaf8b5c)
- [Toolkit for "TrustLLM: Trustworthiness in Large Language Models"](https://github.com/HowieHwong/TrustLLM)
- [AuditNLG: Auditing Generative AI Language Modeling for Trustworthiness (Salesforce)](https://github.com/salesforce/AuditNLG)


<br/>

## Specialized Trainings

- [ISACA](https://www.isaca.org/resources/artificial-intelligence)
- [Theiia Auditing Artificial Intelligence (AI): A Hands-On Course for Internal Auditors](https://www.theiia.org/en/products/learning-solutions/course/auditing-artificial-intelligence-ai-a-hands-on-course-for-internal-auditors/)
- [Theiia Essentials for AI Auditing](https://www.theiia.org/en/products/learning-solutions/course/internal-auditing-in-the-age-of-artificial-intelligence/)
- [Babl Courses](https://babl.ai/courses/)
- [Trustworthy Generative AI Coursera](https://www.coursera.org/learn/trustworthy-generative-ai)
- [Coursera Responsible Generative AI Specialization](https://www.coursera.org/specializations/responsible-generative-ai)

<br/>

## Other Books & Papers

- [Trustworthy AI, AI+Security Papers](https://github.com/nuaa-nlp/TrustworthyAIPapers)
- [Debugging Machine Learning Models with Python](https://www.amazon.es/Debugging-Machine-Learning-Models-Python/dp/1800208588) / ([github repo](https://github.com/PacktPublishing/Debugging-Machine-Learning-Models-with-Python))
- [Towards a Business Case for AI Ethics](https://jyx.jyu.fi/bitstream/handle/123456789/93508/agbeseym.pdf?sequence=1&isAllowed=y) (direct PDF download). Also available as part of this Open Access Book, [Software Business](https://link.springer.com/book/10.1007/978-3-031-53227-6)
- [The intersection of Responsible AI and ESG](https://www.csiro.au/-/media/D61/Responsible-AI/Alphinity/Responsible-AI-and-ESG.pdf)
- [Artificial Intelligence Ethics, Governance and policy challenges - CEPS Task Force Report](https://cdn.ceps.eu/wp-content/uploads/2019/02/AI_TFR.pdf)


<br/>


## Vendor links

- Azure - [What is Responsible AI?](https://learn.microsoft.com/en-us/azure/machine-learning/concept-responsible-ai?view=azureml-api-2)
- AWS - https://aws.amazon.com/ai/generative-ai/security/
- SGS - [Trustworthiness of AI](https://www.sgs.com/en/whitepapers/trustworthiness-of-ai-form)
- SGS - [White Paper: Trustworthy AI, Privacy and Security](https://www.sgs.com/en/whitepapers/trustworthy-ai-privacy-and-security-in-ai-form)

