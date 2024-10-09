## Evidence gathering for AI auditors

Many aspects listed below are not so far from technical due dilligence of conventional systems. An example of a [possible checklist](https://fastdatascience.com/downloads/Technical-due-diligence-report-template-1.pdf) for inspiration (direct PDF download) will cover many of the below.

[This is another one](https://www.edpb.europa.eu/system/files/2024-06/ai-auditing_checklist-for-ai-auditing-scores_edpb-spe-programme_en.pdf) (direct PDF download) based on EU regulatory building blocks.

**Black-box testing**
- Constructing arbitrary inputs and observing system outputs
- Analyzing input-output pairs for patterns or inconsistencies
- Systematically vary inputs to explore the system's behavior across different scenarios. 

Prompt engineering techniques can be used here, especially those that seek to create inputs specifically designed to challenge or potentially "break" the system.

Generative AI or synthetic data can be used as well to construct inputs that might be difficult to do manually.

**Documentation review**
- Examining technical documentation of AI/ML systems. 
- Verifying the presence and completeness of [AI transparency](https://www.ibm.com/think/topics/ai-transparency) reports.AI transparency means understanding how artificial intelligence systems make decisions, why they produce specific results, and what data they're using. Simply put, AI transparency is like providing a window into the inner workings of AI, helping people understand and trust how these systems work. It is said there are [three levels of AI Transparency](https://lup.lub.lu.se/search/files/126635664/Three_Levels_of_AI_Transparency_Accepted_Version.pdf), Algorithmic, Interaction and Social. 

As an auditor you want to understand a set of information that comprises information on the following, at least:
  - Stated Purpose
  - Risk levels
  - Model policies
  - Model generation
  - Intended domain
  - Training data that has been used
  - Training and testing accuracy
  - Identified Biases
  - Adversarial robustness metrics
  - Fairness metrics
  - Explainability metrics
  - Contact information

**Interviews with developers**
- Understand the documented design choices and rationale behind the AI system. Or uncover other choices that are not explicit
- Verifying understanding of potential biases or limitations (complementing already identified and disclosed ones)

**Data analysis**
- Reviewing data sources and preprocessing steps (refer to the [AI & ML Lifecycle page](./aiml_dev_lifecycle.md))
- Examining [data lineage](https://arxiv.org/abs/2407.14390) to understand how data flows through the system. Data lineage refers to the detailed tracking of data's origins, movement, and transformations throughout its lifecycle—from its source, through the various stages of processing, to its final usage in an AI or ML model. It helps in understanding the flow of data and the changes it undergoes as it moves across different processes. In the context of AI & ML, data lineage is crucial for  transparency, accountability, and trust in model outcomes, ensuring, as an auditor, that all steps are properly documented and verifiable:

  - Data Provenance: documented origin of data, acquisition timestamp, curation processes, metadata, pruning criteria, normalization etc. 
  - Data transformation, normally ETL tools will record logs of every data transformation and movement through the pipeline
  - Data pipeline information, documentation of every process in the data pipeline, such as feature engineering, model training, and testing stages. 
  - Recorded transformations applied during feature engineering. This includes encoding of categorical variables, scaling, dimensionality reduction (e.g., PCA), or text preprocessing (e.g., tokenization).
  - Model training logs, including batch sizes, epochs, and data splits (train/test/validation). Logs should capture model input data, feature sets, and parameters used during training
  - Metadata management, which can include data formats, timestamps, transformations applied, and any intermediate results, ensuring that lineage is well-documented


**Model performance metrics**
- Collecting and analyzing metrics across different demographic groups
- Looking for unexplained variations in performance

**Bias audits**
- Conducting specific tests designed to uncover hidden biases.
  - Similar to PII and other sensitive data, identify protected attributes (demographic, socioeconomic, disabilities, even geographical locations)
  - Check for imbalances in data used for training (content, sources, languages, social contexts). Calculatnig the proportions of each group in the dataset can be enough.
- Using validation datasets tailored to detect fairness issues

**Continuous monitoring**
- Implementing systems to track AI performance over time
- Looking for drift or unexpected changes in behavior

**Outputs of Explainability tools**
- Analyzing the results of XAI techniques applied to the system
- Verifying that explanations are consistent and meaningful

**Compliance checks**
- Verifying adherence to relevant regulations and standards
- Checking for implementation of required transparency measures

**Fuzzing**


### Links

- [From Transparency to Accountability and Back: A Discussion of Access and
Evidence in AI Auditing](https://arxiv.org/pdf/2410.04772v1)
- [The Data Provenance Initiative: A Large Scale Audit of Dataset Licensing & Attribution in AI](https://arxiv.org/abs/2310.16787)