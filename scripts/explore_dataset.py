"""Inspección inicial del dataset (paso previo a diseñar los métodos).

Genera en results/figures/ el material que justifica las decisiones de diseño
en la memoria:
    - estadísticas: nº de imágenes, resolución, % medio de píxeles de manzana,
      nº de manzanas por imagen, imágenes sin fruto;
    - histogramas de color de los píxeles de manzana frente a los de fondo en
      HSV y Lab, que es lo que fija los rangos iniciales de los umbrales;
    - mosaico de muestras con su máscara superpuesta.

Uso:
    python scripts/explore_dataset.py --config configs/default.yaml
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def main() -> int:
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
