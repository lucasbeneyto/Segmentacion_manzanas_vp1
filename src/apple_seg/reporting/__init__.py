"""Generación de entregables: tablas y figuras para la memoria y la defensa.

Consume únicamente la tabla larga de métricas y las predicciones; no vuelve a
calcular nada. Así, cualquier figura de la memoria se puede regenerar desde el
CSV de un run sin repetir el cómputo.
"""

from apple_seg.reporting.figures import save_comparison_grid, save_qualitative_panel
from apple_seg.reporting.tables import make_leaderboard, make_summary_table

__all__ = [
    "make_summary_table",
    "make_leaderboard",
    "save_qualitative_panel",
    "save_comparison_grid",
]
