# -----------------------------------------------------------------------------
#  Tri-Axial Discernment Engine
#  v0.1.0 (Calculadora Neutral) o v2.0 (Camino del Criterio)
#
#  Copyright (c) 2025 Ernesto Rosati Beristain
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -----------------------------------------------------------------------------
# src/tri_axial_v2.py
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Criterion:
    """
    Unidad atómica de discernimiento.
    Permite justificar cada puntaje (humano o IA).
    """
    axis: str          # 'F', 'C', 'P'
    dimension: str     # 'Existencia', 'Capacidad', etc.
    question: str      # La pregunta concreta
    score: float       # 0.0 (entropía total) a 1.0 (verdad plena)
    reasoning: str     # Justificación de la "Verdad Consciente"

@dataclass
class DiscernmentResultV2:
    foundation_score: float
    context_score: float
    principle_score: float
    final_score: float
    action: str
    is_grounded: bool        # ¿Pasó el filtro de realidad?
    entropy_alerts: List[str] = field(default_factory=list)
    raw_axes: Dict[str, List[Criterion]] = field(default_factory=dict)

# Config por defecto (se puede mover a un JSON o .env)
V2_THRESHOLDS = {
    "FOUNDATION_MIN": 0.4,   # bajo esto se considera fundamento ilusorio
    "MAX_IF_UNGROUNDED": 0.3,
    "ADOPT": 0.8,
    "CONSIDER": 0.5,
}

def compute_discernment_v2(
    f_criteria: List[Criterion],
    c_criteria: List[Criterion],
    p_criteria: List[Criterion],
    thresholds: Dict[str, float] = V2_THRESHOLDS,
) -> DiscernmentResultV2:
    
    # 1. Calcular promedios por eje
    f_avg = sum(c.score for c in f_criteria) / len(f_criteria)
    c_avg = sum(c.score for c in c_criteria) / len(c_criteria)
    p_avg = sum(c.score for c in p_criteria) / len(p_criteria)

    entropy_alerts: List[str] = []
    is_grounded = True

    # 2. Cálculo base (promedio)
    base_score = (f_avg + c_avg + p_avg) / 3.0

    # 3. VETO DE ENTROPÍA (Fundamento)
    if f_avg < thresholds["FOUNDATION_MIN"]:
        is_grounded = False
        entropy_alerts.append(
            "ALERTA CRÍTICA: El fundamento es ilusorio o demasiado débil."
        )
        final_score = min(base_score, thresholds["MAX_IF_UNGROUNDED"])
        action = "DESCARTAR: Alto riesgo de entropía y colapso."
    else:
        final_score = base_score
        if final_score >= thresholds["ADOPT"]:
            action = "PROCEDER: Alta coherencia y orden."
        elif final_score >= thresholds["CONSIDER"]:
            action = "REVISAR: Válido pero requiere ajustes."
        else:
            action = "CUESTIONAR: La estructura es débil."

    return DiscernmentResultV2(
        foundation_score=f_avg,
        context_score=c_avg,
        principle_score=p_avg,
        final_score=final_score,
        action=action,
        is_grounded=is_grounded,
        entropy_alerts=entropy_alerts,
        raw_axes={
            "F": f_criteria,
            "C": c_criteria,
            "P": p_criteria,
        },
    )
