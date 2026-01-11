from tri_axial_v2 import Criterion, compute_discernment_v2

def main():
    # Ejemplo de proyecto con fundamento débil: depende de crédito no aprobado
    f_criteria = [
        Criterion(
            axis="F",
            dimension="Existencia",
            question="¿Los recursos necesarios existen hoy de forma tangible y verificable?",
            score=0.2,
            reasoning="La mitad del presupuesto depende de un crédito aún no aprobado."
        ),
        Criterion(
            axis="F",
            dimension="Capacidad",
            question="¿Tenemos la competencia probada para transformar el recurso sin destruirlo?",
            score=0.6,
            reasoning="Tenemos experiencia parcial, pero no en el volumen requerido."
        ),
    ]

    c_criteria = [
        Criterion(
            axis="C",
            dimension="Sostenibilidad",
            question="¿El sistema puede mantener este proceso indefinidamente sin colapsar?",
            score=0.5,
            reasoning="El flujo de caja es ajustado; cualquier retraso podría generar tensión."
        ),
        Criterion(
            axis="C",
            dimension="Orden",
            question="¿La estructura propuesta reduce la complejidad y el ruido?",
            score=0.7,
            reasoning="Los roles están definidos, pero aún hay ambigüedad en la toma de decisiones."
        ),
    ]

    p_criteria = [
        Criterion(
            axis="P",
            dimension="Vitalidad",
            question="¿El resultado final aporta más energía/valor al sistema de la que costó producirlo?",
            score=0.8,
            reasoning="Si funciona, el proyecto generaría ingresos recurrentes importantes."
        ),
        Criterion(
            axis="P",
            dimension="Integridad",
            question="¿La ejecución preserva la salud física y mental de los agentes involucrados?",
            score=0.6,
            reasoning="Se anticipan picos de trabajo intensos, pero no permanentes."
        ),
    ]

    result = compute_discernment_v2(f_criteria, c_criteria, p_criteria)

    print("=== RESULTADO V2 MATERIAL ===")
    print(f"Fundamento (F): {result.foundation_score:.2f}")
    print(f"Contexto  (C): {result.context_score:.2f}")
    print(f"Principio (P): {result.principle_score:.2f}")
    print(f"Score final  : {result.final_score:.2f}")
    print(f"Acción sugerida : {result.action}")
    print(f"¿Fundamento real? {result.is_grounded}")
    if result.entropy_alerts:
        print("Alertas de entropía:")
        for alert in result.entropy_alerts:
            print(f"  - {alert}")

if __name__ == "__main__":
    main()

