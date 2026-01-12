# agents/corporate_filter.py
from typing import Dict, List
from tri_axial_v2 import Criterion, compute_discernment_v2

class CorporateDiscernmentAgent:
    def __init__(self, llm: LLMInterface, templates_per_profile: Dict[str, List[Dict]]):
        self.llm = llm
        self.templates_per_profile = templates_per_profile

    def auto_evaluate(self, profile: str, proposal_text: str):
        template = self.templates_per_profile[profile]
        axes = {"F": [], "C": [], "P": []}

        for item in template:
            axis = item["axis"]
            dimension = item["dimension"]
            question = item["question"]

            result = self.llm.score_criterion(proposal_text, question)
            crit = Criterion(
                axis=axis,
                dimension=dimension,
                question=question,
                score=result["score"],
                reasoning=result["reasoning"],
            )
            axes[axis].append(crit)

        discernment = compute_discernment_v2(axes["F"], axes["C"], axes["P"])
        return discernment
