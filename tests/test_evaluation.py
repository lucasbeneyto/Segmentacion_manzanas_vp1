"""Pruebas de las métricas con casos conocidos.

Casos obligatorios: coincidencia perfecta -> 1.0; predicción vacía con GT no
vacía -> 0.0; ambas vacías -> valor convenido (1.0); métricas simétricas donde
corresponda; comportamiento de las métricas de objeto ante fusiones y
divisiones de componentes.
"""

from __future__ import annotations


def test_iou_perfect_match():
    raise NotImplementedError


def test_metrics_on_empty_masks():
    raise NotImplementedError
