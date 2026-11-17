"""Particionado del dataset en subconjuntos de ajuste y de test.

Aunque el proyecto usa técnicas clásicas (sin entrenamiento), varios métodos
tienen umbrales y parámetros que se eligen mirando imágenes. Para que la
evaluación sea honesta, esos parámetros se ajustan sobre el split de
desarrollo (`dev`) y las métricas que se reportan se calculan sobre `test`.

Los splits son deterministas (semilla fija) y se guardan en disco para que todo
el equipo trabaje exactamente con la misma partición.
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence


def random_split(
    sample_ids: Sequence[str], dev_ratio: float = 0.3, seed: int = 42
) -> dict[str, list[str]]:
    """Reparto aleatorio reproducible en {'dev': [...], 'test': [...]}."""
    raise NotImplementedError


def save_split(split: dict[str, list[str]], path: str | Path) -> None:
    """Guarda la partición en JSON para compartirla en el repositorio."""
    raise NotImplementedError


def load_split(path: str | Path) -> dict[str, list[str]]:
    """Carga una partición previamente guardada."""
    raise NotImplementedError
