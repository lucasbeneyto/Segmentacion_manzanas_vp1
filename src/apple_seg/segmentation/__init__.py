"""BLOQUE 2 — Segmentación.

Convierte una imagen (ya preprocesada) en una máscara binaria donde True marca
los píxeles de manzana. Solo se emplean técnicas clásicas de visión por
computador, las estudiadas en la asignatura.

Clase padre del bloque: `Segmenter`.
Refinamiento opcional posterior: `postprocess.MaskRefiner` (morfología,
filtrado por forma, ...), que forma parte de este bloque porque opera sobre
máscaras, no sobre imágenes.

Los módulos con los segmentadores reales los añade el equipo; cada uno se
registra solo con el decorador @SEGMENTERS.register y debe importarse aquí
abajo para que el registro lo conozca. `EJEMPLO_segmentador.py` es la plantilla
a copiar; no forma parte del sistema final.
"""

from apple_seg.segmentation.base import Segmenter
from apple_seg.segmentation.postprocess import MaskRefiner, RefinementChain

# Los imports siguientes existen por su efecto colateral: registrar componentes.
# Añade aquí una línea por cada módulo nuevo de segmentadores.
from apple_seg.segmentation import EJEMPLO_segmentador  # noqa: F401

__all__ = ["Segmenter", "MaskRefiner", "RefinementChain"]
