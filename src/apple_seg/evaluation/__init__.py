"""BLOQUE 3 — Evaluación.

Compara la máscara predicha con la máscara de referencia y produce números
comparables entre combinaciones (preprocesador x segmentador).

Clase padre del bloque: `Metric`.
Orquestador: `Evaluator`, que recorre predicciones y métricas y devuelve la
tabla larga de resultados.

Los módulos con las métricas reales los añade el equipo; cada una se registra
sola con el decorador @METRICS.register y su módulo debe importarse aquí abajo
para que el registro la conozca. `EJEMPLO_metrica.py` es la plantilla a copiar;
no forma parte del sistema final.
"""

from apple_seg.evaluation.base import Metric, confusion
from apple_seg.evaluation.evaluator import Evaluator

# Los imports siguientes existen por su efecto colateral: registrar componentes.
# Añade aquí una línea por cada módulo nuevo de métricas.
from apple_seg.evaluation import EJEMPLO_metrica  # noqa: F401

__all__ = ["Metric", "Evaluator", "confusion"]
