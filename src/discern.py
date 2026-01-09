"""
discern.py
Core implementation of the Tri-Axial Discernment Algorithm (F–C–P)

This module evaluates claims or assertions using:
F = Fundamento (Reality grounding)
C = Context (Where/why the claim exists)
P = Principle (Consequences + coherence)

Returns:
- D score (0.0–1.0)
- Action recommendation
- Breakdown of F, C, P values
"""

def clamp(value, min_value=0.0, max_value=1.0):
    return max(min_value, min(max_value, value))

def evaluate_fundamento(claim, metadata=None):
    """Score Fundamento axis (F)"""
    F = 1.0
    text = claim.lower()

    if "fuente no verificable" in text or "no verificado" in text:
        F *= 0.5
    if "contradice evidencia" in text:
        F *= 0.2
    if metadata and "consistente" in metadata.lower():
        F *= 1.1
    if "suposicion" in text or "suposiciones" in text:
        F *= 0.7

    return clamp(F)

def evaluate_context(claim, metadata=None):
    """Score Context axis (C)"""
    C = 1.0
    text = claim.lower()

    if "emocional" in text or "viral" in text:
        C *= 0.5
    if "grupos vulnerables" in text or "afecta reputaciones" in text:
        C *= 0.7
    if "distorsion" in text or "interes externo" in text:
        C *= 0.6
    if metadata and "contextualizado" in metadata.lower():
        C *= 1.1

    return clamp(C)

def evaluate_principle(claim, metadata=None):
    """Score Principle axis (P)"""
    P = 1.0
    text = claim.lower()

    if "caos" in text or "division" in text:
        P *= 0.5
    if "acciones constructivas" in text:
        P *= 1.1
    if "contradice etica" in text or "indignidad" in text:
        P *= 0.3
    if "revela patrones" in text:
        P *= 1.2

    return clamp(P)

def discern(claim, metadata=None):
    """Main driver"""
    F = evaluate_fundamento(claim, metadata)
    C = evaluate_context(claim, metadata)
    P = evaluate_principle(claim, metadata)

    D = (F + C + P) / 3

    if D > 0.80:
        action = "Adoptar / Difundir"
    elif 0.50 <= D <= 0.80:
        action = "Investigar más antes de actuar"
    elif 0.20 <= D < 0.50:
        action = "Cuestionar o corregir"
    else:
        action = "Descartar / Denunciar como falso"

    return {
        "claim": claim,
        "fundamento": F,
        "contexto": C,
        "principio": P,
        "score": round(D, 3),
        "action": action
    }
