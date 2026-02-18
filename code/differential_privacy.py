"""
=============================================================================
DIFFERENTIAL PRIVACY IN MACHINE LEARNING
=============================================================================

This module demonstrates privacy-preserving machine learning techniques
using Opacus (PyTorch) and TensorFlow Privacy libraries.

CONCEPTUAL BACKGROUND
---------------------
Differential Privacy (DP) provides mathematical guarantees about privacy.
A mechanism M is (ε, δ)-differentially private if for any two adjacent
datasets D and D' (differing in one record) and any output S:

    P[M(D) ∈ S] ≤ e^ε × P[M(D') ∈ S] + δ

In plain terms: The output of the algorithm is nearly identical whether
or not any single individual's data is included.

KEY PARAMETERS:
---------------
- ε (epsilon): Privacy budget. Lower = more privacy.
  - ε = 0: Perfect privacy (but useless results)
  - ε = 1: Strong privacy
  - ε = 10: Weak privacy
  - ε = ∞: No privacy

- δ (delta): Probability of privacy breach. Typically << 1/n.
  - Common choice: 1e-5 or smaller

PRIVACY-UTILITY TRADEOFF:
-------------------------
Lower ε → More privacy → More noise → Lower model accuracy
Higher ε → Less privacy → Less noise → Higher model accuracy

Finding the right balance is crucial for practical deployment.

WHY DP MATTERS FOR TRUSTWORTHY AI:
----------------------------------
1. REGULATORY COMPLIANCE
   - GDPR, CCPA, HIPAA requirements
   - Demonstrable privacy protection

2. TRUST BUILDING
   - Users can trust their data is protected
   - Organizations can use sensitive data responsibly

3. RISK MITIGATION
   - Protection against data breaches
   - Defense against inference attacks

4. ENABLING DATA USE
   - Make sensitive datasets usable
   - Enable collaborative learning

Libraries Used:
- opacus: PyTorch differential privacy library
- tensorflow-privacy: TensorFlow differential privacy library

Installation:
    pip install opacus torch
    pip install tensorflow-privacy tensorflow
"""

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# =============================================================================
# SECTION 1: DIFFERENTIAL PRIVACY FUNDAMENTALS
# =============================================================================
"""
Understanding differential privacy mathematically and intuitively.
"""

print("=" * 70)
print("DIFFERENTIAL PRIVACY IN MACHINE LEARNING")
print("=" * 70)

print("""
This module covers:
1. Differential privacy fundamentals
2. Opacus for PyTorch
3. TensorFlow Privacy
4. Privacy accounting and composition
5. Best practices for private ML
""")


# -------------------------------------------------------------------------
# 1.1 Basic DP Mechanisms
# -------------------------------------------------------------------------

print("\n" + "=" * 70)
print("SECTION 1: DIFFERENTIAL PRIVACY FUNDAMENTALS")
print("=" * 70)

print("\n" + "-" * 70)
print("1.1 Basic Differential Privacy Mechanisms")
print("-" * 70)

print("""
CORE DP MECHANISMS:

1. LAPLACE MECHANISM
   - Adds Laplace-distributed noise
   - For numeric queries with bounded sensitivity
   - Noise scale = sensitivity / epsilon

2. GAUSSIAN MECHANISM
   - Adds Gaussian-distributed noise
   - Provides (ε, δ)-DP
   - More common in deep learning

3. EXPONENTIAL MECHANISM
   - For selecting from discrete options
   - Preserves utility while maintaining privacy

4. RANDOMIZED RESPONSE
   - Classic technique for surveys
   - Answer truthfully with probability p
   - Lie with probability 1-p
""")


def laplace_mechanism(true_value: float, sensitivity: float, epsilon: float) -> float:
    """
    Apply the Laplace mechanism for differential privacy.

    The Laplace mechanism adds noise drawn from a Laplace distribution
    to achieve ε-differential privacy.

    Parameters:
    -----------
    true_value : float
        The actual value to be privatized
    sensitivity : float
        The maximum change in the query output when one record changes
        (L1 sensitivity)
    epsilon : float
        Privacy budget (lower = more privacy)

    Returns:
    --------
    float
        Privatized value

    Mathematical basis:
    ------------------
    For a query f with L1 sensitivity Δf, adding noise from:
        Lap(Δf / ε)
    achieves ε-differential privacy.
    """
    # Scale parameter of Laplace distribution
    scale = sensitivity / epsilon

    # Draw noise from Laplace distribution
    noise = np.random.laplace(0, scale)

    return true_value + noise


