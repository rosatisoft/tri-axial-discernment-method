[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

# Tri-Axial Method of Discernment (F–C–P)

## **Badges y Enlace a Releases**

```md
[![Status](https://img.shields.io/badge/status-prealpha-orange)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)]()
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Zenodo DOI](https://img.shields.io/badge/Zenodo-18182173-blue)](https://doi.org/10.5281/zenodo.18182173)

The Tri-Axial Method can be understood at three layers:
(1) theory (paper), (2) method (questions), (3) engine (this repo).
---
## Who is this for?

The Tri-Axial Method of Discernment is designed for anyone who needs to make
clearer, more grounded, and less biased decisions.

It is especially useful for:

- **Researchers and analysts** evaluating claims and evidence  
- **Journalists and fact-checkers** validating information under uncertainty  
- **Educators and students** learning structured reasoning  
- **Data scientists and ML practitioners** assessing model decisions  
- **Policy makers and institutions** reducing bias and arbitrariness  
- **AI developers** who want transparent reasoning chains for LLMs  
- **General public** wishing to think better in an era of misinformation  

If you must **decide**, **interpret**, or **evaluate** —  
F–C–P gives you structure, without telling you what to think.

This repository contains the conceptual and operational resources for the **Tri-Axial Method of Discernment**, a framework for evaluating information, claims, and decisions using three simultaneous axes:

1. **Foundation (F)** — factual grounding / evidence
2. **Context (C)** — situational frame, motivations, and external forces
3. **Principle (P)** — systemic and ethical implications of action

The method is designed to be usable by both **human agents** and **AI systems**, and is described in detail in the working paper:

> **“Método Triaxial de Discernimiento”**  
> Author: Ernesto Rosati Beristáin  
> Published as a preprint on Zenodo.

> A small engine for **structured judgment** in noisy environments.  
> Foundation (F) · Context (C) · Principle (P)

Este repositorio implementa el **Método Triaxial de Discernimiento** como un motor simple en Python:

- Tú (humano) evalúas una afirmación o decisión en tres ejes:
  - **F** – Fundamento (¿qué tan real y verificable es?)
  - **C** – Contexto (¿en qué entorno y bajo qué fuerzas opera?)
  - **P** – Principio (¿qué consecuencias produce aceptar/actuar en esa dirección?)
- El motor integra esos valores y devuelve:
  - un puntaje de **discernimiento D ∈ [0,1]**
  - una **acción sugerida** (adoptar, complementar, cuestionar o descartar)

La idea central:  
> La IA y el humano no necesitan solo más datos, sino **mejor criterio**.

---

## 1. ¿Para qué sirve?

Para cualquier caso donde haya **información confusa** o **decisiones con ruido**:

- titulares virales, rumores, campañas mediáticas  
- decisiones legales o de política interna  
- elección de datasets, modelos o configuraciones en IA  
- análisis de testimonios, informes o narrativas  
- decisiones personales u organizacionales con impacto

El método NO te dice *qué* pensar, sino **cómo ordenar tu juicio**:

1. Separar **realidad** de apariencia (F).
2. Ver el **marco** y las fuerzas alrededor (C).
3. Medir **impacto y coherencia** de la acción (P).

---

## 2. Idea básica del modelo

El discernimiento se calcula así:

```text
Discernimiento D = (F + C + P) / 3
````

donde:

* **F, C, P** son valores entre **0 y 1**, obtenidos a partir de pequeñas preguntas:

  * F (Fundamento): fuente, evidencia, coherencia con el mundo real…
  * C (Contexto): presión emocional, agendas, marco temporal, actores…
  * P (Principio): entropía o claridad que genera, daño o construcción, coherencia ética…

La implementación es **axioma-agnóstica**:
no obliga a aceptar un sistema metafísico; simplemente asume que:

> Más coherencia y menos entropía narrativa
> normalmente llevan a mejores decisiones.

---

## 3. Cómo usar el motor (versión corta)

### Paso 1 — Formular la afirmación

Ejemplo:

> "Usar todo el dataset siempre maximiza la precisión sin costo extra."

Ese es el **X** que vas a evaluar.

---

### Paso 2 — Puntuar criterios F, C y P

Para cada eje respondes 4–5 preguntas (tabla del paper)
con valores entre **0 y 1**:

* 1.0 → muy sólido / claro / coherente
* 0.5 → dudoso / parcial
* 0.0 → falso / inconsistente

En código, se ve así:

```python
F_criteria = [0.6, 0.4, 0.5, 0.3, 0.4]
C_criteria = [0.7, 0.5, 0.8, 0.4, 0.6]
P_criteria = [0.3, 0.5, 0.6, 0.9, 0.4]
```

---

### Paso 3 — Llamar al motor F–C–P

```python
from tri_axial_discernment import compute_discernment_from_criteria

result = compute_discernment_from_criteria(
    foundation_criteria=F_criteria,
    context_criteria=C_criteria,
    principle_criteria=P_criteria,
    notes={"scenario": "IA training dataset optimization"},
)

print(result.foundation)  # F
print(result.context)     # C
print(result.principle)   # P
print(result.score)       # D
print(result.action)      # acción sugerida (texto)
```

El motor hace tres cosas:

1. **Promedia** los criterios F, C, P.
2. Calcula **D = (F + C + P) / 3**.
3. Devuelve una **acción recomendada**, según la escala:

```text
0.80–1.00 → Adoptar y, si es útil, compartir
0.50–0.79 → Considerar válido, pero complementar análisis
0.20–0.49 → Cuestionar, corregir, contrastar fuentes
0.00–0.19 → Descartar o denunciar si es dañino/falso
```

---

## 4. Ejecutar el ejemplo incluido

El repositorio incluye un ejemplo aplicado a IA:

```bash
python examples/ia_dataset_example.py
```

Ese script:

* define una afirmación concreta,
* establece criterios F, C, P,
* llama al motor,
* imprime el resultado de forma entendible.

Es el modelo mínimo de cómo usar el método en cualquier dominio.

"Install & Run" para recién llegados


## Installation (early preview v0.1)

Clone and run locally:

```bash
git clone https://github.com/rosatisoft/tri-axial-discernment-method.git
cd tri-axial-discernment-method
pip install -r requirements.txt   # upcoming v0.2


Run interactive CLI:

python src/interactive_cli.py


Run a sample:

python examples/ia_dataset_example.py


Open the notebooks:

jupyter lab


---

## 5. Estructura del repositorio

```text
.
├── README.md                        # Este archivo
├── src/
│   └── tri_axial_discernment.py     # Motor F–C–P (implementación principal)
├── examples/
│   └── ia_dataset_example.py        # Ejemplo práctico (IA / datasets)
└── docs/
    ├── ...                          # Textos completos ES/EN (paper)
    └── ...                          # Resumen/abstract, tablas, etc.
```

---

## 6. Qué hace el motor (y qué no)

✅ **Hace:**

* Ordena tu juicio en tres planos: realidad, contexto, consecuencia.
* Te obliga a **explicitar** tu criterio en números (0–1).
* Te permite **comparar casos** y ver por qué algo genera duda.
* Es integrable en:

  * asistentes IA,
  * flujos legales,
  * análisis mediático,
  * herramientas de apoyo a la decisión.

❌ **No hace:**

* No “adivina” la verdad absoluta.
* No reemplaza la evidencia, la investigación ni la responsabilidad.
* No elimina todos los sesgos del evaluador.
* No decide por ti: te muestra **dónde** estás decidiendo mal o por impulso.

---

## 7. Nota conceptual

El método nació dentro de un marco filosófico más amplio
(*El Axioma del Absoluto y la Restauración del Fundamento*).

Sin embargo, en esta implementación:

* el motor se mantiene **neutral** y **general**,
* puede operar con cualquier marco ético que busque:

  * coherencia,
  * claridad,
  * reducción de entropía (caos, confusión, manipulación).

Puedes usarlo como:

> Un “motor de criterio” acoplable a diferentes contextos
> humanos y algorítmicos.

---

## 8. Próximos pasos (sugeridos)

* Añadir más ejemplos:

  * análisis legal (testimonios contradictorios),
  * verificación de titulares virales,
  * decisiones de política interna.
    ya estan en examples
* Crear notebooks (`/notebooks`) con casos explicados paso a paso.
  ya estan en notebooks
* Exponerlo como API ligera o módulo dentro de agentes IA.
  ya estan en src

---

## 9. Plantillas listas para usar

En `templates/` encontrarás formatos listos para imprimir o copiar:

- `evaluation-matrix.md` — matriz general F–C–P para cualquier caso.
- `legal-analysis.md` — versión adaptada a expedientes, testimonios y evidencia.
- `media-analysis.md` — análisis de noticias virales, redes y narrativas mediáticas.

Estas plantillas permiten aplicar el método aunque no se programe nada.

---

### Short English summary

This repository provides a small, axioma-agnostic Python engine for the
**Tri-Axial Method of Discernment (F–C–P)**:

* **F**oundation — factual grounding
* **C**ontext — situational framing
* **P**rinciple — systemic and ethical impact of action

You score each axis with values in [0, 1], the engine computes:

```text
D = (F + C + P) / 3
```

and suggests an action (adopt, complement, question, discard).

It is designed to be:

* simple enough for humans,
* formal enough for code,
* and transparent enough for use in IA alignment and critical evaluation.

See `src/tri_axial_discernment.py` for the core implementation
and `examples/ia_dataset_example.py` for a concrete IA use case.

```
## Contents (roadmap)

- `/docs/` – Formal documents (PDF, manifests, diagrams)
- `/src/` – Code and pseudocode implementations of the F–C–P method
- `/examples/` – Practical use cases (legal analysis, media, AI optimization)
- `/notebooks/` – Jupyter notebooks (interactive demonstrations)

## Reference (Zenodo)

The full paper is available on Zenodo:

https://doi.org/10.5281/zenodo.18182173

## License

The repository contains two kinds of intellectual property:

### 📄 Intellectual Content (Paper, theory, essays)
All formal documents included in `/docs` or linked via DOI  
are licensed under:

**Creative Commons Attribution–NonCommercial–ShareAlike 4.0 (CC BY-NC-SA 4.0)**  
as published on Zenodo: https://doi.org/10.5281/zenodo.18182173

This license restricts **commercial reuse** without permission.

---

### 🧠 Software and Code
All Python source files in `/src`, `/examples` and related modules  
are distributed under:

**Apache License 2.0**  
(You may use, modify, distribute, and commercially deploy the code.)

See the `LICENSE` file for complete terms.


