"""Lectura de la configuración de un experimento (YAML) y construcción de objetos.

Traduce un fichero declarativo a instancias reales usando los registros de
`core.registry`. Es el único sitio donde se "interpreta" el YAML: el pipeline
recibe ya listas de objetos Preprocessor / Segmenter / Metric.

Formato esperado (ver configs/default.yaml):

    dataset:
      images_dir: data/raw/images
      masks_dir: data/raw/masks
    preprocessors:            # una entrada = una CADENA de pasos
      - id: baseline
        steps: []
      - id: mi_cadena
        steps:
          - {name: mi_preprocesador, params: {...}}
          - {name: otro_preprocesador, params: {...}}
    segmenters:
      - {id: mi_config, name: mi_segmentador, params: {...}}
    metrics:
      - {name: mi_metrica}
    output:
      run_name: baseline
      results_dir: results
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from apple_seg.core.registry import METRICS, PREPROCESSORS, SEGMENTERS


@dataclass
class DatasetConfig:
    """Rutas y opciones de carga del dataset."""

    images_dir: Path
    masks_dir: Path | None = None
    image_glob: str = "*"
    mask_template: str = "{stem}.png"
    limit: int | None = None
    resize: tuple[int, int] | None = None


@dataclass
class OutputConfig:
    """Dónde y cómo se escriben resultados (tablas, figuras, máscaras)."""

    run_name: str = "run"
    results_dir: Path = Path("results")
    save_masks: bool = True
    save_qualitative: bool = True
    n_qualitative: int = 6


@dataclass
class ExperimentConfig:
    """Configuración completa de un experimento ya resuelta a objetos."""

    dataset: DatasetConfig
    preprocessors: list[Any] = field(default_factory=list)  # list[Preprocessor]
    segmenters: list[Any] = field(default_factory=list)  # list[Segmenter]
    metrics: list[Any] = field(default_factory=list)  # list[Metric]
    output: OutputConfig = field(default_factory=OutputConfig)
    raw: dict[str, Any] = field(default_factory=dict)  # YAML original, para trazabilidad

    @classmethod
    def from_yaml(cls, path: str | Path) -> "ExperimentConfig":
        """Carga un YAML y construye todos los componentes vía los registros."""
        raise NotImplementedError

    def summary(self) -> str:
        """Resumen en texto del experimento (nº de combinaciones, nombres, etc.)."""
        raise NotImplementedError


def build_preprocessors(specs: list[dict[str, Any]]) -> list[Any]:
    """Construye una lista de cadenas de preprocesado a partir de la sección `preprocessors`.

    Cada spec con `steps` se envuelve en un PreprocessingChain, de modo que el
    pipeline siempre trabaja con objetos que cumplen el contrato Preprocessor.
    """
    raise NotImplementedError


def build_segmenters(specs: list[dict[str, Any]]) -> list[Any]:
    """Instancia los segmentadores declarados en la sección `segmenters`."""
    raise NotImplementedError


def build_metrics(specs: list[dict[str, Any]]) -> list[Any]:
    """Instancia las métricas declaradas en la sección `metrics`."""
    raise NotImplementedError


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Lee un YAML a diccionario (utilidad fina sobre pyyaml)."""
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}
