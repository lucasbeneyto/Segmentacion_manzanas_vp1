# Registro de decisiones de diseño

Bitácora corta de las decisiones no evidentes y su porqué. Sirve para redactar la
memoria sin tener que reconstruir a posteriori por qué se hizo cada cosa.

Formato: una entrada por decisión.

---

### AAAA-MM-DD — Título de la decisión

- **Contexto:** qué problema se observó (con evidencia: imagen, métrica, run).
- **Alternativas consideradas:**
- **Decisión:**
- **Consecuencia medida:** cómo cambió la métrica principal, en qué run.

---

### 2026-11-17 — Arquitectura en tres bloques intercambiables

- **Contexto:** el proyecto requiere comparar varias técnicas de preprocesado y
  segmentación; hacerlo con scripts independientes impide comparar de forma justa.
- **Decisión:** tres bloques con clase padre y registro por nombre, combinables desde
  un YAML, con una tabla larga de métricas como único formato de resultados.
- **Consecuencia esperada:** cualquier método nuevo entra en todas las comparativas sin
  tocar código ajeno; todo número de la memoria es reproducible desde un `config.yaml`.
