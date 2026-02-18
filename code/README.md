# Trustworthy AI - Code Examples

This folder contains canonical Python implementations demonstrating key techniques for building and auditing trustworthy AI systems. Each file provides verbose explanations of the underlying concepts and practical, runnable code examples.

## Contents

| File | Topic | Libraries Used |
|------|-------|----------------|
| [bias_testing.py](./bias_testing.py) | Bias Detection & Mitigation | AIF360, Fairlearn |
| [explainability.py](./explainability.py) | Model Explainability | SHAP, LIME |
| [adversarial_testing.py](./adversarial_testing.py) | Adversarial Robustness Testing | ART (Adversarial Robustness Toolbox), PyRIT |
| [eval_frameworks.py](./eval_frameworks.py) | Model Evaluation Frameworks | Inspect AI, Custom Evals |
| [differential_privacy.py](./differential_privacy.py) | Privacy-Preserving ML | Opacus, TensorFlow Privacy |

## Installation

To run these examples, install the required dependencies:

```bash
# Core dependencies
pip install numpy pandas scikit-learn matplotlib

# Bias testing
pip install aif360 fairlearn

# Explainability
pip install shap lime

# Adversarial testing
pip install adversarial-robustness-toolbox
# PyRIT requires separate installation: pip install pyrit

# Evaluation frameworks
pip install inspect-ai

# Differential privacy
pip install opacus
pip install tensorflow-privacy tensorflow
```

## Usage

Each file is self-contained and can be run directly:

```bash
python bias_testing.py
python explainability.py
python adversarial_testing.py
python eval_frameworks.py
python differential_privacy.py
```

## Structure

Each code file follows a consistent structure:

1. **Conceptual Introduction** - Explains the technique and why it matters for trustworthy AI
2. **Library Overview** - Describes the libraries used and their key features
3. **Data Preparation** - Sets up example data (usually using standard datasets)
4. **Implementation Examples** - Multiple practical examples with verbose comments
5. **Interpretation Guide** - How to interpret the results
6. **Best Practices** - Recommendations for production use

## Related Documentation

These code examples complement the theoretical content in the main repository:

- Bias Testing → [pages/bias.md](../pages/bias.md)
- Explainability → [pages/transparency.md](../pages/transparency.md)
- Adversarial Testing → [pages/attacks.md](../pages/attacks.md)
- Differential Privacy → [pages/diff_priv.md](../pages/diff_priv.md)

## Notes

- Examples use synthetic or standard benchmark datasets for reproducibility
- Code is written for educational clarity, not production optimization
- All examples include extensive inline documentation
- Error handling is minimal to keep focus on the core concepts
