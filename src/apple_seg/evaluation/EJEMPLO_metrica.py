"""EJEMPLO — plantilla de una métrica. NO forma parte del sistema final.

Este fichero existe solo para enseñar cómo se implementa y se registra una
`Metric`. La métrica que calcula (fracción de píxeles coincidentes) es
deliberadamente trivial y además poco útil en este problema, porque el fondo
domina la imagen: no es una propuesta de métrica para el proyecto.

Para crear una métrica real:
    1. Copia este fichero con el nombre de la familia
       (p. ej. `pixel_metrics.py`).
    2. Cambia el nombre de registro y el de la clase.
    3. Implementa `compute` respetando el contrato (ver README, sección 4.4),
       muy en particular la convención de máscaras vacías.
"""

from __future__ import annotations

from apple_seg.core.registry import METRICS
from apple_seg.core.types import Mask
from apple_seg.evaluation.base import Metric, confusion


@METRICS.register("ejemplo_coincidencia")
class EjemploMetrica(Metric):
    """EJEMPLO: fracción de píxeles en los que predicción y referencia coinciden.

    Ilustra los puntos del contrato que suelen fallar:
        - devuelve UN float por imagen (el promedio del conjunto lo hace solo
          la clase padre, en `aggregate`);
        - declara `higher_is_better` para que el reporting ordene las tablas
          sin casos especiales;
        - cuenta TP/FP/FN/TN con `confusion`, la función compartida, para que
          todas las métricas cuenten exactamente lo mismo;
        - resuelve explícitamente el caso degenerado de las máscaras vacías
          (ambas vacías -> 1.0; solo una vacía -> 0.0).
    """

    higher_is_better = True

    def compute(self, pred: Mask, gt: Mask) -> float:
        if not pred.any() and not gt.any():
            return 1.0
        if not pred.any() or not gt.any():
            return 0.0
        tp, fp, fn, tn = confusion(pred, gt)
        total = tp + fp + fn + tn
        return (tp + tn) / total if total else 0.0


@METRICS.register("ejemplo_error")
class EjemploMetricaDeError(Metric):
    """EJEMPLO: plantilla de una métrica donde MENOR es mejor.

    Basta con poner `higher_is_better = False`: el reporting ordena los rankings
    y resalta el mejor valor a partir de ese atributo, sin más cambios.
    """

    higher_is_better = False

    def compute(self, pred: Mask, gt: Mask) -> float:
        tp, fp, fn, tn = confusion(pred, gt)
        return float(fp + fn) / max(pred.size, 1)
