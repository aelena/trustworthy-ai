"""
=============================================================================
BIAS TESTING AND FAIRNESS ASSESSMENT IN MACHINE LEARNING
=============================================================================

This module provides comprehensive examples of bias detection and mitigation
techniques using two industry-standard libraries: IBM's AI Fairness 360 (AIF360)
and Microsoft's Fairlearn.

CONCEPTUAL BACKGROUND
---------------------
Bias in machine learning refers to systematic errors that result in unfair
outcomes for certain groups of people. These biases can manifest at various
stages of the ML pipeline:

1. DATA BIAS: Historical prejudices encoded in training data
2. ALGORITHMIC BIAS: Model architectures that amplify certain patterns
3. EVALUATION BIAS: Metrics that don't capture fairness concerns
4. DEPLOYMENT BIAS: Feedback loops that reinforce unfair outcomes

FAIRNESS DEFINITIONS
--------------------
There are multiple, sometimes conflicting, definitions of fairness:

- DEMOGRAPHIC PARITY: Equal positive prediction rates across groups
  P(Y_pred=1|A=0) = P(Y_pred=1|A=1)

- EQUALIZED ODDS: Equal true positive and false positive rates across groups
  P(Y_pred=1|Y=1,A=0) = P(Y_pred=1|Y=1,A=1)  (equal opportunity)
  P(Y_pred=1|Y=0,A=0) = P(Y_pred=1|Y=0,A=1)  (equal FPR)

- CALIBRATION: Predictions should be equally accurate across groups
  P(Y=1|Y_pred=p,A=0) = P(Y=1|Y_pred=p,A=1) for all p

- INDIVIDUAL FAIRNESS: Similar individuals should receive similar predictions

WHY THIS MATTERS FOR TRUSTWORTHY AI
-----------------------------------
Bias testing is critical for:
- Regulatory compliance (EU AI Act, EEOC guidelines)
- Avoiding reputational and legal risks
- Building systems that work equitably for all users
- Identifying blind spots in model development

Libraries Used:
- aif360: IBM's comprehensive fairness toolkit
- fairlearn: Microsoft's fairness assessment and mitigation library
- scikit-learn: For baseline model training

Installation:
    pip install aif360 fairlearn scikit-learn pandas numpy matplotlib
"""

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# =============================================================================
# SECTION 1: DATA PREPARATION
# =============================================================================
"""
We'll create a synthetic dataset that mimics a credit scoring scenario.
This dataset intentionally contains bias to demonstrate detection techniques.

The scenario: A bank uses ML to predict loan approval.
Protected attribute: Gender (0 = Female, 1 = Male)
Target: Loan approved (0 = No, 1 = Yes)

The synthetic data is constructed with historical bias where:
- Males have a higher base approval rate
- This reflects historical lending discrimination
"""

