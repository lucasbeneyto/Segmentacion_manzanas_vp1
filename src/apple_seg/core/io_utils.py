"""Utilidades de entrada/salida: creación de carpetas de run, guardado de máscaras,
figuras y volcado de la configuración usada.

Centraliza la estructura de `results/` para que todos los experimentos sean
comparables y reproducibles:

    results/runs/<run_name>/
        config.yaml        copia exacta de la configuración ejecutada
        metrics_raw.csv    una fila por (muestra, preproc, segmentador, métrica)
        metrics_summary.csv  tabla agregada por combinación
        masks/<combo>/<sample_id>.png
        figures/...
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np


def make_run_dir(results_dir: str | Path, run_name: str, timestamp: bool = True) -> Path:
    """Crea (y devuelve) la carpeta del run, opcionalmente con marca temporal."""
    raise NotImplementedError


def save_mask(mask: np.ndarray, path: str | Path) -> None:
    """Guarda una máscara booleana como PNG binario {0,255}."""
    raise NotImplementedError


def save_config_copy(config: dict[str, Any], run_dir: str | Path) -> None:
    """Vuelca el YAML efectivo del experimento dentro de la carpeta del run."""
    raise NotImplementedError
