# Why Synthetic Data matters when auditing AI & ML Models

Synthetic data is increasingly used in AI and ML applications due to its ability to protect privacy and expand datasets for model training, and this is why even some data marketplaces are selling it. 

However, despite its benefits, the generation and use of synthetic data must adhere to both ethical standards and regulatory requirements. This section focuses on ensuring that synthetic data is used responsibly, addressing privacy, fairness, transparency, and legal compliance.

### **Transparency and Accountability**
  - **Disclosure**: Organizations should clearly disclose when synthetic data is used in AI models, especially in cases where it impacts consumers or stakeholders. Auditors should therefore assess whether the organization is providing clear and understandable explanations about how synthetic data is created, where they procured or sourced it, or how they generated it, why and how it’s being used, and what its limitations are. 
  - **Accountability**: Auditors should also ensure that accountability structures are in place, such as designated officers or teams responsible for ethical compliance in synthetic data usage.
  - **Governance**: Auditors should examine whether there is proper governance over the generation and use of synthetic data. Organizations should maintain detailed documentation about how synthetic data is generated, which real-world data was used, and how privacy and fairness risks are mitigated. This documentation should be made available during regulatory audits.
  - **Audit Trails and Traceability**: Organizations should be able to trace the origin of the data used to generate synthetic datasets, including the algorithms, tools, and methods used to create the data. Auditors should review these trails to ensure compliance with both regulatory and ethical standards.
  - **Third-Party Data Providers**: If synthetic data is sourced from third-party providers, auditors should ensure that these providers comply with applicable regulations and ethical standards. Contracts and agreements should outline the responsibilities of each party, and auditors should check for compliance with privacy laws and ensure that data-sharing agreements include provisions for the ethical use of synthetic data.

### **Data Privacy Compliance**: 
  - **Protection of Personal Information**: Synthetic data is often used to replace real user data to preserve privacy. However, auditors need to ensure that the synthetic data generation process doesn’t unintentionally reveal sensitive information, which could still violate privacy regulations like GDPR or CCPA.
  - **De-identification Auditing**: Auditors should check whether the synthetic data is truly anonymized and non-reversible (i.e., it cannot be re-engineered to reveal original data). Most likely this synthetic data - if it is any worth - will be derived from real-world individuals, therefore organizations should ensure that the original data subjects are informed that their data may be used to generate synthetic counterparts.

### **Bias and Fairness**:
  - **Bias in Synthetic Data Generation**: Synthetic data should be carefully audited for bias. If the generation process is flawed or the original dataset is biased, the synthetic data will inherit those issues, leading to fairness concerns in AI models. Auditors should assess whether organizations have processes in place to monitor and mitigate biases in synthetic data generation.
  - **Representative Data**: Auditors must ensure that the synthetic data still reflects a diverse and representative sample of the target population, maintaining fairness in model outcomes.

### **Data Quality and Validity**:
  - **Model Accuracy and Performance**: Synthetic data should maintain the characteristics of real data to ensure that AI models trained on it perform accurately in real-world scenarios. Auditors should assess how closely the synthetic data matches the statistical properties of the original data.
  - **Use in Testing and Validation**: Synthetic data is often used for testing and validating models. Auditors should verify that the synthetic data does not distort test results, leading to an inflated sense of model robustness or performance.

### **Security Risks**:
  - **Synthetic Data Leakage**: Synthetic data can introduce new attack vectors, such as model inversion or membership inference attacks, where adversaries attempt to infer original data from the synthetic model. Auditors should evaluate the security of synthetic data to prevent leakage.
   
### Regulatory and Ethical Compliance:
  - **Regulatory Auditing**: Depending on industry regulations, synthetic data might still fall under specific compliance rules. Auditors should be aware of the regulatory landscape surrounding synthetic data use, ensuring that it adheres to legal and ethical standards. Certain industries have sector-specific regulations that synthetic data must comply with. For example, in healthcare (under HIPAA) or financial services (under FINRA), there are stringent rules on how sensitive information can be handled, even when synthetic data is used. Specialized auditors need to evaluate compliance with these specific frameworks for audits in those domains.
  - **Ethical Considerations**: Even with synthetic data, ethical principles, such as consent and transparency, must be upheld. Auditors should verify that organizations using synthetic data communicate its use clearly and ethically to stakeholders.
   Data Minimization and Purpose Limitation:
   - **Data Minimization**: Auditors must ensure that synthetic data adheres to the principles of data minimization (only necessary data is collected and used) and purpose limitation (data is used only for the purpose it was collected for). Synthetic data should not be repurposed for uses that were not originally intended without proper regulatory approval or user consent.

<br/>

   # Possible Audit Questions

- What security protocols are in place during the generation of synthetic data to prevent unauthorized access to the original datasets?

- How is the synthetic data generation process protected from potential attacks (e.g., data leaks, re-identification attacks)?

- Has the organization conducted a formal re-identification risk assessment to ensure synthetic data cannot be reverse-engineered to reveal personal information?

- How often are assessments performed to check for vulnerabilities that could lead to re-identification of original data from synthetic datasets?

- Who has access to the synthetic data generation tools and the original datasets? Is access strictly controlled and monitored?

- Are there defined roles and responsibilities for individuals or teams handling synthetic data generation and security?

- Is the synthetic data generation process compliant with industry standards for data encryption and secure access control?

- What methods are used to anonymize or obfuscate the original data before generating synthetic data, and are these methods compliant with data privacy regulations?

- Does the synthetic data generation process ensure that the original data cannot be re-identified?

- Are individuals informed about the potential use of their data for generating synthetic datasets?

- Does the organization follow specific regulatory guidelines (e.g., GDPR’s pseudonymization requirements) when generating synthetic data? or, Is the synthetic data compliant with all relevant data privacy regulations (GDPR, CCPA, etc.)?

- Is there a detailed documentation process outlining how synthetic data is generated, including the source data, methods, and algorithms used?

- Can the organization provide an audit trail showing the complete lifecycle of the data, from its original form to its synthetic counterpart?

- What processes are in place to detect potential biases in the original datasets before generating synthetic data?

- How does the organization ensure that the synthetic data does not replicate or amplify biases from the original data?

- Are there processes in place to monitor for and mitigate bias in synthetic data?

- Does the synthetic data accurately represent the demographic diversity (e.g., age, gender, ethnicity) present in the original dataset? or at least that which is relevant to the model at hand?

- How does the organization validate that the synthetic data includes fair and representative samples across all relevant subgroups?

- What strategies or algorithms are employed to mitigate bias during the generation of synthetic data?

- Has the organization implemented bias detection tools to test synthetic datasets before using them for model training or testing?

- Are fairness audits regularly conducted on synthetic datasets, and how are the results documented and acted upon?

- What corrective actions are taken when biases or unfair patterns are identified in synthetic data?

- Are there systems in place to track whether synthetic data leads to biased outcomes in downstream AI models? 

- Can the organization provide an audit trail showing the complete lifecycle of the data, from its original form to its synthetic counterpart?

- Are cross-border transfers of synthetic data compliant with international data privacy laws?

- Does the organization have a process to update synthetic data practices based on evolving regulatory requirements?