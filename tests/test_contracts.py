"""Pruebas del CONTRATO: lo que debe cumplir cualquier componente nuevo.

Estas pruebas recorren automáticamente todo lo registrado en los registros y
verifican las reglas del README, de modo que si alguien añade un componente que
no respeta el contrato, la prueba falla sin que haya que escribir un test nuevo:

    - todo Preprocessor devuelve BGR uint8 con el mismo (H, W) que la entrada
      (los que redimensionan o recortan se declaran exentos explícitamente);
    - todo Segmenter devuelve una máscara bool con el (H, W) de la entrada;
    - toda Metric devuelve un float y respeta su `higher_is_better`;
    - todos los componentes son instanciables con sus parámetros por defecto.
"""

from __future__ import annotations


def test_preprocessors_preserve_shape_and_dtype():
    raise NotImplementedError


def test_segmenters_return_boolean_mask():
    raise NotImplementedError


def test_metrics_return_float_in_range():
    raise NotImplementedError
