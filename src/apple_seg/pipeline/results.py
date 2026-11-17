"""Almacenamiento y recuperación de resultados: `ResultStore`.

Persiste la tabla larga de métricas y permite volver a cargar runs anteriores
para compararlos entre sí (p. ej. la tabla final de la memoria, que compara el
baseline con la mejor configuración encontrada).

Formatos:
    - metrics_raw.csv     : tabla larga, una fila por (muestra, combo, métrica).
    - metrics_summary.csv : tabla agregada por combinación.
    - run_meta.json       : versión, fecha, semilla, nº de imágenes, tiempos.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


class ResultStore:
    """Lectura/escritura de los resultados de un run."""

    def __init__(self, run_dir: str | Path) -> None:
        self.run_dir = Path(run_dir)

    def save_raw(self, df: pd.DataFrame) -> Path:
        """Guarda la tabla larga de métricas."""
        raise NotImplementedError

    def save_summary(self, df: pd.DataFrame) -> Path:
        """Guarda la tabla agregada por combinación."""
        raise NotImplementedError

    def load_raw(self) -> pd.DataFrame:
        """Carga la tabla larga de un run previo."""
        raise NotImplementedError

    @staticmethod
    def compare_runs(run_dirs: list[str | Path]) -> pd.DataFrame:
        """Une los resúmenes de varios runs en una sola tabla comparativa."""
        raise NotImplementedError
