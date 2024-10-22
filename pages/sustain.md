# AI Model Sustainability Concerns

There are two key topics in this dimension for the AI model auditor.

- Understand the sustainability concerns and trends around AI & ML models. Obvious things like high energy consumption (resource intensity) and commensurate carbon footprint, both in training and in use.

  - [Towards Sustainability of AI – Identifying Design Patterns for Sustainable Machine Learning Development](https://www.researchgate.net/publication/384071507_Towards_Sustainability_of_AI_-_Identifying_Design_Patterns_for_Sustainable_Machine_Learning_Development/link/66e95304dde50b3258789769/download)
  - [Towards Sustainable Artificial Intelligence: An Overview of Environmental Protection Uses and Issues](https://arxiv.org/pdf/2212.11738)
  - [A Survey on AI Sustainability: Emerging Trends on Learning Algorithms and Research Challenges](https://arxiv.org/abs/2205.03824)
  - [Broadening the perspective for sustainable AI: Sustainability criteria and indicators for Artificial Intelligence systems](https://arxiv.org/pdf/2306.13686)
  - [Sustainable AI: Environmental Implications, Challenges and Opportunities](https://www.researchgate.net/publication/355843251_Sustainable_AI_Environmental_Implications_Challenges_and_Opportunities)
  - [Beyond Efficiency: Scaling AI Sustainably](https://arxiv.org/pdf/2406.05303)
  - [Towards Green Automated Machine Learning: Status Quo and Future Directions](https://arxiv.org/abs/2111.05850)
  - [Artificial intelligence - driven sustainable development: Examining organizational, technical, and processing approaches to achieving global goals](https://www.diva-portal.org/smash/get/diva2:1807287/FULLTEXT01.pdf)
  - [Sustain Magazine](https://algorithmwatch.org/en/wp-content/uploads/2022/06/SustAIn_Magazine_2022_EN.pdf)
  - [Efficiency is Not Enough: A Critical Perspective of Environmentally Sustainable AI](https://arxiv.org/abs/2309.02065)
  - [Towards Green AI: Current Status and Future Research](https://arxiv.org/pdf/2407.10237)
  - [A systematic review of Green AI](https://wires.onlinelibrary.wiley.com/doi/pdfdirect/10.1002/widm.1507)
  - [Towards Green Metaverse Networking Technologies, Advancements and Future Directions](https://www.researchgate.net/publication/365189427_Towards_Green_Metaverse_Networking_Technologies_Advancements_and_Future_Directions)
  - [ChatGPT Needs SPADE (Sustainability, PrivAcy, Digital divide, and Ethics) Evaluation: A Review](https://arxiv.org/abs/2305.03123)


- Understand tools and techniques to measure and assess the sustainability impact of AI models. Key metrics include runtime, which relates to energy consumption and can be used to estimate environmental impact, especially when combined with data on energy consumption and the energy mix. CPU/GPU (Central/Graphical Processing Units) hours are suggested as a quantifiable measure that can be converted into CO2eq emissions with knowledge of the energy mix. The industry and academia still seem to not have converged on a set of comprehensive sustainability metrics and standardization in measuring and reporting power, energy, carbon emissions data in AI. 
  
  - [Estimating the Sustainability of AI models based on theoretical models and experimental data](https://www.researchgate.net/publication/370283228_ESTIMATING_THE_SUSTAINABILITY_OF_AI_MODELS_BASED_ON_THEORETICAL_MODELS_AND_EXPERIMENTAL_DATA/link/644945f8809a5350212c866c/download?_tp=eyJjb250ZXh0Ijp7ImZpcnN0UGFnZSI6InB1YmxpY2F0aW9uIiwicGFnZSI6InB1YmxpY2F0aW9uIn19).
  - [OECD Report - Measuring the environmental impacts of artificial intelligence compute and applications](https://www.oecd.org/en/publications/measuring-the-environmental-impacts-of-artificial-intelligence-compute-and-applications_7babf571-en.html).
  - [Quantifying the Carbon Emissions of Machine Learning](https://arxiv.org/abs/1910.09700) - this paper offers simple key metrics to assess GHG impact through  factors such as the location of the servers used for training and the energy grid or mix used, the length of the training, and even the make and model of hardware on which the training takes place. 
  - [Data-Centric Green AI: An Exploratory Empirical Study](https://arxiv.org/abs/2204.02766) - explores that not all algorithms are equal, obviously, and that modifications in datasets can have dramatic impacts.
  - [Towards energy-efficient Deep Learning: An overview of energy-efficient approaches along the Deep Learning Lifecycle](https://arxiv.org/pdf/2303.01980) - Examines DLLCE, deep learning lifecycle efficiency and life cycle recognition efficiency.
  - [New universal sustainability metrics to assess edge intelligence](https://www.sciencedirect.com/science/article/pii/S2210537921000718)
  - [Towards a Methodology and Framework for AI Sustainability Metrics](https://dl.acm.org/doi/abs/10.1145/3604930.3605715) - (open access)

<br/>

# Key Metrics

| **Sustainability Metrics**         | **Pros**                                                                                                                                   | **Cons**                                                                                                    |
|------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| **CO2-equivalents (CO2eq)**        | - Standardized measure for quantifying carbon emissions from ML model training.                                                            | - May be challenging to measure directly.                                                                   |
|                                    | - Highlights geographical disparities in carbon emissions.                                                                                 | - Emphasis on practical constraints when implementing sustainability measures.                              |
|                                    | - CPU/GPU hours can be converted into CO2eq emissions with knowledge of the energy mix.                                                    |                                                                                                             |
| **Electricity Consumption**        | - FLOPS/W metric provides insights into hardware efficiency.                                                                               | - Measuring energy usage can be challenging.                                                                |
|                                    | - Highlights variations in energy efficiency among hardware devices and AI algorithms.                                                     | - Trade-offs between accuracy and energy in larger datasets.                                                |
| **Carburacy**                      | - Novel carbon-aware accuracy measure for NLP models.                                                                                      | - Larger inputs can increase energy consumption.                                                            |
|                                    | - Strikes a balance between accuracy and environmental impact.                                                                             | - Training batch size and decoding strategy choices involve trade-offs.                                     |
|                                    | - Considers effectiveness, cost, and efficiency.                                                                                           | - Model type can impact sustainability.                                                                     |
| **Universal Sustainability Metrics**| - Recognition Efficiency balances accuracy, complexity, and energy consumption.                                                            | - Emphasis on practical constraints when implementing sustainability measures.                              |
|                                    | - Training Efficiency prioritises energy efficiency.                                                                                       | - Balancing efficiency and environmental impact can be challenging.                                         |
|                                    | - Deep Learning Lifecycle Efficiency assesses model efficiency throughout its lifecycle. Classification system (Class A, B, C, D) for sustainability. |                                                                                                             |



[Source](https://medium.com/version-1/the-green-algorithm-measuring-sustainability-in-ai-4c775e811c2a)