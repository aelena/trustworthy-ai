# Trustworthy AI

This is a collection of links, documents attempting to outline a comprehensive programme for setting up an in-company Trustworthy AI initiative or capability. It's a wide and evolving topic that spans areas beyond technology itself, including ethics, law, social sciences and even philosophy. 

__This document is necessarily work in progress and does not intend to be a final one stop shop__



## Basics

### AI and ML Fundamentals

Get more than a passing familiarity with the underlying technology and main paradigms. 

- Introduction to AI and ML
  - [Basic concepts and terminology](https://medium.com/nlplanet/the-basic-concepts-and-terms-you-need-to-know-for-ai-and-ml-28eb07fd6c49)
- Types of ML and AI systems
  - Types of Machine Learning: Supervised, Unsupervised, Semi-supervised, and Reinforcement Learning, Self-supervised, Online, Transfer
  - Deep Learning
  - Neural networks (FNN, RNN, CNN, [Transformer](https://arxiv.org/abs/1706.03762)) and [backpropagation](https://cklixx.people.wm.edu/teaching/math400/Annette-paper.pdf)
- Machine learning algorithms and techniques


### AI Development Lifecycle
- Data collection and preparation
- Labeling and augmentation
- Model selection and training - Choose the appropriate algorithm(s) based on the nature of the problem (e.g., classification, regression, clustering). This may involve selecting traditional machine learning models or deep learning architectures, depending on complexity and scale.
- Training phases
  - Hyperparameter Tuning: Adjust hyperparameters (e.g., learning rate, regularization factors) to optimize the model's performance. Techniques such as grid search, random search, or more advanced approaches like Bayesian optimization are often employed.
  - Cross-Validation
- Performance metrics - what were the performance metrics for the AI system.
  - [Metrics to evaluate ML algorithms](https://towardsdatascience.com/metrics-to-evaluate-your-machine-learning-algorithm-f10ba6e38234)
- Bias and Fairness testing
  - [Managing bias and unfairness in data for decision support](https://link.springer.com/article/10.1007/s00778-021-00671-8)
  - [Investigating Bias with a Synthetic Data Generator](https://arxiv.org/abs/2209.05889)
  - [Towards a Standard for Identifying and Managing Bias in Artificial Intelligence](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1270.pdf)
- Interpretability and Explainability
  - [Explaining Explanations: An Overview of Interpretability of Machine Learning](https://arxiv.org/pdf/1806.00069)
  - SHAP (Shapley Additive Explanations) - SHAP is a model-agnostic tool for explaining the output of machine learning models. It assigns each feature in a prediction a contribution value, using concepts from cooperative game theory (specifically Shapley values). SHAP values show how much each feature positively or negatively influenced the prediction, providing transparency even in complex models like neural networks or ensemble methods.
    - [original paper](https://arxiv.org/pdf/1705.07874) 
    - [site](https://shap.readthedocs.io/en/latest/)
  - LIME (Local Interpretable Model-agnostic Explanations) - SHAP is a model-agnostic tool for explaining the output of machine learning models. It assigns each feature in a prediction a contribution value, using concepts from cooperative game theory (specifically Shapley values). SHAP values show how much each feature positively or negatively influenced the prediction, providing transparency even in complex models like neural networks or ensemble methods.
    - [paper](https://arxiv.org/abs/1602.04938)
    - [paper with code](https://github.com/marcotcr/lime)
- Deployment and monitoring


## AI Ethics and Governance

### Ethics Requirements
  - [EU AI HLEG - High-level expert group on artificial intelligence](https://digital-strategy.ec.europa.eu/en/policies/expert-group-ai)
  - [IEEE Ethically Aligned Design](https://standards.ieee.org/wp-content/uploads/import/documents/other/ead_v2.pdf)
  - [Ethical Requirements for AI Systems](https://www.researchgate.net/publication/339886423_Ethical_Requirements_for_AI_Systems)

### Ethical AI Principles
- Fairness and non-discrimination - Group and Individual Fairness, techniques to mitigate bias in training data and model outputs. Bias Detection and Mitigation and methods to identify and reduce unfair bias in AI systems.
  - [The Fairness and ML Book](https://fairmlbook.org/)
  - [A Survey on Bias and Fairness in Machine Learning](https://arxiv.org/abs/1908.09635)
- Transparency and explainability - Techniques to make AI models more interpretable and their decisions more understandable, understand how models arrive at their decisions. Explainable AI (XAI) techniques: 
  - [Explainable Artificial Intelligence (XAI): What we know and what is left to attain Trustworthy Artificial Intelligence](https://www.sciencedirect.com/science/article/pii/S1566253523001148)
  - [XAI 2.0 paper](https://arxiv.org/abs/2310.19775)
  - [A Survey Of Methods For Explaining Black Box Models](https://arxiv.org/abs/1802.01933)
- Algorithmic Transparency - providing clear information about the algorithms used in AI systems
- Interpretable ML models
- Privacy and data protection - standard guidelines apply here; collect and use only the necessary data for AI system functionality, protect sensitive data.
  - [Differential privacy](https://arxiv.org/abs/1412.7584)
- Accountability and responsibility
- Communicating AI decisions to stakeholders


- https://digital-strategy.ec.europa.eu/en/library/ethics-guidelines-trustworthy-ai
- [Self-Assessment list for Trustworthy AI (ALTAI)](https://ec.europa.eu/newsroom/dae/document.cfm?doc_id=68342) (direct PDF download)

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

## Trustworthy AI

### Reliability and Robustness
- Model performance evaluation - going beyond the [basic accuracy metrics](https://c3.ai/introduction-what-is-machine-learning/evaluating-model-performance/), such as precision, recall, F1-score, and AUC-ROC, to provide a holistic view of model performance
  - [cross-validation and other techniques](https://www.markovml.com/blog/model-evaluation-metrics) to ensure the model's performance is consistent across different subsets of data
- Error analysis and [debugging](https://www.markovml.com/blog/ml-model-debugging)
  - [Confusion Matrix Analysis](https://en.wikipedia.org/wiki/Confusion_matrix) which examines the types of errors (false positives, false negatives) to understand where the model struggles2.
  - Feature Importance: Analyzing which features contribute most to correct and incorrect predictions.
  - Error Patterns: Identifying systematic errors or biases in the model's predictions.
  - Debugging Techniques: Using techniques like gradient checking, learning curve analysis, and bias-variance decomposition to diagnose issues in model training and performance.
  -Interpretability Methods: Employing techniques like SHAP (SHapley Additive exPlanations) values or LIME (Local Interpretable Model-agnostic Explanations) to understand model decisions.
- Handling edge cases and outliers

### AI Safety
- Risk assessment and mitigation strategies
- Fail-safe mechanisms and graceful degradation
- Long-term AI safety considerations
  - All AI 6 AGI Safety risks papers by [Roman V. Yampolskiy](https://scholar.google.com/citations?user=0_Rq68cAAAAJ&hl=en). It's a long list. 


## AI Security and Adversarial AI

### AI Security Fundamentals
- Threat modeling for AI systems
  - [MLSecOps](https://mlsecops.com/)
  - [Threat Modeling AI/ML Systems and Dependencies](https://learn.microsoft.com/en-us/security/engineering/threat-modeling-aiml)
  - [Threat Modelling and Risk Analysis for Large Language Model (LLM)-Powered Applications](https://arxiv.org/abs/2406.11007)

- Common attack vectors and vulnerabilities

### Adversarial Attacks
- White Box & Black Box - https://deepgram.com/ai-glossary/adversarial-machine-learning
- Types of adversarial attacks - https://viso.ai/deep-learning/adversarial-machine-learning/
  - Evasion
  - Poisoning, data poisoning - a strategy where attackers inject corrupted data into the machine learning pipeline, causing the model to learn incorrect patterns and make erroneous predictions.
  - Model Extraction
- Understand techniques such as L-BFGS, FGSM, JSMA, Deepfool, Carlini & Wagner Attack, how GANs can be used to generate adversarial attacks, Zeroth-order optimization attack and others.
- Generating and detecting adversarial examples
  - Ability to create adversarial inputs for various types of AI models
  - Ability to assess AI models' resilience against adversarial attacks
- Defenses against adversarial attacks - Proficiency in applying techniques like adversarial training, defensive distillation and gradient masking/obfuscation

### AI System Hardening
- Secure AI development practices
- Model and data protection techniques

## AI Auditing Methodologies

### Audit Planning and Scoping
- Defining audit objectives and scope
- Risk assessment for AI systems
- Developing audit criteria and checklists

### Audit Execution Techniques
- Data sampling and analysis
- Model evaluation and testing
- Documentation review and stakeholder interviews

### Reporting and Remediation
- Audit report writing
- Communicating findings and recommendations
- Follow-up and remediation tracking

## Specialized AI Auditing Skills

### Bias Detection and Mitigation
- [Types of AI bias](./pages/types_ai_bias.md)
- Bias measurement techniques
  - [De-biasing "bias" measurement](https://arxiv.org/abs/2205.05770)
- Strategies for reducing bias in AI systems

### AI Performance Metrics
- Selecting appropriate evaluation metrics
- Benchmarking and comparative analysis
- Continuous monitoring of AI systems

### AI Documentation and Traceability
- Model cards and datasheets
- Version control for AI models and datasets
- Audit trail maintenance

## Legal and Regulatory Compliance

### AI-Specific Regulations
- Need to have an understanding of the different AI regulations or frameworks (e.g., EU AI Act, NIST AI Risk Management Framework) referenced elsewhere in this document, in order to leverage them and understand which ones might apply in each specific audit scenario.
- Sector-specific AI regulations (e.g., finance, healthcare). There are many of those. Some relevant examples:
  - [Financial Industry Regulatory Authority (FINRA) AI/ML Guidelines](https://www.finra.org/rules-guidance/key-topics/fintech/report/artificial-intelligence-in-the-securities-industry/ai-apps-in-the-industry). The notes to this document provide additional sector-specific links
  - [In HR and Hiring](https://www.eeoc.gov/laws/guidance/americans-disabilities-act-and-use-software-algorithms-and-artificial-intelligence)

### Data Protection and Privacy Laws
- GDPR and other relevant data protection regulations
- Privacy-preserving AI techniques
  - [Privacy Risks of General-Purpose AI Systems](https://arxiv.org/abs/2407.02027)


## Industry-Specific AI Applications
These would be specializations

### Financial Services
- AI in credit scoring and fraud detection
- Algorithmic trading and risk management

### Healthcare
- AI in medical diagnosis and treatment planning
- Ethical considerations in healthcare AI

### Manufacturing and IoT
- AI in predictive maintenance and quality control
- Safety considerations for AI-powered robotics

## Practical Skills and Tools

### AI Auditing Tools and Platforms
- Overview of commercial and open-source auditing tools
- Hands-on experience with selected tools

### Programming for AI Auditing
- Basic Python for data analysis and model inspection
- Using libraries for fairness and explainability (e.g., AI Fairness 360, SHAP)

### Visualization and Reporting
- Data visualization techniques for AI audit findings
- Creating effective audit reports and dashboards

## Soft Skills for AI Auditors

### Communication and Stakeholder Management
- Explaining technical concepts to non-technical audiences
- Negotiation and conflict resolution in audit scenarios

### Ethical Decision Making
- Navigating ethical dilemmas in AI auditing
- Balancing competing interests and priorities

## Readings (Books and papers)


## Trainings


## Vendor links

- AWS - https://aws.amazon.com/ai/generative-ai/security/