def create_biased_dataset(n_samples=5000, random_state=42):
    """
    Create a synthetic dataset with intentional bias for demonstration.

    This function generates data where the protected attribute (gender)
    influences the outcome (loan approval) beyond what would be justified
    by the legitimate features (income, credit score, etc.).

    Parameters:
    -----------
    n_samples : int
        Number of samples to generate
    random_state : int
        Random seed for reproducibility

    Returns:
    --------
    pd.DataFrame
        Dataset with features, protected attribute, and target
    """
    np.random.seed(random_state)

    # Generate protected attribute (gender: 0=Female, 1=Male)
    # Slightly imbalanced to reflect real-world data
    gender = np.random.binomial(1, 0.52, n_samples)

    # Generate legitimate features
    # Income: Males historically earn more (reflecting real-world wage gap)
    income = np.where(
        gender == 1,
        np.random.normal(65000, 20000, n_samples),  # Male income distribution
        np.random.normal(55000, 18000, n_samples)   # Female income distribution
    )
    income = np.clip(income, 20000, 200000)  # Realistic bounds

    # Credit score: Assume no inherent gender difference
    credit_score = np.random.normal(680, 80, n_samples)
    credit_score = np.clip(credit_score, 300, 850)

    # Employment years
    employment_years = np.random.exponential(5, n_samples)
    employment_years = np.clip(employment_years, 0, 40)

    # Debt-to-income ratio
    debt_ratio = np.random.beta(2, 5, n_samples) * 0.6  # 0-60% range

    # Age (correlated with employment years)
    age = 22 + employment_years + np.random.normal(5, 3, n_samples)
    age = np.clip(age, 18, 75)

    # GENERATE BIASED TARGET VARIABLE
    # The bias is introduced by making gender directly influence approval
    # beyond what the legitimate features would predict

    # Calculate a "fair" score based on legitimate factors
    fair_score = (
        0.3 * (income - 50000) / 50000 +           # Income contribution
        0.3 * (credit_score - 600) / 200 +          # Credit score contribution
        0.2 * (employment_years / 10) +             # Employment contribution
        0.2 * (1 - debt_ratio / 0.6) +              # Debt ratio contribution
        np.random.normal(0, 0.2, n_samples)         # Random noise
    )

    # ADD BIAS: Gender directly influences outcome
    # This represents historical discrimination in lending
    biased_score = fair_score + 0.25 * gender  # Males get a boost

    # Convert to binary outcome
    approval_prob = 1 / (1 + np.exp(-biased_score * 2))
    approved = np.random.binomial(1, approval_prob)

    # Create DataFrame
    df = pd.DataFrame({
        'age': age,
        'income': income,
        'credit_score': credit_score,
        'employment_years': employment_years,
        'debt_ratio': debt_ratio,
        'gender': gender,           # Protected attribute
        'approved': approved        # Target variable
    })

    return df

# Create the dataset
print("=" * 70)
print("CREATING SYNTHETIC BIASED DATASET")
print("=" * 70)
df = create_biased_dataset(n_samples=5000)

print("\nDataset Shape:", df.shape)
print("\nFeature Statistics:")
print(df.describe().round(2))

print("\n" + "-" * 70)
print("INITIAL BIAS ASSESSMENT (Raw Statistics)")
print("-" * 70)

# Simple bias check: Compare approval rates by gender
approval_by_gender = df.groupby('gender')['approved'].agg(['mean', 'count'])
approval_by_gender.index = ['Female', 'Male']
print("\nApproval Rates by Gender:")
print(approval_by_gender)

disparity = approval_by_gender.loc['Male', 'mean'] / approval_by_gender.loc['Female', 'mean']
print(f"\nDisparate Impact Ratio: {disparity:.3f}")
print(f"(Values < 0.8 or > 1.25 typically indicate potential discrimination)")


# =============================================================================
# SECTION 2: AI FAIRNESS 360 (AIF360)
# =============================================================================
"""
AIF360 is IBM's comprehensive toolkit for detecting and mitigating bias.

Key Concepts in AIF360:
-----------------------
1. DATASETS: Special data structures that track protected attributes
2. METRICS: Classes to compute various fairness measures
3. ALGORITHMS: Pre-processing, in-processing, and post-processing techniques

AIF360 Fairness Metrics:
------------------------
- Statistical Parity Difference: Difference in positive prediction rates
- Disparate Impact: Ratio of positive prediction rates
- Equal Opportunity Difference: Difference in true positive rates
- Average Odds Difference: Average of TPR and FPR differences
- Theil Index: Measure of inequality in benefit allocation
"""

print("\n" + "=" * 70)
print("SECTION 2: AI FAIRNESS 360 (AIF360) ANALYSIS")
print("=" * 70)

try:
    from aif360.datasets import BinaryLabelDataset
    from aif360.metrics import BinaryLabelDatasetMetric, ClassificationMetric
    from aif360.algorithms.preprocessing import Reweighing, DisparateImpactRemover
    from aif360.algorithms.postprocessing import EqOddsPostprocessing

    AIF360_AVAILABLE = True
    print("\nAIF360 successfully imported!")

