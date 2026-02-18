"""
=============================================================================
MODEL EXPLAINABILITY AND INTERPRETABILITY
=============================================================================

This module demonstrates techniques for understanding and explaining machine
learning model predictions using SHAP (SHapley Additive exPlanations) and
LIME (Local Interpretable Model-agnostic Explanations).

CONCEPTUAL BACKGROUND
---------------------
As ML models become more complex and are deployed in high-stakes domains
(healthcare, finance, criminal justice), the need to understand WHY a model
makes certain predictions becomes critical.

TWO TYPES OF INTERPRETABILITY:

1. GLOBAL INTERPRETABILITY
   Understanding the overall behavior of the model:
   - Which features are most important overall?
   - How do features interact?
   - What patterns has the model learned?

2. LOCAL INTERPRETABILITY
   Understanding individual predictions:
   - Why was THIS customer denied a loan?
   - Which features drove THIS diagnosis?
   - How certain is the model about THIS prediction?

WHY EXPLAINABILITY MATTERS FOR TRUSTWORTHY AI:
----------------------------------------------
1. REGULATORY COMPLIANCE
   - GDPR's "right to explanation"
   - EU AI Act requirements for high-risk systems
   - US regulations (FCRA, ECOA) for credit decisions

2. DEBUGGING AND IMPROVEMENT
   - Identify spurious correlations
   - Find data quality issues
   - Improve model robustness

3. STAKEHOLDER TRUST
   - Users need to understand AI decisions
   - Auditors need to verify model behavior
   - Domain experts need to validate logic

4. FAIRNESS ASSESSMENT
   - Identify discriminatory patterns
   - Understand feature importance by group
   - Validate that protected attributes aren't proxied

Libraries Used:
- shap: SHAP values for model explanations
- lime: Local explanations for any classifier

Installation:
    pip install shap lime scikit-learn pandas numpy matplotlib
"""

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for script execution
import matplotlib.pyplot as plt

# =============================================================================
# SECTION 1: DATA PREPARATION
# =============================================================================
"""
We'll use a synthetic dataset that simulates a medical diagnosis scenario.
This makes explanations more intuitive and meaningful.

Scenario: Predicting risk of heart disease
Features represent various health indicators
"""

def create_medical_dataset(n_samples=2000, random_state=42):
    """
    Create a synthetic medical dataset for heart disease prediction.

    Features are designed to have interpretable relationships with the outcome,
    making explanations more meaningful for demonstration purposes.

    Returns:
    --------
    X : pd.DataFrame
        Feature matrix with named columns
    y : np.array
        Binary target (0 = low risk, 1 = high risk)
    """
    np.random.seed(random_state)

    # Generate features with realistic medical interpretations
    age = np.random.normal(55, 15, n_samples)
    age = np.clip(age, 20, 90)

    # Cholesterol: higher values increase risk
    cholesterol = np.random.normal(200, 40, n_samples)
    cholesterol = np.clip(cholesterol, 100, 350)

    # Blood pressure (systolic)
    blood_pressure = np.random.normal(120, 20, n_samples)
    blood_pressure = np.clip(blood_pressure, 80, 200)

    # BMI: Body Mass Index
    bmi = np.random.normal(26, 5, n_samples)
    bmi = np.clip(bmi, 15, 45)

    # Exercise hours per week
    exercise = np.random.exponential(3, n_samples)
    exercise = np.clip(exercise, 0, 20)

    # Smoking status (0 = never, 1 = former, 2 = current)
    smoking = np.random.choice([0, 1, 2], n_samples, p=[0.5, 0.25, 0.25])

    # Family history (binary)
    family_history = np.random.binomial(1, 0.3, n_samples)

    # Diabetes (binary)
    diabetes = np.random.binomial(1, 0.15, n_samples)

    # Generate target with known relationships
    # This allows us to verify that explanations match true relationships
    risk_score = (
        0.03 * (age - 40) +                    # Age increases risk
        0.01 * (cholesterol - 180) +           # High cholesterol increases risk
        0.02 * (blood_pressure - 110) +        # High BP increases risk
        0.05 * (bmi - 22) +                    # High BMI increases risk
        -0.15 * exercise +                      # Exercise decreases risk (protective)
        0.5 * smoking +                         # Smoking increases risk
        0.7 * family_history +                  # Family history increases risk
        0.8 * diabetes +                        # Diabetes increases risk
        np.random.normal(0, 0.5, n_samples)    # Random noise
    )

    # Convert to probability and then binary
    prob = 1 / (1 + np.exp(-risk_score))
    y = np.random.binomial(1, prob)

    # Create DataFrame
    X = pd.DataFrame({
        'age': age,
        'cholesterol': cholesterol,
        'blood_pressure': blood_pressure,
        'bmi': bmi,
        'exercise_hours': exercise,
        'smoking_status': smoking,
        'family_history': family_history,
        'diabetes': diabetes
    })

    return X, y

