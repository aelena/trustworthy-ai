_This comes from Perplexity_

## Purpose and Benefits

Cross-validation serves several important purposes:

1. **Model Evaluation**: It provides a more accurate estimate of a model's performance on unseen data compared to a simple train-test split[1][2].

2. **Preventing Overfitting**: By testing the model on multiple subsets of data, cross-validation helps detect and prevent overfitting[3].

3. **Model Selection**: It allows for comparison between different models to select the best performing one[2].

4. **Hyperparameter Tuning**: Cross-validation can be used to optimize model hyperparameters[2].

## Common Cross-Validation Techniques

There are several types of cross-validation methods:

### K-Fold Cross-Validation

This is one of the most popular techniques:

1. The dataset is divided into k equal-sized folds. “k” is simply the number that dictates how many subsets a dataset is split into
2. The model is trained on k-1 folds and tested on the remaining fold.
3. This process is repeated k times, with each fold serving as the test set once.
4. The final performance metric is the average of all k iterations[1][4].

### Holdout Method

The simplest and most well-known form of cross-validation:

- The dataset is split into training and testing sets, typically in a 70-30 or 80-20 ratio.
- The model is trained on the training set and evaluated on the test set[1].

### Leave-One-Out Cross-Validation ([LOOCV](https://machinelearningmastery.com/loocv-for-evaluating-machine-learning-algorithms/))

A special case of k-fold cross-validation:

- k is set to the number of data points in the dataset.
- Each data point serves as the test set once, while the rest of the data is used for training[1].

### Stratified K-Fold Cross-Validation

Similar to k-fold, but ensures that the proportion of samples for each class is preserved in each fold. This is particularly useful for imbalanced datasets[3].

## Implementation Considerations

When implementing cross-validation:

1. **Choose the right k**: Typically, 5 or 10 folds are used, balancing bias and computational cost[4].

2. **Randomization**: Ensure data is shuffled before splitting into folds to avoid any ordering bias.

3. **Stratification**: For classification problems, consider using stratified cross-validation to maintain class proportions.

4. **Repeated Cross-Validation**: For more robust results, the entire cross-validation process can be repeated multiple times with different random splits[4].

5. **Time Series Data**: Special techniques like time series cross-validation should be used for temporal data to maintain the chronological order.

<br/>

## Summary

| Technique | Pros | Cons |
|-----------|------|------|
| K-Fold Cross-Validation | - Provides robust performance estimate<br>- Efficient use of data<br>- Less sensitive to data partitioning<br>- Good balance of bias and variance | - Can be computationally expensive<br>- May not work well for small datasets<br>- Assumes data points are independent |
| Holdout Method | - Simple and quick to implement<br>- Less computationally intensive<br>- Good for large datasets | - High variance in performance estimate<br>- Inefficient use of data<br>- Sensitive to how data is partitioned |
| Leave-One-Out Cross-Validation (LOOCV) | - Uses maximum amount of training data<br>- Deterministic (no random subsampling)<br>- Good for small datasets | - Very computationally expensive<br>- High variance for large datasets<br>- Can overestimate model performance |
| Stratified K-Fold Cross-Validation | - Maintains class proportion in each fold<br>- Reduces bias for imbalanced datasets<br>- Provides more reliable performance estimate | - Slightly more complex to implement<br>- May not be necessary for balanced datasets<br>- Can be computationally expensive |


Citations:
[1] https://www.javatpoint.com/cross-validation-in-machine-learning
[2] https://www.coursera.org/articles/what-is-cross-validation-in-machine-learning
[3] https://www.geeksforgeeks.org/cross-validation-machine-learning/
[4] https://neptune.ai/blog/cross-validation-in-machine-learning-how-to-do-it-right
[5] https://machinelearningmastery.com/k-fold-cross-validation/
[6] https://datascientest.com/en/the-importance-of-cross-validation
[7] https://towardsdatascience.com/cross-validation-in-machine-learning-72924a69872f?gi=e1023f00259b

## Other sources

These are sources I think offer good overviews of what Cross Validation is and how to apply it.

- [Scikit - Cross-validation: evaluating estimator performance](https://scikit-learn.org/stable/modules/cross_validation.html)
- [Is K-fold cross validation the best model selection method for Machine Learning?](https://arxiv.org/abs/2401.16407)
- [Azure - Configure training, validation, cross-validation, and test data in automated machine learning](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-configure-cross-validation-data-splits?view=azureml-api-1)
- [The Ultimate Guide To Cross-Validation In Machine Learning](https://www.simplilearn.com/tutorials/machine-learning-tutorial/cross-validation)
- [Cross-Validation in Machine Learning: How to Do It Right](https://neptune.ai/blog/cross-validation-in-machine-learning-how-to-do-it-right)

