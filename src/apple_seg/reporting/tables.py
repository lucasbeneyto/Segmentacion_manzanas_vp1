"""Tablas de resultados para la memoria.

Transforma la tabla larga en las tablas que se incluyen en el documento:

    - summary_table : filas = combinación (preproc + segmentador),
                      columnas = métricas, celdas = media ± desviación típica.
    - leaderboard   : ranking por la métrica principal (`output.main_metric` del
                      YAML), con el baseline siempre visible para cuantificar la mejora.
    - per_image     : métricas por imagen de una combinación concreta, para
                      localizar y comentar los casos de fallo en la memoria.
    - ablation      : efecto de cada preprocesador manteniendo fijo el
                      segmentador (y viceversa), que es el análisis que
                      justifica las decisiones de diseño.

Exporta a CSV y a Markdown/LaTeX para pegar directamente en el documento.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def make_summary_table(raw: pd.DataFrame, decimals: int = 3) -> pd.DataFrame:
    """Tabla combinación x métrica con media y desviación típica."""
    raise NotImplementedError


def make_leaderboard(raw: pd.DataFrame, main_metric: str, top_k: int | None = None) -> pd.DataFrame:
    """Ranking de combinaciones por la métrica principal."""
    raise NotImplementedError


def make_per_image_table(raw: pd.DataFrame, combo_id: str) -> pd.DataFrame:
    """Métricas imagen a imagen de una combinación, ordenadas de peor a mejor."""
    raise NotImplementedError


def make_ablation_table(raw: pd.DataFrame, main_metric: str, fixed: str = "segmenter_id") -> pd.DataFrame:
    """Efecto marginal de cada preprocesador (o segmentador) sobre la métrica."""
    raise NotImplementedError


def export_table(df: pd.DataFrame, path: str | Path, formats: tuple[str, ...] = ("csv", "md")) -> list[Path]:
    """Exporta una tabla a los formatos indicados (csv, md, tex)."""
    raise NotImplementedError
