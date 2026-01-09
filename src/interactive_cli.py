"""
interactive_cli.py

CLI interactivo para aplicar el Método Triaxial de Discernimiento (F–C–P)
usando el motor definido en tri_axial_discernment.py.

Flujo:
1. El usuario ingresa calificaciones de 0.0 a 1.0 para 15 criterios:
   - 5 para Fundamento (F)
   - 5 para Contexto (C)
   - 5 para Principio (P)
2. El script calcula los promedios por eje y el Discernimiento D.
3. Muestra la acción recomendada según el espectro de D.

Uso (desde la raíz del repositorio):
    python3 src/interactive_cli.py
"""

from typing import List
from tri_axial_discernment import compute_discernment_from_criteria, DiscernmentResult


def clamp(value: float, min_value: float = 0.0, max_value: float = 1.0) -> float:
    return max(min_value, min(max_value, value))


def pedir_valores_eje(nombre_eje: str, criterios: List[str]) -> List[float]:
    """
    Pregunta al usuario por cada criterio de un eje (F, C o P)
    y devuelve una lista de valores entre 0.0 y 1.0.
    """
    print(f"\n=== EJE {nombre_eje} ===")
    print("Ingresa un valor entre 0.0 y 1.0 para cada criterio.")
    print("Sugerencia: 1.0 = muy alto, 0.5 = dudoso, 0.0 = falso/inconsistente.\n")

    valores: List[float] = []

    for idx, criterio in enumerate(criterios, start=1):
        while True:
            try:
                raw = input(f"{idx}. {criterio}  → ")
                raw = raw.strip()

                # Si el usuario solo presiona Enter, asumimos 0.5 (neutral)
                if raw == "":
                    valor = 0.5
                else:
                    valor = float(raw)

                valor = clamp(valor)
                valores.append(valor)
                break
            except ValueError:
                print("⚠ Entrada no válida. Escribe un número entre 0.0 y 1.0 (ej. 0.8).")

    return valores


def imprimir_resultado(result: DiscernmentResult) -> None:
    """
    Muestra de forma legible los resultados del discernimiento.
    """
    print("\n====================================")
    print(" RESULTADO DEL MÉTODO TRIAXIAL (F–C–P)")
    print("====================================")
    print(f"Fundamento (F): {result.foundation:.2f}")
    print(f"Contexto   (C): {result.context:.2f}")
    print(f"Principio  (P): {result.principle:.2f}")
    print("------------------------------------")
    print(f"Discernimiento D: {result.score:.2f}")
    print(f"Acción sugerida : {result.action}")
    if result.notes:
        print("------------------------------------")
        print("Notas:")
        for k, v in result.notes.items():
            print(f"- {k}: {v}")
    print("====================================\n")


def main() -> None:
    print("\n====================================")
    print(" MÉTODO TRIAXIAL DE DISCERNIMIENTO")
    print(" Evaluación interactiva F–C–P")
    print("====================================")
    print("Este asistente te ayudará a evaluar una afirmación, caso o narrativa")
    print("usando los tres ejes: Fundamento, Contexto y Principio.\n")

    claim = input("Escribe brevemente la afirmación o caso a evaluar:\n> ").strip()

    # Criterios según la matriz general del método
    criterios_F = [
        "La fuente es confiable / verificable",
        "Es consistente con hechos conocidos",
        "Coincide con el funcionamiento real del mundo",
        "No requiere suposiciones forzadas",
        "No contradice evidencia sólida",
    ]

    criterios_C = [
        "Existe contexto claro y transparente",
        "No proviene de emoción, presión o manipulación",
        "No generaliza ni estigmatiza grupos completos",
        "Está aislada de agendas políticas o mediáticas interesadas",
        "Los datos/relato están situados en un marco realista",
    ]

    criterios_P = [
        "Produce menor entropía (menos caos/confusión)",
        "Fomenta coherencia interna y externa",
        "Respeta la dignidad humana e institucional",
        "No alimenta odio, división o violencia",
        "Abre caminos de acción responsable",
    ]

    F_vals = pedir_valores_eje("FUNDAMENTO (F)", criterios_F)
    C_vals = pedir_valores_eje("CONTEXTO (C)", criterios_C)
    P_vals = pedir_valores_eje("PRINCIPIO (P)", criterios_P)

    notes = {"claim": claim} if claim else None

    result: DiscernmentResult = compute_discernment_from_criteria(
        F_vals,
        C_vals,
        P_vals,
        notes=notes,
    )

    imprimir_resultado(result)


if __name__ == "__main__":
    main()