except ImportError:
    AIF360_AVAILABLE = False
    print("\nWARNING: AIF360 not installed. Install with: pip install aif360")
    print("Skipping AIF360 examples...")

if AIF360_AVAILABLE:
    # -------------------------------------------------------------------------
    # 2.1 Create AIF360 Dataset
    # -------------------------------------------------------------------------
    """
    AIF360 uses special dataset objects that explicitly track:
    - Protected attributes (e.g., gender, race)
    - Privileged groups (e.g., male, white)
    - Favorable labels (e.g., approved, hired)

    This explicit tracking enables systematic fairness analysis.
    """

    print("\n" + "-" * 70)
    print("2.1 Creating AIF360 BinaryLabelDataset")
    print("-" * 70)

    # Prepare data for AIF360
    # AIF360 requires specific formatting
    aif_df = df.copy()

    # Create the AIF360 dataset
    # We specify which column is the label, which are protected attributes,
    # and what values constitute the privileged group and favorable outcome
    aif_dataset = BinaryLabelDataset(
        df=aif_df,
        label_names=['approved'],           # Target column
        protected_attribute_names=['gender'], # Protected attribute column
        favorable_label=1,                   # What value means "good" outcome
        unfavorable_label=0                  # What value means "bad" outcome
    )

    # Define privileged and unprivileged groups
    # In our scenario: Male (1) is the historically privileged group
    privileged_groups = [{'gender': 1}]    # Males
    unprivileged_groups = [{'gender': 0}]  # Females

    print(f"Dataset created with {aif_dataset.features.shape[0]} samples")
    print(f"Number of features: {aif_dataset.features.shape[1]}")
    print(f"Protected attribute: gender")
    print(f"Privileged group: Male (gender=1)")
    print(f"Unprivileged group: Female (gender=0)")

    # -------------------------------------------------------------------------
    # 2.2 Compute Dataset Metrics (Pre-Model)
    # -------------------------------------------------------------------------
    """
    Before training any model, we can assess bias in the training data itself.
    This is crucial because biased training data will lead to biased models.

    Key metrics computed:
    - Statistical Parity Difference: Should be close to 0 for fairness
    - Disparate Impact: Should be close to 1 for fairness (0.8-1.25 acceptable)
    """

    print("\n" + "-" * 70)
    print("2.2 Dataset Fairness Metrics (Before Modeling)")
    print("-" * 70)

    dataset_metric = BinaryLabelDatasetMetric(
        aif_dataset,
        unprivileged_groups=unprivileged_groups,
        privileged_groups=privileged_groups
    )

    print("\nDATASET-LEVEL FAIRNESS METRICS:")
    print("-" * 40)

    # Statistical Parity Difference
    # Measures: P(Y=1|unprivileged) - P(Y=1|privileged)
    # Ideal value: 0 (equal positive rates)
    # Negative value means unprivileged group has lower positive rate
    spd = dataset_metric.statistical_parity_difference()
    print(f"\nStatistical Parity Difference: {spd:.4f}")
    print(f"  Interpretation: {'FAIR' if abs(spd) < 0.1 else 'POTENTIAL BIAS'}")
    print(f"  (Ideal: 0, Acceptable: -0.1 to 0.1)")

    # Disparate Impact
    # Measures: P(Y=1|unprivileged) / P(Y=1|privileged)
    # Ideal value: 1 (equal rates)
    # The "80% rule" considers values < 0.8 as evidence of discrimination
    di = dataset_metric.disparate_impact()
    print(f"\nDisparate Impact Ratio: {di:.4f}")
    print(f"  Interpretation: {'FAIR' if 0.8 <= di <= 1.25 else 'POTENTIAL BIAS'}")
    print(f"  (Ideal: 1.0, Acceptable: 0.8 to 1.25 per 80% rule)")

    # Base rates by group
    print(f"\nBase Rates:")
    print(f"  Privileged (Male): {dataset_metric.base_rate(privileged=True):.4f}")
    print(f"  Unprivileged (Female): {dataset_metric.base_rate(privileged=False):.4f}")

    # -------------------------------------------------------------------------
    # 2.3 Train a Model and Compute Classification Metrics
    # -------------------------------------------------------------------------
    """
    Now we train a model and assess whether it perpetuates or amplifies
    the bias present in the training data.

    Classification metrics compare model predictions to ground truth,
    broken down by protected group membership.
    """

    print("\n" + "-" * 70)
    print("2.3 Model Training and Classification Metrics")
    print("-" * 70)

    # Split data
    train_df, test_df = train_test_split(df, test_size=0.3, random_state=42)

    # Create AIF360 datasets for train and test
    train_aif = BinaryLabelDataset(
        df=train_df,
        label_names=['approved'],
        protected_attribute_names=['gender'],
        favorable_label=1,
        unfavorable_label=0
    )

    test_aif = BinaryLabelDataset(
        df=test_df,
        label_names=['approved'],
        protected_attribute_names=['gender'],
        favorable_label=1,
        unfavorable_label=0
    )

    # Train a logistic regression model
    feature_cols = ['age', 'income', 'credit_score', 'employment_years', 'debt_ratio']
    X_train = train_df[feature_cols]
    y_train = train_df['approved']
    X_test = test_df[feature_cols]
    y_test = test_df['approved']

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train model
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train_scaled, y_train)

    # Get predictions
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

    print(f"\nModel Accuracy: {accuracy_score(y_test, y_pred):.4f}")

    # Create predicted dataset for AIF360
    test_pred_aif = test_aif.copy()
    test_pred_aif.labels = y_pred.reshape(-1, 1)

    # Compute classification metrics
    classification_metric = ClassificationMetric(
        test_aif,                    # Ground truth
        test_pred_aif,               # Predictions
        unprivileged_groups=unprivileged_groups,
        privileged_groups=privileged_groups
    )

    print("\nCLASSIFICATION FAIRNESS METRICS:")
    print("-" * 40)

    # Equal Opportunity Difference
    # Measures difference in True Positive Rates between groups
    # Ideal: 0 (both groups have equal chance of correct positive prediction)
    eod = classification_metric.equal_opportunity_difference()
    print(f"\nEqual Opportunity Difference: {eod:.4f}")
    print(f"  Interpretation: {'FAIR' if abs(eod) < 0.1 else 'POTENTIAL BIAS'}")
    print(f"  (Measures TPR difference; Ideal: 0)")

    # Average Odds Difference
    # Average of TPR difference and FPR difference
    # Comprehensive measure of predictive equality
    aod = classification_metric.average_odds_difference()
    print(f"\nAverage Odds Difference: {aod:.4f}")
    print(f"  Interpretation: {'FAIR' if abs(aod) < 0.1 else 'POTENTIAL BIAS'}")
    print(f"  (Average of TPR and FPR differences; Ideal: 0)")

    # Theil Index
    # Measures inequality in the distribution of benefits
    # 0 = perfect equality, higher = more inequality
    theil = classification_metric.theil_index()
    print(f"\nTheil Index: {theil:.4f}")
    print(f"  Interpretation: {'LOW INEQUALITY' if theil < 0.1 else 'HIGHER INEQUALITY'}")
    print(f"  (Measures benefit inequality; Ideal: 0)")

    # Group-specific metrics
    print(f"\nGroup-Specific Performance:")
    print(f"  TPR (Male):   {classification_metric.true_positive_rate(privileged=True):.4f}")
    print(f"  TPR (Female): {classification_metric.true_positive_rate(privileged=False):.4f}")
    print(f"  FPR (Male):   {classification_metric.false_positive_rate(privileged=True):.4f}")
    print(f"  FPR (Female): {classification_metric.false_positive_rate(privileged=False):.4f}")

    # -------------------------------------------------------------------------
    # 2.4 Bias Mitigation with Reweighing (Pre-processing)
    # -------------------------------------------------------------------------
    """
    REWEIGHING is a pre-processing technique that assigns weights to training
    examples to ensure fair representation.

    How it works:
    1. Calculate expected weights assuming independence between protected
       attribute and label
    2. Assign higher weights to underrepresented combinations
    3. Train model with these weights

    This doesn't change the data, just how much each example counts during
    training.
    """

    print("\n" + "-" * 70)
    print("2.4 Bias Mitigation: Reweighing (Pre-processing)")
    print("-" * 70)

    # Apply reweighing
    reweigher = Reweighing(
        unprivileged_groups=unprivileged_groups,
        privileged_groups=privileged_groups
    )

    train_aif_reweighed = reweigher.fit_transform(train_aif)

    print("\nReweighing applied to training data")
    print(f"Sample weights range: {train_aif_reweighed.instance_weights.min():.3f} - "
          f"{train_aif_reweighed.instance_weights.max():.3f}")

    # Train model with sample weights
    model_reweighed = LogisticRegression(random_state=42, max_iter=1000)
    model_reweighed.fit(
        X_train_scaled,
        y_train,
        sample_weight=train_aif_reweighed.instance_weights
    )

    # Evaluate
    y_pred_reweighed = model_reweighed.predict(X_test_scaled)

    test_pred_reweighed = test_aif.copy()
    test_pred_reweighed.labels = y_pred_reweighed.reshape(-1, 1)

    metric_reweighed = ClassificationMetric(
        test_aif,
        test_pred_reweighed,
        unprivileged_groups=unprivileged_groups,
        privileged_groups=privileged_groups
    )

    print("\nMETRICS AFTER REWEIGHING:")
    print("-" * 40)
    print(f"Accuracy: {accuracy_score(y_test, y_pred_reweighed):.4f} "
          f"(was {accuracy_score(y_test, y_pred):.4f})")
    print(f"Statistical Parity Diff: {metric_reweighed.statistical_parity_difference():.4f} "
          f"(was {classification_metric.statistical_parity_difference():.4f})")
    print(f"Equal Opportunity Diff: {metric_reweighed.equal_opportunity_difference():.4f} "
          f"(was {eod:.4f})")
    print(f"Average Odds Diff: {metric_reweighed.average_odds_difference():.4f} "
          f"(was {aod:.4f})")


