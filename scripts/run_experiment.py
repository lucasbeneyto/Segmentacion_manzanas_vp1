"""Lanza un experimento completo desde un fichero de configuración.

Uso:
    python scripts/run_experiment.py configs/experiments/EJEMPLO_experimento.yaml

Envoltorio fino sobre `apple_seg.cli run`; existe para poder ejecutar el
pipeline sin instalar el paquete (añade src/ al path).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def main() -> int:
    from apple_seg.cli import main as cli_main

    return cli_main(["run", *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())
