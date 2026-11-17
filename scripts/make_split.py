"""Genera y guarda la partición dev/test del dataset.

Se ejecuta UNA VEZ al principio del proyecto; el fichero resultante
(configs/split.json) se versiona en el repositorio para que todo el equipo
ajuste y evalúe exactamente sobre las mismas imágenes.

Uso:
    python scripts/make_split.py --dev-ratio 0.3 --seed 42
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def main() -> int:
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
