"""
tri_axial_discernment.py

Core implementation of the Tri-Axial Method of Discernment (F–C–P):
- F: Foundation (factual grounding)
- C: Context (situational frame and external forces)
- P: Principle (systemic / ethical implications of action)

This module is axioma-agnostic: it does not impose any specific
metaphysical or doctrinal foundation. It simply provides a numerical
and procedural structure to evaluate:

    Discernment D = f(F, C, P)

Typical workflow:
1. Score each axis (F, C, P) with values between 0 and 1.
2. Compute the overall discernment score D.
3. Use the suggested action as a decision aid.

Author: Ernesto Rosati Beristáin (conceptual framework)
Code helper: ChatGPT (implementation)
"""

from dataclasses import dataclass
from typing import List, Dict, Optional


def clamp(value: float, min_value: float = 0.0, max_value: float = 1.0) -> float:
    """Limit a numeric value to the [min_value, max_value] interval."""
    return max(min_value, min(max_value, value))


def average(scores: List[float]) -> float:
    """Return the average of a list of scores in [0, 1]. Empty list → 0.0."""
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


@dataclass
class AxisScores:
    """Container for axis-level scores (already averaged)."""
    foundation: float  # F
    context: float     # C
    principle: float   # P


@dataclass
class DiscernmentResult:
    """
    Result of applying the Tri-Axial Method.

    Attributes:
        foundation: averaged score for the Foundation axis (0–1)
        context: averaged score for the Context axis (0–1)
        principle: averaged score for the Principle axis (0–1)
        score: overall discernment D in [0, 1]
        action: suggested action according to the D spectrum
        notes: optional dictionary with extra metadata (e.g., comments)
    """
    foundation: float
    context: float
    principle: float
    score: float
    action: str
    notes: Optional[Dict[str, str]] = None


def interpret_action(score: float) -> str:
    """
    Map the overall discernment score D to a recommended action.

    Spectrum (can be adjusted to match the conceptual framework):

        0.80–1.00 → Adopt and, if useful, share
        0.50–0.79 → Consider valid but complement with further analysis
        0.20–0.49 → Question, correct, contrast sources
        0.00–0.19 → Discard or denounce if harmful / false
    """
    score = clamp(score)

    if score >= 0.80:
        return "Adopt and, if useful, share."
    if score >= 0.50:
        return "Consider valid, but complement with further analysis."
    if score >= 0.20:
        return "Question, correct, and contrast with additional sources."
    return "Discard or denounce if it is harmful or clearly false."


def compute_axes_from_criteria(
    foundation_criteria: List[float],
    context_criteria: List[float],
    principle_criteria: List[float],
) -> AxisScores:
    """
    Compute axis scores F, C, P from lists of criteria (each score in [0, 1]).

    This function mirrors the human evaluation table:
    - Several questions per axis (e.g., 5 for F, 5 for C, 5 for P).
    - Each answered with a score between 0 and 1.
    - The axis value is the average of its criteria.

    Example:
        F_criteria = [0.6, 0.4, 0.5, 0.3, 0.4]
        C_criteria = [...]
        P_criteria = [...]

        axes = compute_axes_from_criteria(F_criteria, C_criteria, P_criteria)
    """
    F = clamp(average(foundation_criteria))
    C = clamp(average(context_criteria))
    P = clamp(average(principle_criteria))
    return AxisScores(foundation=F, context=C, principle=P)


def compute_discernment(
    foundation: float,
    context: float,
    principle: float,
    notes: Optional[Dict[str, str]] = None,
) -> DiscernmentResult:
    """
    Compute the overall discernment score D and recommended action
    from axis-level scores F, C, P.

        D = (F + C + P) / 3

    All inputs are clamped to [0, 1].
    """
    F = clamp(foundation)
    C = clamp(context)
    P = clamp(principle)

    D = (F + C + P) / 3.0
    action = interpret_action(D)

    return DiscernmentResult(
        foundation=F,
        context=C,
        principle=P,
        score=D,
        action=action,
        notes=notes,
    )


def compute_discernment_from_criteria(
    foundation_criteria: List[float],
    context_criteria: List[float],
    principle_criteria: List[float],
    notes: Optional[Dict[str, str]] = None,
) -> DiscernmentResult:
    """
    High-level helper:
    1. Take raw criteria scores (0–1) for each axis.
    2. Compute axis averages.
    3. Compute overall discernment D and action.

    This is the most convenient entry point for typical use.
    """
    axes = compute_axes_from_criteria(
        foundation_criteria,
        context_criteria,
        principle_criteria,
    )
    return compute_discernment(
        foundation=axes.foundation,
        context=axes.context,
        principle=axes.principle,
        notes=notes,
    )


if __name__ == "__main__":
    # Simple manual test / demo.
    # Example: IA training decision, similar to the one in the paper.
    F_criteria = [0.6, 0.4, 0.5, 0.3, 0.4]  # Foundation axis
    C_criteria = [0.7, 0.5, 0.8, 0.4, 0.6]  # Context axis
    P_criteria = [0.3, 0.5, 0.6, 0.9, 0.4]  # Principle axis

    result = compute_discernment_from_criteria(
        F_criteria,
        C_criteria,
        P_criteria,
        notes={"example": "Training dataset optimization case"},
    )

    print("Tri-Axial Discernment Result")
    print("----------------------------")
    print(f"Foundation (F): {result.foundation:.2f}")
    print(f"Context    (C): {result.context:.2f}")
    print(f"Principle  (P): {result.principle:.2f}")
    print(f"Overall D     : {result.score:.2f}")
    print(f"Action        : {result.action}")
    if result.notes:
        print(f"Notes         : {result.notes}")