# Create dataset
print("=" * 70)
print("CREATING MEDICAL DATASET FOR HEART DISEASE PREDICTION")
print("=" * 70)

X, y = create_medical_dataset(n_samples=2000)

print("\nDataset Shape:", X.shape)
print("\nFeature Summary:")
print(X.describe().round(2))
print(f"\nTarget Distribution: {np.bincount(y)}")
print(f"  Low Risk (0): {(y==0).sum()} ({(y==0).mean()*100:.1f}%)")
print(f"  High Risk (1): {(y==1).sum()} ({(y==1).mean()*100:.1f}%)")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Train models
print("\n" + "-" * 70)
print("TRAINING MODELS")
print("-" * 70)

# Random Forest (our main model for explanations)
rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
rf_model.fit(X_train, y_train)
print(f"\nRandom Forest Accuracy: {rf_model.score(X_test, y_test):.4f}")

# Gradient Boosting (for comparison)
gb_model = GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42)
gb_model.fit(X_train, y_train)
print(f"Gradient Boosting Accuracy: {gb_model.score(X_test, y_test):.4f}")

# Logistic Regression (inherently interpretable baseline)
lr_model = LogisticRegression(max_iter=1000, random_state=42)
lr_model.fit(X_train, y_train)
print(f"Logistic Regression Accuracy: {lr_model.score(X_test, y_test):.4f}")


# =============================================================================
# SECTION 2: SHAP (SHapley Additive exPlanations)
# =============================================================================
"""
SHAP VALUES: A UNIFIED APPROACH TO FEATURE IMPORTANCE

THEORETICAL FOUNDATION:
-----------------------
SHAP values are based on Shapley values from cooperative game theory.
The idea: How do we fairly distribute the "payout" (prediction) among
the "players" (features)?

For a prediction f(x), the SHAP value φᵢ for feature i represents:
- The average marginal contribution of feature i
- Across all possible orderings of features
- Compared to a baseline (typically the average prediction)

KEY PROPERTIES (that make SHAP special):
-----------------------------------------
1. LOCAL ACCURACY: Sum of SHAP values = prediction - expected value
   f(x) = E[f(x)] + Σ φᵢ

2. MISSINGNESS: Features not present contribute zero
   If xᵢ is missing, φᵢ = 0

3. CONSISTENCY: If a feature's contribution increases, its SHAP value increases

4. ADDITIVITY: For linear models, SHAP values equal the feature contributions

TYPES OF SHAP EXPLAINERS:
-------------------------
- TreeExplainer: Fast, exact for tree-based models
- KernelExplainer: Model-agnostic, uses sampling (slower)
- DeepExplainer: For neural networks
- LinearExplainer: For linear models
- GradientExplainer: Uses gradients for any differentiable model
"""

print("\n" + "=" * 70)
print("SECTION 2: SHAP EXPLANATIONS")
print("=" * 70)

try:
    import shap
    SHAP_AVAILABLE = True
    print("\nSHAP library successfully imported!")

except ImportError:
    SHAP_AVAILABLE = False
    print("\nWARNING: SHAP not installed. Install with: pip install shap")
    print("Skipping SHAP examples...")

