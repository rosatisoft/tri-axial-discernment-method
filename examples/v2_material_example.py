from tri_axial_v2 import Criterion, compute_discernment_v2

def main():
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

    c_criteria = [...]  # similar
    p_criteria = [...]  # similar

    result = compute_discernment_v2(f_criteria, c_criteria, p_criteria)
    print(result)

if __name__ == "__main__":
    main()
