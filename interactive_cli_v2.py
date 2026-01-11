#!/usr/bin/env python
# -----------------------------------------------------------------------------
#  Tri-Axial Discernment Engine - CLI interactivo V2.0 (Camino del Criterio)
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

import json
import sys
from pathlib import Path
from typing import List, Dict

# Aseguramos que se pueda importar src/tri_axial_v2.py
ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
TEMPLATES_DIR = ROOT_DIR / "templates"
TEMPLATE_FILE = TEMPLATES_DIR / "v2_material_discernment.json"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from tri_axial_v2 import Criterion, compute_discernment_v2  # type: ignore


def load_material_template(path: Path) -> List[Dict[str, str]]:
    """Carga la tabla material V2 desde JSON."""
    if not path.exists():
        raise FileNotFoundError(f"No se encontró la plantilla: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("La plantilla JSON debe ser una lista de criterios.")
    return data


def ask_score(question: str) -> float:
    """
    Pide al usuario un valor entre 0.0 y 1.0.
    Permite usar punto o coma decimal.
    """
    while True:
        raw = input(f"  Puntaje [0.0 – 1.0] para:\n  » {question}\n  > ").strip()
        # Soportar coma como decimal
        raw = raw.replace(",", ".")
        try:
            value = float(raw)
        except ValueError:
            print("  ⚠ Entrada no válida. Escribe un número entre 0.0 y 1.0.\n")
            continue
        if 0.0 <= value <= 1.0:
            return value
        print("  ⚠ El valor debe estar entre 0.0 y 1.0.\n")


def ask_reasoning() -> str:
    """Pide una justificación breve del puntaje."""
    text = input("  Justificación breve (puedes dejarlo vacío):\n  > ").strip()
    if not text:
        return "Sin justificación explícita."
    return text


def collect_criteria_from_template(template: List[Dict[str, str]]) -> Dict[str, List[Criterion]]:
    """
    Construye listas de Criterion agrupadas por eje (F, C, P)
    a partir de la plantilla JSON.
    """
    axes: Dict[str, List[Criterion]] = {"F": [], "C": [], "P": []}

    print("\n=== Evaluación V2.0 - Fundamento Material y Entropía ===\n")
    print("Responde cada criterio con un valor entre 0.0 y 1.0.")
    print("Sugerencia general:")
    print("  0.0  = Entropía total / falsedad")
    print("  0.5  = Dudoso / mezclado")
    print("  1.0  = Verdad plena / totalmente alineado\n")

    for item in template:
        axis = item.get("axis")
        dimension = item.get("dimension", "")
        question = item.get("question", "")
        entropy_alert = item.get("entropy_alert", "")

        if axis not in axes:
            print(f"⚠ Se encontró un eje desconocido en la plantilla: {axis!r}. Se ignora.")
            continue

        print("------------------------------------------------------------")
        print(f"Eje: {axis}    Dimensión: {dimension}")
        print(f"Pregunta: {question}")
        if entropy_alert:
            print(f"Posible señal de entropía si el valor es bajo:\n  - {entropy_alert}")
        print()

        score = ask_score(question)
        reasoning = ask_reasoning()

        crit = Criterion(
            axis=axis,
            dimension=dimension,
            question=question,
            score=score,
            reasoning=reasoning,
        )
        axes[axis].append(crit)
        print()

    return axes


def print_result(result) -> None:
    """Imprime el resultado de discernimiento de forma legible."""
    print("\n============================================================")
    print("                 RESULTADO DE DISCERNIMIENTO V2             ")
    print("============================================================\n")

    print(f"Fundamento (F) : {result.foundation_score:.2f}")
    print(f"Contexto  (C)  : {result.context_score:.2f}")
    print(f"Principio (P)  : {result.principle_score:.2f}")
    print("-" * 60)
    print(f"Score final    : {result.final_score:.2f}")
    print(f"Acción sugerida: {result.action}")
    print(f"Fundamento real (is_grounded): {result.is_grounded}")
    print("-" * 60)

    if result.entropy_alerts:
        print("⚠ Alertas de entropía:")
        for alert in result.entropy_alerts:
            print(f"  - {alert}")
        print("-" * 60)

    # Opcional: mostrar resumen por eje
    print("\nDetalle por criterio:\n")
    for axis_label, criteria in result.raw_axes.items():
        print(f"[Eje {axis_label}]")
        for c in criteria:
            print(f"  - ({c.dimension}) {c.question}")
            print(f"    Puntaje: {c.score:.2f}")
            print(f"    Motivo : {c.reasoning}")
        print()


def main() -> None:
    try:
        template = load_material_template(TEMPLATE_FILE)
    except Exception as e:
        print(f"Error al cargar la plantilla material: {e}")
        sys.exit(1)

    axes = collect_criteria_from_template(template)

    f_criteria = axes.get("F", [])
    c_criteria = axes.get("C", [])
    p_criteria = axes.get("P", [])

    if not f_criteria or not c_criteria or not p_criteria:
        print("⚠ Faltan criterios en alguno de los ejes (F, C o P). Revisa la plantilla.")
        sys.exit(1)

    result = compute_discernment_v2(f_criteria, c_criteria, p_criteria)
    print_result(result)


if __name__ == "__main__":
    main()
