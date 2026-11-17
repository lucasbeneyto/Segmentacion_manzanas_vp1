# Guion de la memoria descriptiva

Documento de trabajo: estructura propuesta para la memoria que se entrega el
**9 de diciembre de 2026**, junto con el código.

## Estructura propuesta

1. **Introducción y objetivo** — el problema de la recolección automatizada; qué debe
   hacer el sistema; restricción de usar solo técnicas clásicas vistas en la asignatura.
2. **Análisis del conjunto de datos** — nº de imágenes, resolución, condiciones de
   iluminación, oclusión por follaje, manzanas por imagen, % de píxeles de fruto.
   Histogramas de color fruto vs. fondo en HSV y Lab (salida de `scripts/explore_dataset.py`).
   Justifica las decisiones de diseño posteriores.
3. **Metodología**
   - Arquitectura del sistema (los tres bloques y el pipeline; figura del README).
   - Preprocesado: qué problema de la imagen ataca cada técnica.
   - Segmentación: fundamento de cada método y por qué se considera.
   - Refinado morfológico y filtrado por forma.
4. **Protocolo experimental** — partición dev/test, qué se ajusta y dónde, métricas
   elegidas y por qué (y por qué `accuracy` no sirve como criterio aquí).
5. **Resultados** — tabla principal (combinación × métrica), ablación del preprocesado,
   figuras cualitativas, tiempos de cómputo.
6. **Discusión** — análisis de casos de fallo: oclusión, brillos especulares, manzanas
   en racimo, fruto verde, retroiluminación. Qué método gana y en qué condiciones.
7. **Conclusiones y trabajo futuro.**
8. **Declaración de uso de herramientas de IA** (obligatoria, formato literal abajo).
9. **Referencias.**

---

## Declaración de uso de herramientas de IA

> Formato exigido por el enunciado. Rellenar con el uso real que se le haya dado.

**Herramientas utilizadas:**

**Finalidad del uso:**

**Indicaciones o instrucciones proporcionadas:**

**Uso del contenido generado:**

**Revisión y edición:**

**Limitaciones y consideraciones éticas:**

---

## Defensa (15 de diciembre de 2026, 10 minutos)

Guion sugerido: problema (1') · datos y dificultades reales (2') · arquitectura y
métodos (3') · resultados comparativos (2') · casos de fallo y conclusiones (2').
Apoyarse en los paneles cualitativos del mapa de errores: comunican mejor que las tablas.
