"""Orquestación: une los tres bloques en un experimento reproducible.

El pipeline es el objetivo final del proyecto: dada una configuración con
M preprocesadores, N segmentadores y K métricas, ejecuta el producto cartesiano
M x N sobre todo el dataset, calcula las K métricas y escribe tablas y figuras.

Ningún módulo de los bloques debe importar nada de `pipeline`: la dependencia va
siempre en un único sentido (pipeline -> bloques).
"""

from apple_seg.pipeline.runner import ExperimentRunner
from apple_seg.pipeline.grid import CombinationGrid

__all__ = ["ExperimentRunner", "CombinationGrid"]
