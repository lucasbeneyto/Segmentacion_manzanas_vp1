"""EJEMPLO — plantilla de un segmentador y de un refinador de máscara.
NO forma parte del sistema final.

Este fichero existe solo para enseñar cómo se implementan y se registran un
`Segmenter` y un `MaskRefiner`. Las técnicas que aplican (umbral fijo sobre el
canal rojo, y apertura morfológica) son deliberadamente triviales: no son una
propuesta de método para el proyecto.

Para crear un segmentador real:
    1. Copia este fichero con el nombre de la familia de métodos
       (p. ej. `color_threshold.py`).
    2. Cambia el nombre de registro y el de la clase.
    3. Implementa `segment` respetando el contrato (ver README, sección 4.3).
    4. Si el método necesita estimar parámetros a partir de imágenes,
       impleméntalo en `fit` y declara `requires_fit = True`.
"""

from __future__ import annotations

from typing import Iterable

import cv2
import numpy as np

from apple_seg.core.registry import SEGMENTERS
from apple_seg.core.types import Image, Mask, Sample
from apple_seg.segmentation.base import Segmenter
from apple_seg.segmentation.postprocess import MaskRefiner


@SEGMENTERS.register("ejemplo_umbral_rojo")
class EjemploSegmentador(Segmenter):
    """EJEMPLO: marca como manzana los píxeles con canal R por encima de un umbral.

    Ilustra los puntos del contrato que suelen fallar:
        - la imagen llega en BGR (el canal rojo es el índice 2, no el 0);
        - la salida es un array de dtype bool, NO uint8 ni {0, 255};
        - la máscara conserva el (H, W) de la entrada;
        - la imagen de entrada no se modifica;
        - el refinado morfológico no se hace aquí dentro, sino en `refiner`,
          que la clase padre aplica sola dentro de `predict`.

    Args:
        umbral: Valor mínimo del canal rojo para considerar un píxel manzana.
    """

    def __init__(self, umbral: int = 150, **kwargs) -> None:
        super().__init__(umbral=umbral, **kwargs)
        self.umbral = umbral

    def segment(self, image: Image) -> Mask:
        canal_rojo = image[:, :, 2]
        return canal_rojo > self.umbral


@SEGMENTERS.register("ejemplo_umbral_rojo_ajustable")
class EjemploSegmentadorConAjuste(Segmenter):
    """EJEMPLO: igual que el anterior, pero estimando el umbral a partir de datos.

    Muestra cómo se usa `fit` para los métodos que necesitan ajustar parámetros.
    El runner llama a `fit` UNA sola vez y SOLO con el split `dev`; usar `test`
    para ajustar invalidaría los resultados.

    Args:
        percentil: Percentil del canal rojo de los píxeles de manzana del split
            de desarrollo que se toma como umbral.
    """

    requires_fit = True

    def __init__(self, percentil: float = 10.0, **kwargs) -> None:
        super().__init__(percentil=percentil, **kwargs)
        self.percentil = percentil
        self.umbral_: int = 150  # valor por defecto hasta que se llame a fit

    def fit(self, samples: Iterable[Sample]) -> "EjemploSegmentadorConAjuste":
        valores = [
            s.image[:, :, 2][s.gt_mask]
            for s in samples
            if s.gt_mask is not None and s.gt_mask.any()
        ]
        if valores:
            self.umbral_ = int(np.percentile(np.concatenate(valores), self.percentil))
        self.is_fitted = True
        return self

    def segment(self, image: Image) -> Mask:
        return image[:, :, 2] > self.umbral_


class EjemploRefinador(MaskRefiner):
    """EJEMPLO: apertura morfológica sobre la máscara. NO es una propuesta de método.

    Plantilla de `MaskRefiner`: bool (H, W) -> bool (H, W). Los refinadores se
    declaran aparte del segmentador para poder medir en las tablas cuánto
    aportan, en lugar de esconderlos dentro de `segment`.

    Args:
        ksize: Lado del elemento estructurante elíptico.
    """

    def __init__(self, ksize: int = 5) -> None:
        super().__init__(ksize=ksize)
        self.ksize = ksize

    def apply(self, mask: Mask) -> Mask:
        elemento = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (self.ksize, self.ksize))
        abierta = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_OPEN, elemento)
        return abierta.astype(bool)
