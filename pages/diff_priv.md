# Differential Privacy

> **Code Examples**: See [differential_privacy.py](../code/differential_privacy.py) for practical implementations using Opacus (PyTorch) and TensorFlow Privacy, including privacy accounting and DP-SGD training.

Differential privacy is a concept in data privacy that ensures the protection of individual data while allowing for the release of statistical information about a dataset. That is, it provides a way to release information about a dataset without revealing information about specific individuals in the data. It works by adding noise to data and query results, such that the query accuracy is retained but no user data is leaked. That math magic is achieved by calculating the patterns of groups within the dataset without disrupting information about individuals in the dataset. 

The challenge lies in not impacting negatively the accuracy of the model. The higher the level of privacy that differential privacy can provide, the lower the model's accuracy. Differential privacy can be implemented using various techniques such as adding noise to data, using differentially private mechanisms, and applying differential privacy to machine learning models. 

Differential Privacy matters to AI & ML auditors for several reasons:

- **Privacy protection assessment**: Auditors need to evaluate how well AI and ML models protect individual privacy. Differential privacy provides a rigorous mathematical framework for quantifying privacy guarantees, allowing auditors to assess the strength of privacy protection in a model.

- **Compliance verification**: As privacy regulations become more stringent, auditors need to verify if models comply with legal requirements. Knowledge of differential privacy can help auditors determine if a model meets specific privacy standards.

- **Risk evaluation**: Auditors must identify potential privacy risks in AI and ML systems. Understanding differential privacy helps in assessing the risk of information leakage or individual re-identification from model outputs.

- **Best practices implementation**: Auditors should be able to recommend best practices for privacy-preserving machine learning. Differential privacy is considered a gold standard in this area, making it crucial for auditors to understand and recommend its implementation where appropriate.

- **Trade-off analysis**: Differential privacy involves a trade-off between privacy and utility. Auditors need to understand this balance to evaluate if a model achieves an appropriate level of privacy without significantly compromising its performance or utility / accuracy. 

- **Technical evaluation**: Auditors may need to review the implementation of privacy-preserving techniques in ML models. Knowledge of differential privacy algorithms and mechanisms (like DP-SGD) is essential for this technical evaluation.

- **Emerging trends awareness**: As AI and ML evolve, new privacy-preserving techniques are developed. Understanding differential privacy helps auditors stay current with these advancements and assess their effectiveness.

A scenario where DP is important is where a company needs to learn about its user community without leaking individual data in that learning, that is, not learn about specific individual. See [this from Apple](https://www.apple.com/privacy/docs/Differential_Privacy_Overview.pdf) to learn more about this use case.

## Techniques


| Technique | Description | Best Used For | Key Characteristics | Libraries |
|-----------|-------------|----------------|---------------------|-----------|
| Laplace Mechanism | Adds Laplace-distributed noise to numeric results | Numeric queries, aggregate statistics | Simple, widely used, pure ε-DP | Diffprivlib, OpenDP, [Google DP](https://github.com/google/differential-privacy) |
| Gaussian Mechanism | Adds Gaussian-distributed noise to results | Numeric queries, ML applications | (ε,δ)-DP, analytical properties | Diffprivlib, TensorFlow Privacy, Opacus |
| Exponential Mechanism | Probabilistically selects output based on quality score | Non-numeric data, selection tasks | Versatile, handles categorical data | Diffprivlib, OpenDP |
| Randomized Response | Respondents randomly choose to answer truthfully or randomly | Surveys with sensitive topics | Provides plausible deniability | Diffprivlib, Google DP |
| Sample and Aggregate | Splits data, computes on subsamples, then aggregates | Complex queries, large datasets | Can improve accuracy for some queries | OpenDP |
| Private Multiplicative Weights | Iteratively updates a distribution over data domain | Answering many linear queries | Efficient for high-dimensional data | OpenDP |
| Local Differential Privacy | Applies noise at individual data point level | Untrusted data sources, distributed systems | Strong privacy, often lower accuracy | [Google DP](https://github.com/google/differential-privacy) |
| Objective Perturbation | Adds noise to optimization objective functions | Privacy-preserving machine learning | Useful for empirical risk minimization | Diffprivlib |
| DP-SGD | Clips gradients and adds noise during model training | Training ML models with privacy | Standard for DP deep learning | Opacus, TensorFlow Privacy |
| Smooth Sensitivity | Adapts noise based on local data sensitivity | Queries sensitive to small changes in data | Can improve utility for some queries | OpenDP |

Note that this list is not exhaustive, and some libraries may support additional techniques or variations of these methods. Additionally, new libraries and implementations are continually being developed in this rapidly evolving field.


## Citations

- [A Practical Guide to Machine Learning with
Differential Privacy](https://arxiv.org/pdf/2303.00654.pdf)
- [Differential privacy in deep learning: Privacy and beyond](https://www.sciencedirect.com/science/article/abs/pii/S0167739X23002315)
- [Google Repo for DP](https://github.com/google/differential-privacy), which contains further links to explore the topic. 
- [DP-Auditorium: a Large Scale Library for Auditing Differential Privacy](https://arxiv.org/abs/2307.05608), and code for the [library](https://github.com/google/differential-privacy/tree/main/python/dp_auditorium)
- [NIST Blog Series on Differential Privacy](https://www.nist.gov/itl/applied-cybersecurity/privacy-engineering/collaboration-space/blog-series/differential-privacy)
- [Differential privacy in deep learning: Privacy and beyond](https://www.researchgate.net/publication/371515293_Differential_privacy_in_deep_learning_Privacy_and_beyond)
- [An Introduction to Various Privacy Models](https://cdn.ttgtmedia.com/rms/security/Mobile%20Security%20and%20Privacy_ch%2011.pdf)
- [Differential Privacy and Machine Learning: a Survey and Review](https://arxiv.org/abs/1412.7584)

<br/>

- https://www.private-ai.com/en/2022/10/18/the-basics-of-differential-privacy-its-applicability-to-nlu-models/
- https://www.craft.ai/en/post/the-key-to-un-risk-model-deployment-unpacking-differential-privacy
- https://towardsdatascience.com/understanding-differential-privacy-85ce191e198a?gi=ec8e64b0f733
- https://clanx.ai/glossary/differential-privacy-in-ai
- https://www.anonos.com/blog/what-is-differential-privacy-definition-mechanisms-examples
- https://research.google/blog/making-ml-models-differentially-private-best-practices-and-open-challenges/
- https://www.sciencedirect.com/topics/computer-science/differential-privacy

- https://www.craft.ai/en/post/the-key-to-un-risk-model-deployment-unpacking-differential-privacy
- https://www.ai4europe.eu/research/ai-catalog/diffprivlib-ibm-differential-privacy-library
- https://blog.openmined.org/a-survey-of-differential-privacy-frameworks/
- https://research.ibm.com/blog/ibm-differential-privacy-library-the-single-line-of-code-that-can-protect-your-data
- https://github.com/IBM/differential-privacy-library
- https://research.kudelskisecurity.com/2020/03/11/differential-privacy-a-comparison-of-libraries/
- https://www.sciencedirect.com/topics/computer-science/differential-privacy
- https://pydp.readthedocs.io/en/latest/introduction.html