# =============================================================================
# SECTION 3: FAIRLEARN
# =============================================================================
"""
Fairlearn is Microsoft's toolkit for assessing and improving fairness.

Key Features:
- MetricFrame: Disaggregated metric computation
- Reduction algorithms: Constrained optimization for fair classifiers
- Dashboard: Interactive visualization (not shown in this script)

Fairlearn Philosophy:
- Fairness as a sociotechnical challenge, not just a technical one
- Focus on understanding disparities before mitigating
- Multiple mitigation strategies with different trade-offs
"""

print("\n" + "=" * 70)
print("SECTION 3: FAIRLEARN ANALYSIS")
print("=" * 70)

try:
    from fairlearn.metrics import (
        MetricFrame,
        demographic_parity_difference,
        demographic_parity_ratio,
        equalized_odds_difference,
        selection_rate
    )
    from fairlearn.reductions import (
        ExponentiatedGradient,
        DemographicParity,
        EqualizedOdds,
        TruePositiveRateParity
    )
    from fairlearn.postprocessing import ThresholdOptimizer

    FAIRLEARN_AVAILABLE = True
    print("\nFairlearn successfully imported!")

except ImportError:
    FAIRLEARN_AVAILABLE = False
    print("\nWARNING: Fairlearn not installed. Install with: pip install fairlearn")
    print("Skipping Fairlearn examples...")

