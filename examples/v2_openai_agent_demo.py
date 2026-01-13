from pathlib import Path
from dataclasses import dataclass
from typing import Tuple
import json

from openai import OpenAI
from tri_axial_v2 import Criterion, compute_discernment_v2

TEMPLATE_FILE = Path("templates") / "v2_material_discernment.json"


@dataclass
class OpenAILLM:
    """
    Pequeño wrapper para pedirle a gpt-4o-mini que puntúe un criterio
    y devuelva score (0–1) + razonamiento.
    """
    model: str = "gpt-4o-mini"

    def __post_init__(self):
        self.client = OpenAI()

    def score(self, project_desc: str, axis: str, dimension: str, question: str) -> Tuple[float, str]:
        system_msg = (
            "Eres un evaluador de proyectos que usa una escala de 0.0 a 1.0.\n"
            "0.0 = entropía total / irreal / muy mala base.\n"
            "1.0 = completamente realista, sostenible y alineado.\n"
            "Debes responder SOLO un JSON con los campos:\n"
            '{ "score": <número 0-1>, "reasoning": "<explicación breve en español>" }'
        )

        user_msg = (
            f"Proyecto a evaluar:\n{project_desc}\n\n"
            f"Criterio ({axis}-{dimension}):\n{question}\n\n"
            "Calibra un número entre 0.0 y 1.0 según esta descripción."
        )

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            response_format={"type": "json_object"},
        )

        content = resp.choices[0].message.content
        data = json.loads(content)

        score = float(data["score"])
        # Aseguramos el rango [0, 1]
        score = max(0.0, min(1.0, score))
        reasoning = data.get("reasoning", "").strip()

        return score, reasoning


def main() -> None:
    # 1. Cargar la tabla material V2
    template = json.loads(TEMPLATE_FILE.read_text(encoding="utf-8"))

    # 2. Descripción del proyecto
    print("=== Agente de Discernimiento V2 (Material + Entropía) ===\n")
    project_desc = input("Describe brevemente el proyecto a evaluar:\n> ")

    llm = OpenAILLM()
    axes = {"F": [], "C": [], "P": []}

    # 3. Recorrer cada criterio de la tabla y pedir sugerencia al modelo
    for item in template:
        axis = item["axis"]
        dimension = item["dimension"]
        question = item["question"]

        print("\n------------------------------------------------------------")
        print(f"Eje: {axis}    Dimensión: {dimension}")
        print(f"Pregunta: {question}")

        score, reasoning = llm.score(project_desc, axis, dimension, question)
        print(f"Sugerencia del modelo: {score:.2f}")
        if reasoning:
            print(f"Motivo del modelo: {reasoning}")

        adjust_raw = input(
            "Si quieres ajustar el puntaje, escribe un valor 0.0–1.0 "
            "(o presiona Enter para aceptar el valor sugerido):\n> "
        ).strip()

        if adjust_raw:
            try:
                score = float(adjust_raw.replace(",", "."))
                score = max(0.0, min(1.0, score))
            except ValueError:
                print("Valor inválido, se mantiene la sugerencia de la IA.")

        crit = Criterion(
            axis=axis,
            dimension=dimension,
            question=question,
            score=score,
            reasoning=reasoning,
        )
        axes[axis].append(crit)

    # 4. Calcular el discernimiento con tu motor V2
    result = compute_discernment_v2(axes["F"], axes["C"], axes["P"])

    print("\n============================================================")
    print("                 RESULTADO DE DISCERNIMIENTO V2")
    print("============================================================\n")
    print(f"Fundamento (F) : {result.foundation_score:.2f}")
    print(f"Contexto  (C)  : {result.context_score:.2f}")
    print(f"Principio (P)  : {result.principle_score:.2f}")
    print("------------------------------------------------------------")
    print(f"Score final    : {result.final_score:.2f}")
    print(f"Acción sugerida: {result.action}")
    print(f"Fundamento real (is_grounded): {result.is_grounded}")
    if result.entropy_alerts:
        print("Alertas de entropía:")
        for alert in result.entropy_alerts:
            print(f"  - {alert}")


if __name__ == "__main__":
    main()