def gaussian_mechanism(
    true_value: float,
    sensitivity: float,
    epsilon: float,
    delta: float
) -> float:
    """
    Apply the Gaussian mechanism for (ε, δ)-differential privacy.

    Parameters:
    -----------
    true_value : float
        The actual value to be privatized
    sensitivity : float
        L2 sensitivity of the query
    epsilon : float
        Privacy budget
    delta : float
        Probability of privacy breach (typically << 1/n)

    Returns:
    --------
    float
        Privatized value

    Mathematical basis:
    ------------------
    For a query f with L2 sensitivity Δf, adding noise from:
        N(0, σ²) where σ = Δf × √(2 ln(1.25/δ)) / ε
    achieves (ε, δ)-differential privacy.
    """
    # Calculate noise standard deviation
    sigma = sensitivity * np.sqrt(2 * np.log(1.25 / delta)) / epsilon

    # Draw noise from Gaussian distribution
    noise = np.random.normal(0, sigma)

    return true_value + noise


# Demonstrate basic mechanisms
print("\n" + "-" * 70)
print("1.2 Demonstrating Basic Mechanisms")
print("-" * 70)

# Example: Computing average salary with DP
true_avg_salary = 75000
salary_sensitivity = 200000 / 1000  # Max salary / number of people

print("\nExample: Private computation of average salary")
print(f"True average: ${true_avg_salary:,.0f}")
print(f"Sensitivity: ${salary_sensitivity:,.0f}")

print("\nLaplace Mechanism Results (100 trials each):")
for eps in [0.1, 1.0, 10.0]:
    private_values = [
        laplace_mechanism(true_avg_salary, salary_sensitivity, eps)
        for _ in range(100)
    ]
    mean_error = np.mean(np.abs(np.array(private_values) - true_avg_salary))
    print(f"  ε={eps:4.1f}: Mean absolute error = ${mean_error:,.0f}")

print("\nGaussian Mechanism Results (100 trials each):")
for eps in [0.1, 1.0, 10.0]:
    private_values = [
        gaussian_mechanism(true_avg_salary, salary_sensitivity, eps, 1e-5)
        for _ in range(100)
    ]
    mean_error = np.mean(np.abs(np.array(private_values) - true_avg_salary))
    print(f"  ε={eps:4.1f}: Mean absolute error = ${mean_error:,.0f}")


# -------------------------------------------------------------------------
# 1.3 Privacy Composition
# -------------------------------------------------------------------------

print("\n" + "-" * 70)
print("1.3 Privacy Composition")
print("-" * 70)

print("""
COMPOSITION THEOREMS:

When running multiple DP mechanisms, privacy "composes" (degrades):

1. BASIC COMPOSITION
   - Running k ε-DP algorithms gives kε-DP
   - Very loose bound

2. ADVANCED COMPOSITION
   - For k (ε, δ)-DP algorithms:
   - Total privacy ≈ (√(2k ln(1/δ')) × ε + k×ε×(e^ε - 1), k×δ + δ')
   - Much tighter for many iterations

3. RÉNYI DP COMPOSITION
   - Uses Rényi divergence
   - Tightest bounds for deep learning
   - Used by Opacus and TF Privacy

IMPLICATIONS FOR ML:
- Each training epoch uses privacy budget
- More epochs = more privacy cost
- Must account for total budget used
""")


# =============================================================================
# SECTION 2: OPACUS (PyTorch Differential Privacy)
# =============================================================================
"""
Opacus is Meta's library for training PyTorch models with differential privacy.

Key Features:
- Drop-in replacement for standard training
- Automatic privacy accounting
- Per-sample gradient clipping
- Works with most PyTorch models
"""

print("\n" + "=" * 70)
print("SECTION 2: OPACUS (PyTorch)")
print("=" * 70)

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader, TensorDataset
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("PyTorch not available.")

