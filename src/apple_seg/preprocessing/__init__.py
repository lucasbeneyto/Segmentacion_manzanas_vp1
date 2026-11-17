"""BLOQUE 1 — Preprocesado.

Transforma la imagen de entrada en otra imagen (mismo alto y ancho) más
favorable para la segmentación.

Clase padre del bloque: `Preprocessor`.
Composición: `PreprocessingChain` (es a su vez un Preprocessor, patrón composite),
lo que permite encadenar N pasos y tratar la cadena como un único componente.

Los módulos con los preprocesadores reales los añade el equipo; cada uno se
registra solo con el decorador @PREPROCESSORS.register y debe importarse aquí
abajo para que el registro lo conozca. `EJEMPLO_preprocesador.py` es la
plantilla a copiar; no forma parte del sistema final.
"""

from apple_seg.preprocessing.base import Preprocessor
from apple_seg.preprocessing.chain import Identity, PreprocessingChain

# Los imports siguientes existen por su efecto colateral: registrar componentes.
# Añade aquí una línea por cada módulo nuevo de preprocesadores.
from apple_seg.preprocessing import EJEMPLO_preprocesador  # noqa: F401

__all__ = ["Preprocessor", "PreprocessingChain", "Identity"]
