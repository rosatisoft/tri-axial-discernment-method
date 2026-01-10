"""
© 2026 Ernesto Rosati  
Este documento está licenciado bajo Apache 2.0  
Publicación oficial y DOI disponible en Zenodo
https://doi.org/10.5281/zenodo.18182173

ia_dataset_example.py

Example: applying the Tri-Axial Method of Discernment (F–C–P)
to a practical IA scenario:

    Claim:
        "Using the full dataset will always maximize accuracy
         without significant extra cost."

We evaluate this claim with:
- Foundation (F): factual / empirical grounding
- Context (C): situational / institutional frame
- Principle (P): systemic and ethical impact

This script is meant to be run from the repository root:

    python examples/ia_dataset_example.py
"""

import os
import sys

# Ensure we can import the module from ../src
CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(CURRENT_DIR, "..", "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from tri_axial_discernment import (
    compute_discernment_from_criteria,
)


def main() -> None:
    # --- 1) Describe the scenario (for humans) -----------------------------
    claim = (
        "Using the full dataset will always maximize accuracy "
        "without significant extra cost."
    )

    print("IA Dataset Optimization Example")
    print("================================")
    print(f"Claim under evaluation:\n  {claim}\n")

    # --- 2) Criteria scores (0–1) for each axis ---------------------------
    # These values mirror the example table in the conceptual document.

    # I. FOUNDATION (F)
    # - Benchmarks show overfitting with very large datasets
    # - Some empirical evidence contradicts the 'always' / 'no cost' claim
    F_criteria = [
        0.6,  # Source is partially trustworthy (benchmarks exist)
        0.4,  # Not fully consistent with known ML literature
        0.5,  # Matches some real-world behavior, but not all
        0.3,  # Requires strong assumptions about "no extra cost"
        0.4,  # Contradicted by evidence of energy/compute overhead
    ]

    # II. CONTEXT (C)
    # - Pressure for maximum accuracy
    # - Business incentives may ignore sustainability
    C_criteria = [
        0.7,  # Context is clear: maximize accuracy
        0.5,  # Some emotional / competitive pressure is present
        0.8,  # Not targeting groups, but impacts dev teams (burnout)
        0.4,  # Influenced by commercial agenda
        0.6,  # Only partly realistic regarding compute/energy limits
    ]

    # III. PRINCIPLE (P)
    # - We use a principle of "minimize entropy and maximize coherence"
    P_criteria = [
        0.3,  # Increases resource waste → more systemic "entropy"
        0.5,  # Improves accuracy but harms long-term sustainability
        0.6,  # Some respect for human/institutional constraints
        0.9,  # Does not create hate/division, only internal trade-offs
        0.4,  # Does not really open new responsible paths of action
    ]

    # --- 3) Compute discernment -------------------------------------------
    result = compute_discernment_from_criteria(
        foundation_criteria=F_criteria,
        context_criteria=C_criteria,
        principle_criteria=P_criteria,
        notes={
            "scenario": "IA training dataset optimization",
            "interpretation": (
                "Full dataset use should be questioned; a curated subset "
                "may save 30–50% of resources with similar performance."
            ),
        },
    )

    # --- 4) Print results in a human-readable way -------------------------
    print("Axis scores (0–1):")
    print(f"  Foundation (F): {result.foundation:.2f}")
    print(f"  Context    (C): {result.context:.2f}")
    print(f"  Principle  (P): {result.principle:.2f}")
    print()
    print(f"Overall discernment D: {result.score:.2f}")
    print(f"Suggested action     : {result.action}")
    print()

    if result.notes:
        print("Notes:")
        for key, value in result.notes.items():
            print(f"  - {key}: {value}")


if __name__ == "__main__":
    main()
