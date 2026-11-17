"""Pruebas de los segmentadores sobre imágenes sintéticas.

Con discos rojos sobre fondo verde, cualquier método razonable debe alcanzar un
IoU alto; sirve de prueba de humo que detecta errores de canales (BGR/RGB
invertidos) y de inversión de máscara.
"""

from __future__ import annotations


def test_color_segmenter_on_synthetic_apples():
    raise NotImplementedError
