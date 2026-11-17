"""Motor del pipeline: `ExperimentRunner`.

Es el corazón del proyecto. Flujo de una ejecución:

    1. Carga el dataset con el ImageLoader de la configuración.
    2. Ajusta (fit) los segmentadores que lo requieran, usando SOLO el split dev.
    3. Para cada combinación (preprocesador, segmentador) y cada imagen de test:
         imagen -> preprocesador.apply -> segmentador.predict -> Prediction
       midiendo el tiempo de cómputo.
    4. Pasa las predicciones al Evaluator -> tabla larga de métricas.
    5. Escribe en results/runs/<run_name>/: config, tablas, máscaras y figuras.

Garantías que debe cumplir y que conviene no romper al modificarlo:
    - Determinismo: misma configuración -> mismos resultados (semillas fijadas).
    - Aislamiento: un fallo en una combinación se registra y no aborta el resto.
    - Trazabilidad: todo resultado es reconstruible desde el config.yaml del run.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from apple_seg.core.config import ExperimentConfig
from apple_seg.core.types import Prediction, Sample
from apple_seg.preprocessing.base import Preprocessor
from apple_seg.segmentation.base import Segmenter


class ExperimentRunner:
    """Ejecuta un experimento completo definido por una `ExperimentConfig`."""

    def __init__(self, config: ExperimentConfig) -> None:
        raise NotImplementedError

    def run(self) -> pd.DataFrame:
        """Ejecuta todas las combinaciones y devuelve la tabla larga de métricas.

        Efectos: crea la carpeta del run y escribe tablas, máscaras y figuras.
        """
        raise NotImplementedError

    def run_single(
        self, sample: Sample, preprocessor: Preprocessor, segmenter: Segmenter
    ) -> Prediction:
        """Aplica una combinación a una muestra y mide el tiempo de cómputo.

        Es también el punto de entrada para depurar un caso concreto desde un
        notebook sin lanzar el experimento entero.
        """
        raise NotImplementedError

    def _fit_segmenters(self, dev_samples: list[Sample]) -> None:
        """Llama a `fit` en los segmentadores con `requires_fit = True`."""
        raise NotImplementedError

    @property
    def run_dir(self) -> Path:
        """Carpeta de salida de este run."""
        raise NotImplementedError