if FAIRLEARN_AVAILABLE:
    # -------------------------------------------------------------------------
    # 3.1 MetricFrame: Disaggregated Metrics
    # -------------------------------------------------------------------------
    """
    MetricFrame is Fairlearn's core class for computing metrics separately
    for different groups. This is essential for understanding WHERE
    disparities exist, not just WHETHER they exist.

    Benefits:
    - See exactly how metrics differ between groups
    - Compare multiple metrics simultaneously
    - Foundation for informed mitigation decisions
    """

    print("\n" + "-" * 70)
    print("3.1 MetricFrame: Disaggregated Metrics Analysis")
    print("-" * 70)

    # Get sensitive feature for test set
    sensitive_test = test_df['gender'].map({0: 'Female', 1: 'Male'})

    # Create MetricFrame with multiple metrics
    # This lets us see how each metric varies across groups
    metrics = {
        'accuracy': accuracy_score,
        'selection_rate': selection_rate,  # P(Y_pred = 1)
        'count': lambda y_true, y_pred: len(y_true)
    }

    metric_frame = MetricFrame(
        metrics=metrics,
        y_true=y_test,
        y_pred=y_pred,  # Using predictions from Section 2
        sensitive_features=sensitive_test
    )

    print("\nDISAGGREGATED METRICS BY GROUP:")
    print("-" * 40)
    print(metric_frame.by_group.round(4))

    print("\nOVERALL METRICS:")
    print("-" * 40)
    print(metric_frame.overall.round(4))

    print("\nDISPARITIES (max - min across groups):")
    print("-" * 40)
    print(metric_frame.difference(method='between_groups').round(4))

    print("\nRATIOS (min / max across groups):")
    print("-" * 40)
    print(metric_frame.ratio(method='between_groups').round(4))

    # Compute specific fairness metrics
    print("\nFAIRLEARN FAIRNESS METRICS:")
    print("-" * 40)

    dp_diff = demographic_parity_difference(
        y_test, y_pred, sensitive_features=sensitive_test
    )
    dp_ratio = demographic_parity_ratio(
        y_test, y_pred, sensitive_features=sensitive_test
    )

    print(f"\nDemographic Parity Difference: {dp_diff:.4f}")
    print(f"  (Difference in selection rates; Ideal: 0)")

    print(f"\nDemographic Parity Ratio: {dp_ratio:.4f}")
    print(f"  (Ratio of selection rates; Ideal: 1.0, Acceptable: 0.8-1.25)")

    # -------------------------------------------------------------------------
    # 3.2 Exponentiated Gradient: Constrained Optimization
    # -------------------------------------------------------------------------
    """
    Exponentiated Gradient is a reduction algorithm that trains a fair
    classifier by treating fairness as a constraint in an optimization problem.

    How it works:
    1. Define a fairness constraint (e.g., Demographic Parity)
    2. Iteratively adjust the classifier to satisfy the constraint
    3. Balance accuracy with fairness through constraint satisfaction

    Constraints available:
    - DemographicParity: Equal selection rates
    - EqualizedOdds: Equal TPR and FPR
    - TruePositiveRateParity: Equal true positive rates
    - FalsePositiveRateParity: Equal false positive rates
    - ErrorRateParity: Equal error rates
    """

    print("\n" + "-" * 70)
    print("3.2 Exponentiated Gradient: Fair Classifier Training")
    print("-" * 70)

    # Prepare data
    sensitive_train = train_df['gender'].values
    sensitive_test_arr = test_df['gender'].values

    # Train with Demographic Parity constraint
    print("\nTraining with DEMOGRAPHIC PARITY constraint...")

    constraint_dp = DemographicParity()

    mitigator_dp = ExponentiatedGradient(
        estimator=LogisticRegression(random_state=42, max_iter=1000),
        constraints=constraint_dp,
        eps=0.01  # Fairness tolerance
    )

    mitigator_dp.fit(X_train_scaled, y_train, sensitive_features=sensitive_train)
    y_pred_dp = mitigator_dp.predict(X_test_scaled)

    # Evaluate
    metric_frame_dp = MetricFrame(
        metrics={'accuracy': accuracy_score, 'selection_rate': selection_rate},
        y_true=y_test,
        y_pred=y_pred_dp,
        sensitive_features=sensitive_test
    )

    dp_diff_mitigated = demographic_parity_difference(
        y_test, y_pred_dp, sensitive_features=sensitive_test
    )

    print("\nRESULTS WITH DEMOGRAPHIC PARITY CONSTRAINT:")
    print("-" * 40)
    print(f"Accuracy: {accuracy_score(y_test, y_pred_dp):.4f} (original: {accuracy_score(y_test, y_pred):.4f})")
    print(f"Demographic Parity Diff: {dp_diff_mitigated:.4f} (original: {dp_diff:.4f})")
    print("\nBy Group:")
    print(metric_frame_dp.by_group.round(4))

    # Train with Equalized Odds constraint
    print("\nTraining with EQUALIZED ODDS constraint...")

    constraint_eo = EqualizedOdds()

    mitigator_eo = ExponentiatedGradient(
        estimator=LogisticRegression(random_state=42, max_iter=1000),
        constraints=constraint_eo,
        eps=0.01
    )

    mitigator_eo.fit(X_train_scaled, y_train, sensitive_features=sensitive_train)
    y_pred_eo = mitigator_eo.predict(X_test_scaled)

    eo_diff_mitigated = equalized_odds_difference(
        y_test, y_pred_eo, sensitive_features=sensitive_test
    )
    eo_diff_original = equalized_odds_difference(
        y_test, y_pred, sensitive_features=sensitive_test
    )

    print("\nRESULTS WITH EQUALIZED ODDS CONSTRAINT:")
    print("-" * 40)
    print(f"Accuracy: {accuracy_score(y_test, y_pred_eo):.4f} (original: {accuracy_score(y_test, y_pred):.4f})")
    print(f"Equalized Odds Diff: {eo_diff_mitigated:.4f} (original: {eo_diff_original:.4f})")

    # -------------------------------------------------------------------------
    # 3.3 Threshold Optimizer: Post-processing
    # -------------------------------------------------------------------------
    """
    ThresholdOptimizer is a post-processing technique that finds group-specific
    classification thresholds to achieve fairness.

    How it works:
    1. Take a trained classifier's probability predictions
    2. Find different thresholds for different groups
    3. Thresholds are optimized to satisfy fairness constraints

    Advantage: Can be applied to any existing model without retraining
    Disadvantage: Requires access to protected attributes at prediction time
    """

    print("\n" + "-" * 70)
    print("3.3 Threshold Optimizer: Post-processing Mitigation")
    print("-" * 70)

    # Get probability predictions from original model
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

    # Apply ThresholdOptimizer
    print("\nApplying threshold optimization for demographic parity...")

    threshold_optimizer = ThresholdOptimizer(
        estimator=model,
        constraints="demographic_parity",
        predict_method="predict_proba",
        prefit=True  # Model is already fitted
    )

    # Fit the threshold optimizer
    threshold_optimizer.fit(X_train_scaled, y_train, sensitive_features=sensitive_train)

    # Get predictions with optimized thresholds
    y_pred_thresh = threshold_optimizer.predict(X_test_scaled, sensitive_features=sensitive_test_arr)

    dp_diff_thresh = demographic_parity_difference(
        y_test, y_pred_thresh, sensitive_features=sensitive_test
    )

    print("\nRESULTS WITH THRESHOLD OPTIMIZATION:")
    print("-" * 40)
    print(f"Accuracy: {accuracy_score(y_test, y_pred_thresh):.4f} (original: {accuracy_score(y_test, y_pred):.4f})")
    print(f"Demographic Parity Diff: {dp_diff_thresh:.4f} (original: {dp_diff:.4f})")


