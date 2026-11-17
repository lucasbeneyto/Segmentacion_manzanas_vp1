"""apple_seg — Sistema de visión clásico para la segmentación de manzanas en árbol.

Paquete raíz del proyecto final de Visión por Computador I (curso 2026/2027).

La arquitectura se organiza en tres bloques principales e intercambiables, unidos
por el pipeline:

    data  ->  preprocessing  ->  segmentation  ->  evaluation  ->  reporting

Cada bloque expone una clase padre (contrato) y N implementaciones concretas que
se registran por nombre, de forma que un experimento se define por completo desde
un fichero YAML sin tocar el código del pipeline.

Clases padre del contrato:
    - preprocessing.Preprocessor
    - segmentation.Segmenter
    - evaluation.Metric
    - data.ImageLoader
"""

__version__ = "0.1.0"
