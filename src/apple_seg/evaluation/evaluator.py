"""Orquestador del bloque de evaluación: `Evaluator`.

Recibe predicciones y métricas y produce la TABLA LARGA de resultados, que es
el formato canónico de salida del proyecto:

    sample_id | preprocessor_id | segmenter_id | metric | value | runtime_s

Todo lo demás (tablas resumen, ranking, gráficos) se deriva de esa tabla en el
bloque de reporting. Mantener un único formato intermedio evita que cada
persona del equipo invente el suyo.
"""

from __future__ import annotations

from typing import Iterable, Sequence

import pandas as pd

from apple_seg.core.types import Prediction, Sample
from apple_seg.evaluation.base import Metric


class Evaluator:
    """Calcula todas las métricas sobre todas las predicciones.

    Args:
        metrics: Métricas a aplicar (cualquier subclase de Metric).
        skip_empty_gt: Si True, excluye del promedio las imágenes sin manzanas.
    """

    def __init__(self, metrics: Sequence[Metric], skip_empty_gt: bool = False) -> None:
        self.metrics = list(metrics)
        self.skip_empty_gt = skip_empty_gt

    def evaluate_one(self, prediction: Prediction, sample: Sample) -> list[dict]:
        """Evalúa una predicción y devuelve una fila por métrica."""
        raise NotImplementedError

    def evaluate(
        self, predictions: Iterable[Prediction], samples: dict[str, Sample]
    ) -> pd.DataFrame:
        """Tabla larga con una fila por (muestra, combinación, métrica)."""
        raise NotImplementedError

    def summarize(self, raw: pd.DataFrame) -> pd.DataFrame:
        """Agrega la tabla larga por combinación usando `Metric.aggregate`.

        Devuelve media y desviación típica por (preprocesador, segmentador,
        métrica), que es la tabla que va a la memoria.
        """
        raise NotImplementedError
