# agents/interactive_agent.py
from dataclasses import dataclass
from typing import List, Dict
import json

from openai import OpenAI  # pip install openai

from tri_axial_v2 import Criterion, compute_discernment_v2


@dataclass
class LLMInterface:
    """
    Wrapper concreto para usar un modelo de OpenAI (ChatGPT)
    para puntuar cada criterio del método tri-axial.
    """
    model: str = "gpt-4o-mini"   # cámbialo al modelo que prefieras
    temperature: float = 0.0     # 0.0 = más determinista

    def __post_init__(self) -> None:
        # Usa la API key de la variable de entorno OPENAI_API_KEY
        # Ver: https://platform.openai.com/docs/libraries
        self.client = OpenAI()

    def score_criterion(self, project_desc: str, question: str) -> Dict:
        """
        Dado un proyecto y una pregunta de la tabla de discernimiento,
        pide al modelo que devuelva:
          - score: número entre 0.0 y 1.0
          - reasoning: explicación breve en español
        """
        system_prompt = (
            "Eres un evaluador cuantitativo para un sistema de discernimiento "
            "ético basado en tres ejes: Fundamento, Contexto y Principio.\n"
            "Tu tarea es leer la descripción de un proyecto y una pregunta "
            "de evaluación, y devolver SOLO un objeto JSON con esta forma:\n"
            '{ "score": <número entre 0 y 1>, "reasoning": "<explicación breve>" }.\n'
            "El campo 'score' debe ser un número real entre 0.0 y 1.0 "
            "con máximo dos decimales. La 'reasoning' debe estar en español, "
            "máximo 50 palabras."
        )

        user_prompt = (
            "Descripción del proyecto a evaluar:\n"
            "-----------------------------------\n"
            f"{project_desc}\n\n"
            "Criterio específico a puntuar:\n"
            "------------------------------\n"
            f"{question}\n\n"
            "Responde EXCLUSIVAMENTE con un JSON válido, sin texto adicional."
        )

        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            response_format={"type": "json_object"},  # modo JSON
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        content = completion.choices[0].message.content
        data = json.loads(content)

        # Normalizamos y acotamos el score por seguridad
        raw_score = float(data.get("score", 0.0))
        score = max(0.0, min(1.0, raw_score))

        reasoning = str(data.get("reasoning", "")).strip()
        if not reasoning:
            reasoning = "Sin justificación generada por el modelo."

        return {
            "score": score,
            "reasoning": reasoning,
        }


class InteractiveDiscernmentAgent:
    def __init__(self, llm: LLMInterface, template: List[Dict]):
        self.llm = llm
        self.template = template  # lista del JSON

    def run_session(self, project_desc: str):
        axes = {"F": [], "C": [], "P": []}

        for item in self.template:
            axis = item["axis"]
            dimension = item["dimension"]
            question = item["question"]

            # 1) LLM propone un puntaje inicial
            proposal = self.llm.score_criterion(project_desc, question)
            suggested = proposal["score"]
            reasoning = proposal["reasoning"]

            print(f"\n[{axis} - {dimension}] {question}")
            print(f"IA sugiere: {suggested:.2f} ({reasoning})")
            raw = input(
                "¿Aceptas este valor? [Enter = sí / número 0–1 para cambiar]: "
            ).strip()
            if raw:
                suggested = float(raw.replace(",", "."))

            crit = Criterion(
                axis=axis,
                dimension=dimension,
                question=question,
                score=suggested,
                reasoning=reasoning,
            )
            axes[axis].append(crit)

        result = compute_discernment_v2(axes["F"], axes["C"], axes["P"])
        return result
