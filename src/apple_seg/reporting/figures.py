"""Figuras para la memoria y la defensa.

Figuras previstas:
    - qualitative_panel : para una imagen, una fila por combinación con
                          [original | preprocesada | máscara predicha |
                           superposición | mapa de errores TP/FP/FN].
                          Es la figura que mejor explica por qué un método
                          falla y la más útil en la presentación.
    - comparison_grid   : misma imagen, todas las combinaciones en rejilla.
    - metric_barplot    : barras con la métrica principal por combinación,
                          con barras de error.
    - metric_boxplot    : dispersión por imagen, para ver si un método es bueno
                          de media o solo en casos fáciles.
    - failure_cases     : las N imágenes con peor IoU de la mejor combinación.

Convención de color del mapa de errores (coherente en todo el proyecto):
    verde = TP (acierto), rojo = FP (falsa alarma), azul = FN (fruto perdido).
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import pandas as pd

from apple_seg.core.types import Prediction, Sample


def overlay_mask(sample: Sample, mask, alpha: float = 0.45):
    """Superpone una máscara sobre la imagen original (devuelve imagen BGR)."""
    raise NotImplementedError


def error_map(pred, gt):
    """Imagen BGR con TP en verde, FP en rojo y FN en azul."""
    raise NotImplementedError


def save_qualitative_panel(
    sample: Sample, predictions: Sequence[Prediction], path: str | Path
) -> Path:
    """Panel cualitativo de una imagen con todas las combinaciones."""
    raise NotImplementedError


def save_comparison_grid(samples: Sequence[Sample], predictions, path: str | Path) -> Path:
    """Rejilla de comparación de varias imágenes y combinaciones."""
    raise NotImplementedError


def save_metric_barplot(raw: pd.DataFrame, metric: str, path: str | Path) -> Path:
    """Gráfico de barras de una métrica por combinación."""
    raise NotImplementedError


def save_metric_boxplot(raw: pd.DataFrame, metric: str, path: str | Path) -> Path:
    """Diagrama de caja de la distribución por imagen de una métrica."""
    raise NotImplementedError


def save_failure_cases(raw: pd.DataFrame, combo_id: str, n: int, path: str | Path) -> Path:
    """Figura con los peores casos de una combinación."""
    raise NotImplementedError
