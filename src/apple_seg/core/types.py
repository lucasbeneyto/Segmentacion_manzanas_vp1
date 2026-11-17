"""Tipos y estructuras de datos compartidas por todos los bloques.

Define el "idioma común" del pipeline: qué es una imagen, qué es una máscara y
qué objetos viajan entre bloques. Si todos los módulos respetan estas
convenciones, cualquier preprocesador se puede combinar con cualquier
segmentador y con cualquier métrica.

Convenciones (OBLIGATORIAS para todo el equipo):
    - Imagen en color : np.ndarray (H, W, 3), dtype=uint8, orden de canales BGR
                        (el que devuelve cv2.imread).
    - Imagen en gris  : np.ndarray (H, W), dtype=uint8.
    - Máscara         : np.ndarray (H, W), dtype=bool. True = píxel de manzana.
    - Las máscaras del dataset se binarizan al cargarlas (ver data.loader).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

# Alias semánticos; no son tipos reales, documentan la forma esperada del array.
Image = np.ndarray  # (H, W, 3) uint8, BGR
GrayImage = np.ndarray  # (H, W) uint8
Mask = np.ndarray  # (H, W) bool


@dataclass
class Sample:
    """Una muestra del dataset: imagen original y su máscara de referencia.

    Attributes:
        sample_id: Identificador único (normalmente el nombre del fichero sin extensión).
        image: Imagen RGB/BGR original, sin preprocesar.
        gt_mask: Máscara de referencia (ground truth). None en inferencia pura.
        meta: Metadatos libres (ruta, tamaño original, split, etc.).
    """

    sample_id: str
    image: Image
    gt_mask: Mask | None = None
    meta: dict[str, Any] = field(default_factory=dict)

    @property
    def shape(self) -> tuple[int, int]:
        """Alto y ancho de la imagen."""
        return self.image.shape[0], self.image.shape[1]


@dataclass
class Prediction:
    """Resultado de aplicar una combinación (preprocesador, segmentador) a una muestra.

    Es la unidad que consume el bloque de evaluación y el de reporting.

    Attributes:
        sample_id: Muestra de la que procede.
        pred_mask: Máscara binaria predicha (H, W) bool.
        preprocessor_id: Identificador de la cadena de preprocesado utilizada.
        segmenter_id: Identificador del segmentador utilizado.
        runtime_s: Tiempo de cómputo (preproceso + segmentación) en segundos.
        intermediate: Imágenes intermedias opcionales para figuras cualitativas
            (p. ej. {"preprocessed": img, "raw_mask": m}). No se usa en métricas.
    """

    sample_id: str
    pred_mask: Mask
    preprocessor_id: str
    segmenter_id: str
    runtime_s: float = 0.0
    intermediate: dict[str, np.ndarray] = field(default_factory=dict)

    @property
    def combo_id(self) -> str:
        """Identificador legible de la combinación evaluada."""
        return f"{self.preprocessor_id}+{self.segmenter_id}"


def as_mask(array: np.ndarray) -> Mask:
    """Normaliza cualquier array a máscara booleana (H, W).

    Acepta máscaras uint8 {0,255}, {0,1}, float en [0,1] o imágenes de 3 canales
    (en cuyo caso se reduce al primer canal). Es el punto único donde se decide
    qué cuenta como "píxel positivo".
    """
    arr = np.asarray(array)
    if arr.ndim == 3:
        arr = arr[..., 0]
    if arr.dtype == bool:
        return arr
    if np.issubdtype(arr.dtype, np.floating):
        return arr > 0.5
    return arr > 0


def check_same_shape(pred: Mask, gt: Mask) -> None:
    """Valida que predicción y ground truth sean comparables; lanza ValueError si no."""
    if pred.shape != gt.shape:
        raise ValueError(
            f"Dimensiones incompatibles: pred={pred.shape} vs gt={gt.shape}. "
            "Si el preprocesado redimensiona, debe revertirse antes de evaluar."
        )