if SHAP_AVAILABLE:
    # -------------------------------------------------------------------------
    # 2.1 TreeExplainer for Random Forest
    # -------------------------------------------------------------------------
    """
    TreeExplainer is optimized for tree-based models (Random Forest, XGBoost,
    LightGBM, etc.). It computes exact SHAP values efficiently using the
    tree structure.

    For a Random Forest with T trees, TreeExplainer:
    1. Traverses each tree
    2. Computes the expected value at each node
    3. Calculates feature contributions along the path
    4. Averages across all trees
    """

    print("\n" + "-" * 70)
    print("2.1 TreeExplainer for Random Forest")
    print("-" * 70)

    # Create explainer
    # We pass the model and optionally the training data
    explainer_tree = shap.TreeExplainer(rf_model)

    print("\nComputing SHAP values for test set...")
    print("(This may take a moment for large datasets)")

    # Compute SHAP values for test set
    # shap_values is an array of shape (n_samples, n_features)
    # For binary classification, we get values for each class
    shap_values = explainer_tree.shap_values(X_test)

    # For binary classification, shap_values is a list [class_0_values, class_1_values]
    # We typically focus on class 1 (positive class)
    if isinstance(shap_values, list):
        shap_values_class1 = shap_values[1]
    else:
        shap_values_class1 = shap_values

    print(f"\nSHAP values shape: {shap_values_class1.shape}")
    print(f"Expected value (base prediction): {explainer_tree.expected_value}")

    # -------------------------------------------------------------------------
    # 2.2 Global Feature Importance (Mean |SHAP|)
    # -------------------------------------------------------------------------
    """
    Global feature importance from SHAP is computed as the mean absolute
    SHAP value for each feature across all samples.

    This tells us: On average, how much does each feature contribute to
    predictions (in either direction)?

    Advantages over traditional feature importance:
    - Consistent across different model types
    - Based on actual prediction contributions
    - Accounts for feature interactions
    """

    print("\n" + "-" * 70)
    print("2.2 Global Feature Importance (Mean |SHAP|)")
    print("-" * 70)

    # Calculate mean absolute SHAP values
    mean_abs_shap = np.abs(shap_values_class1).mean(axis=0)

    # Create importance DataFrame
    importance_df = pd.DataFrame({
        'Feature': X.columns,
        'Mean |SHAP|': mean_abs_shap
    }).sort_values('Mean |SHAP|', ascending=False)

    print("\nGLOBAL FEATURE IMPORTANCE (by mean |SHAP|):")
    print("-" * 40)
    for idx, row in importance_df.iterrows():
        bar = '█' * int(row['Mean |SHAP|'] / importance_df['Mean |SHAP|'].max() * 30)
        print(f"{row['Feature']:20s} {row['Mean |SHAP|']:.4f} {bar}")

    print("\nINTERPRETATION:")
    print("-" * 40)
    print(f"""
    The most important features for predicting heart disease risk are:
    1. {importance_df.iloc[0]['Feature']}: Highest average impact on predictions
    2. {importance_df.iloc[1]['Feature']}: Second highest impact
    3. {importance_df.iloc[2]['Feature']}: Third highest impact

    Features with higher mean |SHAP| values have more influence on the
    model's predictions, regardless of whether they increase or decrease risk.
    """)

    # -------------------------------------------------------------------------
    # 2.3 SHAP Summary Plot (Feature Effects)
    # -------------------------------------------------------------------------
    """
    The SHAP summary plot shows:
    - Feature importance (y-axis ordering)
    - Distribution of SHAP values for each feature
    - Relationship between feature values and SHAP values (color)

    Red = high feature value, Blue = low feature value
    Right side = increases prediction, Left side = decreases prediction
    """

    print("\n" + "-" * 70)
    print("2.3 SHAP Summary Plot")
    print("-" * 70)

    print("\nGenerating SHAP summary plot...")
    plt.figure(figsize=(10, 8))
    shap.summary_plot(shap_values_class1, X_test, show=False)
    plt.title("SHAP Summary Plot - Feature Impact on Heart Disease Risk")
    plt.tight_layout()
    plt.savefig('shap_summary_plot.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: shap_summary_plot.png")

    print("""
    HOW TO READ THE SUMMARY PLOT:
    -----------------------------
    - Each dot is one patient
    - X-axis: SHAP value (impact on prediction)
    - Color: Feature value (red=high, blue=low)

    For example, for 'diabetes':
    - Red dots (diabetes=1) tend to be on the RIGHT → increases risk
    - Blue dots (diabetes=0) tend to be on the LEFT → decreases risk

    For 'exercise_hours':
    - Red dots (more exercise) tend to be on the LEFT → decreases risk
    - This matches our expectation that exercise is protective
    """)

    # -------------------------------------------------------------------------
    # 2.4 Local Explanation: Single Prediction
    # -------------------------------------------------------------------------
    """
    LOCAL EXPLANATIONS show why the model made a specific prediction for
    one individual. This is crucial for:
    - Explaining decisions to affected individuals
    - Debugging unexpected predictions
    - Audit and compliance requirements
    """

    print("\n" + "-" * 70)
    print("2.4 Local Explanation: Individual Prediction")
    print("-" * 70)

    # Select a specific patient to explain
    patient_idx = 0
    patient = X_test.iloc[patient_idx:patient_idx+1]
    patient_shap = shap_values_class1[patient_idx]
    prediction = rf_model.predict_proba(patient)[0, 1]

    print(f"\nEXPLAINING PREDICTION FOR PATIENT #{patient_idx}")
    print("=" * 50)
    print("\nPatient Features:")
    for col in X.columns:
        print(f"  {col}: {patient[col].values[0]:.2f}")

    print(f"\nPrediction: {prediction:.2%} probability of high risk")
    print(f"Base rate (expected value): {explainer_tree.expected_value[1]:.2%}")

    print("\nFEATURE CONTRIBUTIONS (SHAP values):")
    print("-" * 50)

    # Sort by absolute contribution
    contrib_df = pd.DataFrame({
        'Feature': X.columns,
        'Value': patient.values[0],
        'SHAP': patient_shap
    }).sort_values('SHAP', key=abs, ascending=False)

    for _, row in contrib_df.iterrows():
        direction = "↑ INCREASES" if row['SHAP'] > 0 else "↓ DECREASES"
        print(f"  {row['Feature']:20s} = {row['Value']:8.2f} → {row['SHAP']:+.4f} ({direction} risk)")

    print(f"\n  Sum of SHAP values: {patient_shap.sum():.4f}")
    print(f"  Base + SHAP sum = {explainer_tree.expected_value[1] + patient_shap.sum():.4f}")
    print(f"  (This should approximately equal the prediction in log-odds space)")

    # -------------------------------------------------------------------------
    # 2.5 SHAP Waterfall Plot
    # -------------------------------------------------------------------------
    """
    The waterfall plot shows how the prediction is built up from the base
    value by adding each feature's contribution.

    It visualizes: base_value + Σ(SHAP values) = final prediction
    """

    print("\n" + "-" * 70)
    print("2.5 SHAP Waterfall Plot")
    print("-" * 70)

    print("\nGenerating waterfall plot for patient prediction...")

    # Create explanation object for waterfall
    explanation = shap.Explanation(
        values=patient_shap,
        base_values=explainer_tree.expected_value[1],
        data=patient.values[0],
        feature_names=X.columns.tolist()
    )

    plt.figure(figsize=(10, 6))
    shap.waterfall_plot(explanation, show=False)
    plt.title(f"SHAP Waterfall - Patient #{patient_idx}")
    plt.tight_layout()
    plt.savefig('shap_waterfall.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: shap_waterfall.png")

    # -------------------------------------------------------------------------
    # 2.6 SHAP Dependence Plot
    # -------------------------------------------------------------------------
    """
    Dependence plots show the relationship between a feature's value and
    its SHAP value. This reveals:
    - Non-linear relationships
    - Interaction effects (when colored by another feature)
    - Threshold effects
    """

    print("\n" + "-" * 70)
    print("2.6 SHAP Dependence Plots")
    print("-" * 70)

    print("\nGenerating dependence plots...")

    # Age dependence
    plt.figure(figsize=(10, 5))
    shap.dependence_plot('age', shap_values_class1, X_test, show=False)
    plt.title("SHAP Dependence: Age")
    plt.tight_layout()
    plt.savefig('shap_dependence_age.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: shap_dependence_age.png")

    # Exercise dependence
    plt.figure(figsize=(10, 5))
    shap.dependence_plot('exercise_hours', shap_values_class1, X_test, show=False)
    plt.title("SHAP Dependence: Exercise Hours")
    plt.tight_layout()
    plt.savefig('shap_dependence_exercise.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: shap_dependence_exercise.png")

    print("""
    INTERPRETING DEPENDENCE PLOTS:
    ------------------------------
    Age plot:
    - As age increases, SHAP values tend to increase
    - This means older age → higher predicted risk
    - The spread shows uncertainty/variability

    Exercise plot:
    - As exercise increases, SHAP values tend to DECREASE
    - This means more exercise → lower predicted risk
    - Exercise is a protective factor

    The color in dependence plots shows interaction effects with
    another feature (automatically selected or specified).
    """)


# =============================================================================
# SECTION 3: LIME (Local Interpretable Model-agnostic Explanations)
# =============================================================================
"""
LIME: A DIFFERENT APPROACH TO LOCAL EXPLANATIONS

CORE IDEA:
----------
LIME explains any model by approximating it LOCALLY with an interpretable
model (typically linear regression).

How LIME works:
1. Perturb the input: Create variations of the instance to explain
2. Get predictions: Ask the black-box model to predict on perturbations
3. Weight by proximity: Closer perturbations matter more
4. Fit simple model: Train a linear model on the weighted perturbations
5. Extract explanation: The simple model's coefficients are the explanation

DIFFERENCES FROM SHAP:
----------------------
LIME:
- Approximates the model locally
- Faster for single explanations
- Explanations can vary with random sampling
- No theoretical guarantee of faithfulness

SHAP:
- Exact computation of feature contributions
- Consistent and additive
- Can be slower (especially KernelSHAP)
- Theoretical guarantees from game theory

WHEN TO USE WHICH:
------------------
- Use SHAP when you need consistent, theoretically grounded explanations
- Use LIME when you need fast explanations and some approximation is okay
- Use both for validation: if they disagree, investigate further
"""

print("\n" + "=" * 70)
print("SECTION 3: LIME EXPLANATIONS")
print("=" * 70)

try:
    import lime
    import lime.lime_tabular
    LIME_AVAILABLE = True
    print("\nLIME library successfully imported!")

except ImportError:
    LIME_AVAILABLE = False
    print("\nWARNING: LIME not installed. Install with: pip install lime")
    print("Skipping LIME examples...")

if LIME_AVAILABLE:
    # -------------------------------------------------------------------------
    # 3.1 Create LIME Explainer
    # -------------------------------------------------------------------------
    """
    LimeTabularExplainer needs:
    - Training data: To understand feature distributions
    - Feature names: For interpretable output
    - Class names: For classification tasks
    - Mode: 'classification' or 'regression'
    """

    print("\n" + "-" * 70)
    print("3.1 Creating LIME Explainer")
    print("-" * 70)

    # Create the LIME explainer
    lime_explainer = lime.lime_tabular.LimeTabularExplainer(
        training_data=X_train.values,
        feature_names=X.columns.tolist(),
        class_names=['Low Risk', 'High Risk'],
        mode='classification',
        discretize_continuous=True,  # Bin continuous features for interpretability
        random_state=42
    )

    print("\nLIME explainer created with settings:")
    print(f"  - Training samples: {X_train.shape[0]}")
    print(f"  - Features: {X_train.shape[1]}")
    print(f"  - Mode: classification")
    print(f"  - Discretize continuous: True")

    # -------------------------------------------------------------------------
    # 3.2 Explain Single Prediction
    # -------------------------------------------------------------------------
    """
    explain_instance() generates a local explanation for one data point.

    Parameters:
    - data_row: The instance to explain
    - predict_fn: Model's prediction function (must return probabilities)
    - num_features: How many features to include in explanation
    - num_samples: How many perturbations to generate (more = more stable)
    """

    print("\n" + "-" * 70)
    print("3.2 LIME Explanation for Single Prediction")
    print("-" * 70)

    # Explain the same patient we used for SHAP
    patient_values = X_test.iloc[patient_idx].values

    print(f"\nGenerating LIME explanation for Patient #{patient_idx}...")
    print("(Creating perturbations and fitting local linear model)")

    lime_exp = lime_explainer.explain_instance(
        patient_values,
        rf_model.predict_proba,
        num_features=8,     # Include all features
        num_samples=5000    # More samples = more stable explanation
    )

    print("\nLIME EXPLANATION:")
    print("=" * 50)
    print(f"\nPrediction probabilities:")
    print(f"  Low Risk:  {rf_model.predict_proba([patient_values])[0, 0]:.2%}")
    print(f"  High Risk: {rf_model.predict_proba([patient_values])[0, 1]:.2%}")

    print(f"\nLocal model intercept: {lime_exp.intercept[1]:.4f}")
    print(f"Local model R²: {lime_exp.score:.4f}")
    print("  (R² indicates how well the linear model fits the local region)")

    print("\nFEATURE CONTRIBUTIONS (from local linear model):")
    print("-" * 50)

    # Get explanation as list of (feature, weight) tuples
    explanation_list = lime_exp.as_list(label=1)  # For High Risk class

    for feature_rule, weight in explanation_list:
        direction = "↑ INCREASES" if weight > 0 else "↓ DECREASES"
        print(f"  {feature_rule:35s} → {weight:+.4f} ({direction} risk)")

    # -------------------------------------------------------------------------
    # 3.3 Compare LIME and SHAP
    # -------------------------------------------------------------------------
    """
    Comparing LIME and SHAP explanations for the same prediction helps us:
    - Validate that explanations are consistent
    - Understand the differences between approaches
    - Build confidence in our interpretations
    """

    print("\n" + "-" * 70)
    print("3.3 Comparing LIME and SHAP Explanations")
    print("-" * 70)

    if SHAP_AVAILABLE:
        print("\nCOMPARISON: Same Patient, Different Methods")
        print("=" * 50)

        print("\nTop features by impact:")
        print("-" * 50)
        print(f"{'Feature':<20} {'SHAP':>12} {'LIME':>12} {'Agree?':>10}")
        print("-" * 50)

        # Get LIME weights by feature (need to extract feature name from rule)
        lime_weights = {}
        for rule, weight in explanation_list:
            # Extract base feature name (before any conditions)
            for feat in X.columns:
                if feat in rule:
                    lime_weights[feat] = weight
                    break

        for feat in X.columns:
            shap_val = patient_shap[X.columns.tolist().index(feat)]
            lime_val = lime_weights.get(feat, 0)
            agree = "✓" if (shap_val > 0) == (lime_val > 0) else "✗"
            print(f"{feat:<20} {shap_val:>+12.4f} {lime_val:>+12.4f} {agree:>10}")

        print("""
    INTERPRETATION:
    ---------------
    - SHAP and LIME often agree on direction (increase/decrease risk)
    - Magnitudes may differ due to different methodologies
    - Disagreements warrant further investigation
    - Agreement increases confidence in the explanation
        """)

    # -------------------------------------------------------------------------
    # 3.4 LIME Visualization
    # -------------------------------------------------------------------------

    print("\n" + "-" * 70)
    print("3.4 LIME Visualization")
    print("-" * 70)

    print("\nGenerating LIME explanation plot...")
    fig = lime_exp.as_pyplot_figure(label=1)
    plt.title(f"LIME Explanation - Patient #{patient_idx} (High Risk)")
    plt.tight_layout()
    plt.savefig('lime_explanation.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: lime_explanation.png")

    # -------------------------------------------------------------------------
    # 3.5 Explaining Multiple Predictions
    # -------------------------------------------------------------------------
    """
    For production use, you often need to explain multiple predictions.
    This section shows how to generate explanations at scale.
    """

    print("\n" + "-" * 70)
    print("3.5 Batch Explanations")
    print("-" * 70)

    print("\nGenerating explanations for multiple patients...")

    # Explain first 5 patients
    n_patients = 5
    batch_explanations = []

    for i in range(n_patients):
        exp = lime_explainer.explain_instance(
            X_test.iloc[i].values,
            rf_model.predict_proba,
            num_features=5,
            num_samples=1000  # Fewer samples for speed
        )
        batch_explanations.append({
            'patient': i,
            'prediction': rf_model.predict_proba([X_test.iloc[i].values])[0, 1],
            'top_features': exp.as_list(label=1)[:3]  # Top 3 features
        })

    print("\nSUMMARY OF BATCH EXPLANATIONS:")
    print("=" * 60)
    for exp in batch_explanations:
        print(f"\nPatient #{exp['patient']}: {exp['prediction']:.1%} high risk")
        print("  Top 3 contributing factors:")
        for feat, weight in exp['top_features']:
            direction = "↑" if weight > 0 else "↓"
            print(f"    {direction} {feat}: {weight:+.4f}")


# =============================================================================
# SECTION 4: ADVANCED TOPICS AND BEST PRACTICES
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 4: ADVANCED TOPICS AND BEST PRACTICES")
print("=" * 70)

# -------------------------------------------------------------------------
# 4.1 Model Comparison Using Explanations
# -------------------------------------------------------------------------
"""
Explanations can help compare different models:
- Do they rely on the same features?
- Do they capture the same relationships?
- Are some models more interpretable than others?
"""

print("\n" + "-" * 70)
print("4.1 Comparing Models via Explanations")
print("-" * 70)

print("\nComparing feature importance across models:")
print("-" * 50)

# Logistic Regression coefficients (inherently interpretable)
lr_importance = pd.DataFrame({
    'Feature': X.columns,
    'LR Coef': np.abs(lr_model.coef_[0])
}).sort_values('LR Coef', ascending=False)

# Random Forest built-in importance
rf_importance = pd.DataFrame({
    'Feature': X.columns,
    'RF Importance': rf_model.feature_importances_
}).sort_values('RF Importance', ascending=False)

print("\nLogistic Regression (by |coefficient|):")
for _, row in lr_importance.head(5).iterrows():
    print(f"  {row['Feature']}: {row['LR Coef']:.4f}")

print("\nRandom Forest (by impurity-based importance):")
for _, row in rf_importance.head(5).iterrows():
    print(f"  {row['Feature']}: {row['RF Importance']:.4f}")

if SHAP_AVAILABLE:
    print("\nRandom Forest (by mean |SHAP|):")
    for _, row in importance_df.head(5).iterrows():
        print(f"  {row['Feature']}: {row['Mean |SHAP|']:.4f}")

print("""
OBSERVATIONS:
-------------
- Different methods can rank features differently
- SHAP importance is based on actual prediction contributions
- Built-in RF importance can overstate high-cardinality features
- Logistic regression coefficients need careful interpretation with scaling
""")

# -------------------------------------------------------------------------
# 4.2 Best Practices
# -------------------------------------------------------------------------

print("\n" + "-" * 70)
print("4.2 Best Practices for Production Explainability")
print("-" * 70)

print("""
BEST PRACTICES FOR TRUSTWORTHY EXPLANATIONS:
============================================

1. VALIDATE EXPLANATIONS
   - Compare multiple methods (SHAP vs LIME)
   - Check that explanations match domain knowledge
   - Test on known cases where you understand the "right" answer

2. USE APPROPRIATE EXPLAINERS
   - TreeExplainer for tree-based models (fast, exact)
   - KernelSHAP for any model (slower, flexible)
   - LIME when speed is critical and approximation is acceptable

3. PROVIDE CONTEXT
   - Show base rates alongside individual explanations
   - Compare to similar cases
   - Include confidence/uncertainty measures

4. CONSIDER YOUR AUDIENCE
   - Technical users: Full SHAP plots, detailed metrics
   - Business users: Simple summaries, key factors
   - End users: Plain language, actionable insights

5. DOCUMENT LIMITATIONS
   - Explanations are approximations
   - Different methods may give different results
   - Feature interactions may not be fully captured

6. MONITOR EXPLANATION QUALITY
   - Track if explanations remain consistent over time
   - Watch for drift in feature importance
   - Validate that explanations align with model updates

7. HANDLE SENSITIVE FEATURES CAREFULLY
   - Decide whether to show protected attributes in explanations
   - Consider fairness implications
   - Ensure explanations don't reveal private information
""")

# -------------------------------------------------------------------------
# 4.3 Common Pitfalls
# -------------------------------------------------------------------------

print("\n" + "-" * 70)
print("4.3 Common Pitfalls to Avoid")
print("-" * 70)

print("""
PITFALLS IN MODEL EXPLAINABILITY:
=================================

1. EXPLAINING THE WRONG THING
   ✗ Explaining training predictions (use test/production data)
   ✗ Global explanations for individual decisions
   ✗ Feature importance without directionality

2. OVER-TRUSTING EXPLANATIONS
   ✗ Assuming explanations are 100% accurate
   ✗ Not validating with domain experts
   ✗ Using one method without cross-validation

3. MISINTERPRETING RESULTS
   ✗ Confusing importance with causality
   ✗ Ignoring feature correlations
   ✗ Missing interaction effects

4. TECHNICAL ISSUES
   ✗ Using wrong SHAP explainer for model type
   ✗ Too few samples in LIME (unstable explanations)
   ✗ Not handling missing values properly

5. COMMUNICATION PROBLEMS
   ✗ Too technical for the audience
   ✗ Not providing actionable insights
   ✗ Leaving out important context
""")


print("\n" + "=" * 70)
print("END OF EXPLAINABILITY EXAMPLES")
print("=" * 70)

print("""
FILES GENERATED:
- shap_summary_plot.png: Global feature importance visualization
- shap_waterfall.png: Single prediction breakdown
- shap_dependence_age.png: Age vs. SHAP value relationship
- shap_dependence_exercise.png: Exercise vs. SHAP value relationship
- lime_explanation.png: LIME local explanation visualization

These visualizations demonstrate key explainability concepts that are
essential for trustworthy AI systems.
""")
