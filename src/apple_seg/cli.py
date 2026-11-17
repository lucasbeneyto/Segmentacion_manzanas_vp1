"""Interfaz de línea de comandos del proyecto.

Punto de entrada único para lanzar y consultar experimentos:

    python -m apple_seg.cli run configs/experiments/baseline.yaml
    python -m apple_seg.cli list-components
    python -m apple_seg.cli report results/runs/baseline

Subcomandos:
    run             : ejecuta un experimento completo desde un YAML.
    list-components : muestra preprocesadores, segmentadores y métricas
                      registrados (útil para saber qué hay disponible sin leer
                      el código).
    report          : regenera tablas y figuras de un run ya ejecutado.
    compare         : tabla comparativa de varios runs.
"""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    """Define los subcomandos y sus argumentos."""
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """Punto de entrada de la CLI. Devuelve el código de salida del proceso."""
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
