"""Contrato del bloque de evaluación: la clase padre `Metric`.

REGLA DEL CONTRATO
    entrada : (pred: Mask bool (H, W), gt: Mask bool (H, W))  -- misma forma
    salida  : float  (un único número por imagen)

Puntos clave:
    - `compute` se evalúa imagen a imagen; `aggregate` decide cómo se resume el
      conjunto (media por defecto; algunas métricas requieren acumular
      confusiones y calcular el valor global, p. ej. IoU "dataset-level").
    - `higher_is_better` permite que el reporting ordene y resalte las tablas
      automáticamente, sin casos especiales por métrica.
    - Casos degenerados (predicción y GT vacías): se devuelve `empty_value`
      explícitamente, en lugar de NaN silencioso. La convención del proyecto es
      1.0 cuando ambas están vacías (acierto perfecto) y 0.0 cuando solo una lo
      está. Esto debe aplicarse igual en TODAS las métricas.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Sequence

import numpy as np

from apple_seg.core.types import Mask, check_same_shape


class Metric(ABC):
    """CLASE PADRE del bloque de evaluación.

    Subclases: implementar `compute`; sobrescribir `aggregate` solo si la
    métrica no es promediable por imagen.
    """

    registry_name: str = "metric"
    higher_is_better: bool = True

    def __init__(self, **params: Any) -> None:
        self.params: dict[str, Any] = params

    @abstractmethod
    def compute(self, pred: Mask, gt: Mask) -> float:
        """Valor de la métrica para un par (predicción, referencia)."""

    def __call__(self, pred: Mask, gt: Mask) -> float:
        check_same_shape(pred, gt)
        return self.compute(pred, gt)

    def aggregate(self, values: Sequence[float]) -> float:
        """Resumen del conjunto. Por defecto, media aritmética."""
        return float(np.mean(values)) if len(values) else float("nan")

    def get_params(self) -> dict[str, Any]:
        return dict(self.params)

    @property
    def id(self) -> str:
        return self.registry_name

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.id}>"


def confusion(pred: Mask, gt: Mask) -> tuple[int, int, int, int]:
    """Cuenta (TP, FP, FN, TN) de un par de máscaras booleanas.

    Función compartida por las métricas de píxel; se implementa una sola vez
    para que todas cuenten exactamente lo mismo.
    """
    check_same_shape(pred, gt)
    tp = int(np.count_nonzero(pred & gt))
    fp = int(np.count_nonzero(pred & ~gt))
    fn = int(np.count_nonzero(~pred & gt))
    tn = int(pred.size - tp - fp - fn)
    return tp, fp, fn, tn
