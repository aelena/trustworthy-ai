# E2E Problem definition and solution   

Based on the Lawler Model.

```mermaid
graph LR
    A[Implement Lawler Model for AI Problem Definition]
    A --> B[Understanding the Problem Space]
    A --> C[Data Consideration]
    A --> D[Algorithmic Choices]
    A --> E[Ethical Concerns]
    A --> F[Design and Implementation]

    B --> B1[Needs Assessment] 
    B1 -- results in --> B7[Problem Statement]
    B --> B2[Stakeholder Mapping]

    B -- presupposes --> B3[Alignment with Business Objectives] -- is guided by --> B14[AI Strategy]
    B --> B4[ROI Projection] -- supports --> B3
    B --> B5[Resource Assessment]
    B7 -- includes --> B15[Risk Analysis]
  
    B7 -- results in --> B9[Proposed Solution]
    B7 -- delivers --> B10[Implementation Plan]
    B7 -- documents --> B11[Expected Outcomes]

    C --> C1[Data Sourcing]
    C --> C2[Data Preprocessing]

    D --> D1[Model Selection]
    D --> D2[Machine Learning Methods]

    E --> E1[Ethical Assessment]
    E --> E2[Bias Mitigation]

    F --> F1[Prototype Development] -- validates --> F4[Business Case] 
    F --> F2[Iterative Design]
    F --> F3[Deployment Plan & CI/CD]
    F3 --> F5[Integrations]
    F3 --> F6[Monitoring]

 

```

<br/>
<br/>

- [Lawler Model for designing AI Products](https://cdotimes.com/2023/09/21/the-lawler-model-for-designing-ai-products-a-bloomberggpt-case-study/) - this is an ad-infested website, open with a blocker. 
- [Thinkable models](https://www.sciencedirect.com/science/article/abs/pii/S0732312396900048)