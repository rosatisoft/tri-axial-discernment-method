# agents/interactive_agent.py
from dataclasses import dataclass
from typing import List, Dict
from tri_axial_v2 import Criterion, compute_discernment_v2

@dataclass
class LLMInterface:
    """Wrapper genérico para el modelo que uses (OpenAI, etc.)."""
    def score_criterion(self, project_desc: str, question: str) -> Dict:
        # Aquí haces la llamada real al LLM.
        # Debe devolverte algo como:
        # {"score": 0.7, "reasoning": "Porque..."}
        raise NotImplementedError

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
            raw = input("¿Aceptas este valor? [Enter = sí / número 0–1 para cambiar]: ").strip()
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