try:
    from opacus import PrivacyEngine
    from opacus.validators import ModuleValidator
    from opacus.utils.batch_memory_manager import BatchMemoryManager
    from opacus.accountants.utils import get_noise_multiplier
    OPACUS_AVAILABLE = True
    print("\nOpacus successfully imported!")
except ImportError:
    OPACUS_AVAILABLE = False
    print("\nOpacus not installed. Install with: pip install opacus")


if TORCH_AVAILABLE and OPACUS_AVAILABLE:
    print("\n" + "-" * 70)
    print("2.1 Opacus Architecture Overview")
    print("-" * 70)

    print("""
    OPACUS COMPONENTS:

    1. PrivacyEngine
       - Wraps model, optimizer, and data loader
       - Tracks privacy budget
       - Handles gradient clipping and noise addition

    2. Module Validation
       - Checks if model is compatible with DP
       - Some layers (e.g., BatchNorm) need replacement
       - Provides automatic fixes

    3. Privacy Accountant
       - Tracks ε spent during training
       - Uses Rényi DP for tight bounds
       - Warns when budget exceeded

    HOW IT WORKS:
    -------------
    Standard SGD:
        θ ← θ - η × (1/B) × Σ∇L(x_i, θ)

    DP-SGD (simplified):
        1. Compute per-sample gradients: g_i = ∇L(x_i, θ)
        2. Clip each gradient: g̃_i = g_i × min(1, C/||g_i||)
        3. Aggregate and add noise: g̃ = (1/B) × (Σg̃_i + N(0, σ²C²I))
        4. Update: θ ← θ - η × g̃

    Where:
    - C = clipping norm (max gradient magnitude)
    - σ = noise multiplier (controls privacy)
    - B = batch size
    """)

    # -------------------------------------------------------------------------
    # 2.2 Create Dataset and Model
    # -------------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("2.2 Creating Dataset and Model")
    print("-" * 70)

    # Create synthetic classification dataset
    np.random.seed(42)
    torch.manual_seed(42)

    n_samples = 1000
    n_features = 20

    # Generate data
    X = np.random.randn(n_samples, n_features).astype(np.float32)
    # Create linearly separable classes with some noise
    true_weights = np.random.randn(n_features)
    y = (X @ true_weights + np.random.randn(n_samples) * 0.5 > 0).astype(np.int64)

    # Convert to PyTorch
    X_tensor = torch.from_numpy(X)
    y_tensor = torch.from_numpy(y)

    # Split
    train_size = int(0.8 * n_samples)
    X_train, X_test = X_tensor[:train_size], X_tensor[train_size:]
    y_train, y_test = y_tensor[:train_size], y_tensor[train_size:]

    # Create DataLoaders
    train_dataset = TensorDataset(X_train, y_train)
    test_dataset = TensorDataset(X_test, y_test)

    batch_size = 64
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size)

    print(f"Dataset: {n_samples} samples, {n_features} features")
    print(f"Train: {train_size} samples")
    print(f"Test: {n_samples - train_size} samples")
    print(f"Batch size: {batch_size}")

    # Define model
    class SimpleClassifier(nn.Module):
        """A simple neural network for binary classification."""

        def __init__(self, input_dim):
            super().__init__()
            self.layers = nn.Sequential(
                nn.Linear(input_dim, 64),
                nn.ReLU(),
                nn.Linear(64, 32),
                nn.ReLU(),
                nn.Linear(32, 2)
            )

        def forward(self, x):
            return self.layers(x)

    # Create model
    model = SimpleClassifier(n_features)

    # Validate and fix model for DP compatibility
    print("\nValidating model for DP compatibility...")
    errors = ModuleValidator.validate(model, strict=False)

    if errors:
        print(f"  Found {len(errors)} compatibility issues. Fixing...")
        model = ModuleValidator.fix(model)
        print("  Model fixed!")
    else:
        print("  Model is DP-compatible!")

    # -------------------------------------------------------------------------
    # 2.3 Training Without DP (Baseline)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("2.3 Training WITHOUT Differential Privacy (Baseline)")
    print("-" * 70)

    def train_epoch(model, train_loader, optimizer, criterion):
        """Train for one epoch."""
        model.train()
        total_loss = 0
        correct = 0
        total = 0

        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            _, predicted = outputs.max(1)
            correct += predicted.eq(y_batch).sum().item()
            total += y_batch.size(0)

        return total_loss / len(train_loader), correct / total

    def evaluate(model, test_loader):
        """Evaluate model accuracy."""
        model.eval()
        correct = 0
        total = 0

        with torch.no_grad():
            for X_batch, y_batch in test_loader:
                outputs = model(X_batch)
                _, predicted = outputs.max(1)
                correct += predicted.eq(y_batch).sum().item()
                total += y_batch.size(0)

        return correct / total

    # Train baseline model
    baseline_model = SimpleClassifier(n_features)
    baseline_optimizer = optim.Adam(baseline_model.parameters(), lr=0.01)
    criterion = nn.CrossEntropyLoss()

    print("\nTraining baseline (non-private) model...")
    n_epochs = 10

    for epoch in range(n_epochs):
        loss, train_acc = train_epoch(
            baseline_model, train_loader, baseline_optimizer, criterion
        )

    test_acc = evaluate(baseline_model, test_loader)
    print(f"\nBaseline Results:")
    print(f"  Train Accuracy: {train_acc:.1%}")
    print(f"  Test Accuracy: {test_acc:.1%}")

    # -------------------------------------------------------------------------
    # 2.4 Training WITH DP using Opacus
    # -------------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("2.4 Training WITH Differential Privacy (Opacus)")
    print("-" * 70)

    # Privacy parameters
    target_epsilon = 8.0    # Privacy budget
    target_delta = 1e-5     # Failure probability
    max_grad_norm = 1.0     # Gradient clipping norm

    print(f"\nPrivacy Parameters:")
    print(f"  Target ε (epsilon): {target_epsilon}")
    print(f"  δ (delta): {target_delta}")
    print(f"  Max gradient norm (C): {max_grad_norm}")

    # Create fresh model for DP training
    dp_model = SimpleClassifier(n_features)
    dp_model = ModuleValidator.fix(dp_model)  # Ensure DP compatibility

    dp_optimizer = optim.Adam(dp_model.parameters(), lr=0.01)

    # Wrap with PrivacyEngine
    print("\nInitializing PrivacyEngine...")

    privacy_engine = PrivacyEngine()

    dp_model, dp_optimizer, dp_train_loader = privacy_engine.make_private_with_epsilon(
        module=dp_model,
        optimizer=dp_optimizer,
        data_loader=train_loader,
        epochs=n_epochs,
        target_epsilon=target_epsilon,
        target_delta=target_delta,
        max_grad_norm=max_grad_norm,
    )

    print(f"  Noise multiplier (σ): {dp_optimizer.noise_multiplier:.3f}")
    print(f"  Expected ε after training: {target_epsilon}")

    # Train with DP
    print("\nTraining with differential privacy...")

    for epoch in range(n_epochs):
        dp_model.train()
        total_loss = 0
        correct = 0
        total = 0

        for X_batch, y_batch in dp_train_loader:
            dp_optimizer.zero_grad()
            outputs = dp_model(X_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            dp_optimizer.step()

            total_loss += loss.item()
            _, predicted = outputs.max(1)
            correct += predicted.eq(y_batch).sum().item()
            total += y_batch.size(0)

        # Get current privacy spent
        epsilon = privacy_engine.get_epsilon(target_delta)

        if (epoch + 1) % 2 == 0:
            print(f"  Epoch {epoch+1}: Loss={total_loss/len(dp_train_loader):.4f}, "
                  f"Acc={correct/total:.1%}, ε={epsilon:.2f}")

    # Final evaluation
    dp_test_acc = evaluate(dp_model, test_loader)
    final_epsilon = privacy_engine.get_epsilon(target_delta)

    print(f"\nDifferentially Private Results:")
    print(f"  Test Accuracy: {dp_test_acc:.1%}")
    print(f"  Final ε spent: {final_epsilon:.2f}")
    print(f"  Privacy guarantee: ({final_epsilon:.2f}, {target_delta})-DP")

    # Compare results
    print("\n" + "-" * 70)
    print("2.5 Comparison: Private vs Non-Private")
    print("-" * 70)

    print(f"""
    Model           | Test Accuracy | Privacy Guarantee
    ----------------+---------------+------------------
    Baseline        | {test_acc:.1%}         | None
    DP (ε={final_epsilon:.1f})     | {dp_test_acc:.1%}         | ({final_epsilon:.2f}, {target_delta})-DP

    Accuracy Drop: {(test_acc - dp_test_acc)*100:.1f} percentage points

    INTERPRETATION:
    - The DP model provides mathematical privacy guarantees
    - There's a privacy-utility tradeoff (some accuracy loss)
    - The guarantee means: removing any single training example
      would result in nearly identical model outputs
    """)

else:
    print("""
    OPACUS CONCEPTUAL OVERVIEW:

    Without PyTorch/Opacus installed, here's what the code would do:

    1. VALIDATE MODEL
       - Check for DP-incompatible layers
       - Replace BatchNorm with GroupNorm
       - Ensure gradient computation works per-sample

    2. INITIALIZE PRIVACY ENGINE
       - Wrap model, optimizer, data loader
       - Calculate noise multiplier for target (ε, δ)
       - Set up privacy accounting

    3. TRAIN WITH DP
       - Each batch:
         a) Compute per-sample gradients
         b) Clip each gradient to max_norm
         c) Add calibrated Gaussian noise
         d) Update model parameters
       - Track cumulative privacy spent

    4. PRIVACY ACCOUNTING
       - After training, know exact (ε, δ) guarantee
       - Can verify budget wasn't exceeded
    """)


# =============================================================================
# SECTION 3: TENSORFLOW PRIVACY
# =============================================================================
"""
TensorFlow Privacy provides DP training for TensorFlow/Keras models.

Similar concepts to Opacus but for the TensorFlow ecosystem.
"""

print("\n" + "=" * 70)
print("SECTION 3: TENSORFLOW PRIVACY")
print("=" * 70)

try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("TensorFlow not available.")

try:
    from tensorflow_privacy.privacy.optimizers.dp_optimizer_keras import DPKerasSGDOptimizer
    from tensorflow_privacy.privacy.analysis import compute_dp_sgd_privacy_lib
    TF_PRIVACY_AVAILABLE = True
    print("\nTensorFlow Privacy successfully imported!")
except ImportError:
    TF_PRIVACY_AVAILABLE = False
    print("\nTensorFlow Privacy not installed.")
    print("Install with: pip install tensorflow-privacy tensorflow")

print("\n" + "-" * 70)
print("3.1 TensorFlow Privacy Architecture")
print("-" * 70)

print("""
TENSORFLOW PRIVACY COMPONENTS:

1. DP OPTIMIZERS
   - DPKerasSGDOptimizer: DP version of SGD
   - DPKerasAdamOptimizer: DP version of Adam
   - Drop-in replacements for standard optimizers

2. PRIVACY ACCOUNTING
   - compute_dp_sgd_privacy: Calculate ε for given parameters
   - Uses Rényi DP for tight bounds

3. MODEL REQUIREMENTS
   - Must use vectorized loss (reduction='none')
   - Standard Keras layers work

EXAMPLE CODE STRUCTURE:
```python
import tensorflow as tf
from tensorflow_privacy.privacy.optimizers.dp_optimizer_keras import DPKerasSGDOptimizer
from tensorflow_privacy.privacy.analysis.compute_dp_sgd_privacy_lib import compute_dp_sgd_privacy

# Privacy parameters
l2_norm_clip = 1.0
noise_multiplier = 0.5
num_microbatches = 1
learning_rate = 0.01

# Create DP optimizer
optimizer = DPKerasSGDOptimizer(
    l2_norm_clip=l2_norm_clip,
    noise_multiplier=noise_multiplier,
    num_microbatches=num_microbatches,
    learning_rate=learning_rate
)

# Build model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(10)
])

# Compile - IMPORTANT: use reduction='none' for the loss
model.compile(
    optimizer=optimizer,
    loss=tf.keras.losses.CategoricalCrossentropy(
        from_logits=True,
        reduction=tf.losses.Reduction.NONE  # Required for DP!
    ),
    metrics=['accuracy']
)

# Train
model.fit(x_train, y_train, epochs=10, batch_size=64)

# Compute privacy guarantee
epsilon, _ = compute_dp_sgd_privacy(
    n=len(x_train),
    batch_size=64,
    noise_multiplier=noise_multiplier,
    epochs=10,
    delta=1e-5
)
print(f'Privacy guarantee: ε = {epsilon}')
```
""")

if TF_AVAILABLE and TF_PRIVACY_AVAILABLE:
    print("\n" + "-" * 70)
    print("3.2 Privacy Analysis with TensorFlow Privacy")
    print("-" * 70)

    # Demonstrate privacy analysis
    print("\nComputing privacy guarantees for different configurations:")
    print("-" * 60)

    configs = [
        {"noise_multiplier": 0.5, "epochs": 10},
        {"noise_multiplier": 1.0, "epochs": 10},
        {"noise_multiplier": 1.0, "epochs": 50},
        {"noise_multiplier": 2.0, "epochs": 50},
    ]

    n_train = 10000
    batch_size = 64

    print(f"{'Noise σ':>10} | {'Epochs':>6} | {'ε':>10}")
    print("-" * 35)

    for config in configs:
        eps, _ = compute_dp_sgd_privacy_lib.compute_dp_sgd_privacy(
            n=n_train,
            batch_size=batch_size,
            noise_multiplier=config["noise_multiplier"],
            epochs=config["epochs"],
            delta=1e-5
        )
        print(f"{config['noise_multiplier']:>10.1f} | {config['epochs']:>6} | {eps:>10.2f}")

    print("""
    OBSERVATIONS:
    - Higher noise multiplier → lower ε (more privacy)
    - More epochs → higher ε (privacy degrades)
    - Must balance training quality with privacy budget
    """)


# =============================================================================
# SECTION 4: PRACTICAL CONSIDERATIONS
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 4: PRACTICAL CONSIDERATIONS")
print("=" * 70)

print("\n" + "-" * 70)
print("4.1 Choosing Privacy Parameters")
print("-" * 70)

print("""
GUIDELINES FOR PARAMETER SELECTION:

1. EPSILON (ε) - Privacy Budget
   --------------------------------
   ε ≤ 1:    Strong privacy (research standard)
   ε ≤ 10:   Reasonable privacy for many applications
   ε > 10:   Weak privacy (may not provide meaningful protection)

   Industry examples:
   - Apple (iOS keyboard): ε = 2-4 per day
   - Google (RAPPOR): ε = 2-9
   - US Census: ε varied by query type

2. DELTA (δ) - Failure Probability
   --------------------------------
   Should be << 1/n where n is dataset size
   Common choice: 1/n or 1e-5

3. GRADIENT CLIPPING (C)
   --------------------------------
   Too small: Underfits (gradients always clipped)
   Too large: More noise needed for same privacy
   Start with median gradient norm, tune empirically

4. NOISE MULTIPLIER (σ)
   --------------------------------
   Determined by target ε, δ, and number of steps
   Use privacy accounting tools to compute

5. BATCH SIZE
   --------------------------------
   Larger batches → can use smaller noise per example
   Privacy amplification via subsampling
   Trade-off with memory and computation
""")

print("\n" + "-" * 70)
print("4.2 Common Pitfalls and Solutions")
print("-" * 70)

print("""
COMMON PITFALLS:

1. WRONG PRIVACY ACCOUNTING
   ❌ Ignoring composition across epochs
   ❌ Not accounting for hyperparameter tuning
   ✅ Use proper privacy accountants (Opacus, TF Privacy)

2. MODEL ARCHITECTURE ISSUES
   ❌ Using BatchNorm (not DP-compatible)
   ❌ Variable-length inputs without proper handling
   ✅ Use GroupNorm or LayerNorm
   ✅ Pad sequences to fixed length

3. DATA PREPROCESSING LEAKS
   ❌ Computing statistics on private data without DP
   ❌ Data-dependent preprocessing
   ✅ Use public statistics or DP statistics
   ✅ Fixed preprocessing pipelines

4. HYPERPARAMETER TUNING
   ❌ Tuning on private data without accounting
   ✅ Budget for hyperparameter search
   ✅ Use public proxy datasets

5. EVALUATION LEAKS
   ❌ Evaluating on test set without privacy accounting
   ✅ Include evaluation in privacy budget
   ✅ Use held-out public data if possible
""")

print("\n" + "-" * 70)
print("4.3 Privacy-Utility Trade-off Visualization")
print("-" * 70)

# Simulate privacy-utility trade-off
epsilons = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0]
# Simulated accuracy values (in practice, would come from experiments)
# These follow a typical pattern: very low acc at low ε, improving with higher ε
simulated_accuracy = [0.52, 0.58, 0.65, 0.72, 0.80, 0.85, 0.88, 0.89]

