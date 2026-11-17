"""EJEMPLO — plantilla de un preprocesador. NO forma parte del sistema final.

Este fichero existe solo para enseñar cómo se implementa y se registra un
`Preprocessor`. La técnica que aplica (sumar una constante al brillo) es
deliberadamente trivial: no es una propuesta de método para el proyecto.

Para crear un preprocesador real:
    1. Copia este fichero con el nombre del método (p. ej. `denoise.py`).
    2. Cambia el nombre de registro y el de la clase.
    3. Implementa `apply` respetando el contrato (ver README, sección 4.2).
    4. Ya puedes usarlo desde cualquier YAML; no hay nada más que tocar.
"""

from __future__ import annotations

import numpy as np

from apple_seg.core.registry import PREPROCESSORS
from apple_seg.core.types import Image
from apple_seg.preprocessing.base import Preprocessor


@PREPROCESSORS.register("ejemplo_brillo")
class EjemploPreprocesador(Preprocessor):
    """EJEMPLO: suma una constante al brillo de la imagen.

    Ilustra los cuatro puntos del contrato que suelen fallar:
        - los parámetros se declaran en `__init__` y se pasan a `super()`,
          para que aparezcan en el informe del experimento;
        - la imagen de entrada NO se modifica (se trabaja sobre una copia);
        - la salida mantiene (H, W, 3) y dtype uint8;
        - el desbordamiento se controla explícitamente (clip antes de castear).

    Args:
        delta: Cantidad sumada a cada canal, en niveles de gris [-255, 255].
    """

    def __init__(self, delta: int = 20) -> None:
        super().__init__(delta=delta)
        self.delta = delta

    def apply(self, image: Image) -> Image:
        salida = image.astype(np.int16) + self.delta
        return np.clip(salida, 0, 255).astype(np.uint8)
