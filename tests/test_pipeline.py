"""Prueba de integración del pipeline completo.

Ejecuta un experimento mínimo (2 preprocesadores x 2 segmentadores x 2 métricas)
sobre un dataset sintético y comprueba que la tabla de resultados tiene el
número de filas esperado, las columnas del formato canónico y que se han
escrito los ficheros de salida.
"""

from __future__ import annotations


def test_runner_produces_expected_rows(tmp_path):
    raise NotImplementedError