plt.figure(figsize=(10, 6))
plt.semilogx(epsilons, simulated_accuracy, 'bo-', markersize=10, linewidth=2)
plt.axhline(y=0.90, color='r', linestyle='--', label='Non-private baseline')
plt.axvline(x=1.0, color='g', linestyle='--', alpha=0.5, label='Strong privacy threshold')
plt.axvline(x=10.0, color='orange', linestyle='--', alpha=0.5, label='Weak privacy threshold')

plt.xlabel('Privacy Budget (ε)', fontsize=12)
plt.ylabel('Test Accuracy', fontsize=12)
plt.title('Privacy-Utility Trade-off in Differentially Private ML', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.ylim([0.5, 0.95])

plt.tight_layout()
plt.savefig('privacy_utility_tradeoff.png', dpi=150, bbox_inches='tight')
plt.close()

print("Saved: privacy_utility_tradeoff.png")

print("""
The plot shows the typical privacy-utility trade-off:
- At very low ε (strong privacy), accuracy is limited
- Accuracy improves as ε increases
- Eventually reaches near non-private performance
- The "knee" of the curve is often the sweet spot
""")


# =============================================================================
# SECTION 5: BEST PRACTICES SUMMARY
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 5: BEST PRACTICES FOR DIFFERENTIAL PRIVACY")
print("=" * 70)

print("""
BEST PRACTICES CHECKLIST:

1. BEFORE TRAINING
   □ Determine required privacy level (ε, δ)
   □ Validate model architecture for DP compatibility
   □ Ensure preprocessing doesn't leak information
   □ Set aside privacy budget for hyperparameter tuning

2. DURING TRAINING
   □ Use proper DP optimizers (Opacus, TF Privacy)
   □ Monitor privacy budget consumption
   □ Use appropriate batch sizes for privacy amplification
   □ Tune gradient clipping norm empirically

3. AFTER TRAINING
   □ Report final (ε, δ) guarantee
   □ Document all privacy-relevant parameters
   □ Validate that budget wasn't exceeded
   □ Consider privacy of the evaluation phase

4. DEPLOYMENT
   □ Ensure model weights are the only thing released
   □ No additional queries on training data
   □ Document privacy guarantees for users
   □ Plan for model updates (additional privacy cost)

5. SPECIAL CONSIDERATIONS
   □ Federated learning: Track per-user privacy
   □ Multiple models: Composition of privacy
   □ Public data: Can use for preprocessing/tuning
   □ Synthetic data: Consider DP synthetic data generation

RESOURCES:
- Opacus: https://opacus.ai/
- TensorFlow Privacy: https://github.com/tensorflow/privacy
- DP Theory: https://differentialprivacy.org/
- NIST Guidelines: https://www.nist.gov/privacy-framework
""")


print("\n" + "=" * 70)
print("END OF DIFFERENTIAL PRIVACY EXAMPLES")
print("=" * 70)

print("""
KEY TAKEAWAYS:

1. Differential privacy provides mathematical privacy guarantees
   - ε controls privacy strength (lower = more private)
   - δ is the probability of privacy breach

2. Libraries make DP ML practical
   - Opacus for PyTorch
   - TensorFlow Privacy for TensorFlow
   - Handle gradient clipping and noise addition

3. There's always a privacy-utility trade-off
   - More privacy → more noise → lower accuracy
   - Choose ε based on application requirements

4. Privacy accounting is crucial
   - Track total privacy spent
   - Account for all data access
   - Use composition theorems

5. Implementation details matter
   - Model architecture compatibility
   - Preprocessing considerations
   - Proper hyperparameter tuning

FILES GENERATED:
- privacy_utility_tradeoff.png: Visualization of privacy-utility trade-off
""")