# =============================================================================
# SECTION 4: SUMMARY AND BEST PRACTICES
# =============================================================================
"""
SUMMARY OF BIAS TESTING APPROACHES
----------------------------------

1. PRE-PROCESSING (Before Training):
   - Reweighing: Adjust sample weights
   - Disparate Impact Remover: Transform features
   - Sampling: Oversample/undersample groups

   Pros: Model-agnostic, preserves model choice
   Cons: May not fully address algorithmic bias

2. IN-PROCESSING (During Training):
   - Exponentiated Gradient: Constrained optimization
   - Adversarial Debiasing: Add fairness to loss function
   - Prejudice Remover: Regularization for fairness

   Pros: Directly optimizes for fairness
   Cons: Need to modify training procedure

3. POST-PROCESSING (After Training):
   - Threshold Optimization: Group-specific thresholds
   - Equalized Odds Post-processing: Adjust predictions
   - Calibration: Ensure equal calibration across groups

   Pros: Works with any existing model
   Cons: May require protected attributes at inference

BEST PRACTICES FOR PRODUCTION:
------------------------------

1. UNDERSTAND YOUR CONTEXT
   - What does "fairness" mean in your domain?
   - Who are the stakeholders?
   - What are the legal requirements?

2. MEASURE BEFORE MITIGATING
   - Compute multiple fairness metrics
   - Understand WHERE disparities exist
   - Document baseline performance

3. CONSIDER TRADE-OFFS
   - Fairness often trades off with accuracy
   - Different fairness definitions can conflict
   - Business impact vs. fairness improvement

4. VALIDATE THOROUGHLY
   - Test on held-out data
   - Monitor over time
   - Check for intersectional bias

5. DOCUMENT EVERYTHING
   - Why you chose certain metrics
   - What mitigation you applied
   - What trade-offs you accepted
"""

print("\n" + "=" * 70)
print("SUMMARY: COMPARISON OF APPROACHES")
print("=" * 70)

print("\n" + "-" * 70)
print("ACCURACY VS FAIRNESS TRADE-OFFS")
print("-" * 70)

results = []

# Original model
results.append({
    'Approach': 'Original Model',
    'Accuracy': accuracy_score(y_test, y_pred),
    'DP Difference': dp_diff if FAIRLEARN_AVAILABLE else 'N/A'
})

# Add results from each mitigation approach
if AIF360_AVAILABLE:
    results.append({
        'Approach': 'AIF360 Reweighing',
        'Accuracy': accuracy_score(y_test, y_pred_reweighed),
        'DP Difference': metric_reweighed.statistical_parity_difference()
    })

if FAIRLEARN_AVAILABLE:
    results.append({
        'Approach': 'Fairlearn Exp. Gradient (DP)',
        'Accuracy': accuracy_score(y_test, y_pred_dp),
        'DP Difference': dp_diff_mitigated
    })
    results.append({
        'Approach': 'Fairlearn Threshold Opt.',
        'Accuracy': accuracy_score(y_test, y_pred_thresh),
        'DP Difference': dp_diff_thresh
    })

results_df = pd.DataFrame(results)
print("\n", results_df.to_string(index=False))

print("\n" + "-" * 70)
print("KEY TAKEAWAYS")
print("-" * 70)
print("""
1. Bias testing should be a standard part of ML model development
2. Use multiple metrics - no single metric captures all aspects of fairness
3. Mitigation often involves accuracy trade-offs - make informed decisions
4. AIF360 and Fairlearn complement each other:
   - AIF360: Comprehensive metrics, more algorithms
   - Fairlearn: Better API, MetricFrame for analysis
5. Always validate on held-out data and monitor in production
""")

print("\n" + "=" * 70)
print("END OF BIAS TESTING EXAMPLES")
print("=" * 70)
