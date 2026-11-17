# Segmentación de manzanas en árbol — Visión por Computador I (2026/2027)

Sistema de visión **clásico** (sin aprendizaje profundo) que identifica las manzanas
presentes en el árbol situado frente al robot recolector, y marco experimental para
medir objetivamente qué combinación de técnicas funciona mejor.

> **Entregas:** código + memoria el **9 de diciembre de 2026**; defensa (10 min) el
> **15 de diciembre de 2026**. La memoria debe incluir la declaración de uso de
> herramientas de IA (plantilla en [docs/memoria.md](docs/memoria.md)).

---

## 1. Qué es este documento

Este README es el **contrato** entre las partes del sistema. Describe las clases padre
de cada bloque y las reglas que deben cumplir sus implementaciones. Si cada persona
respeta el contrato de su bloque, **cualquier** preprocesador se puede combinar con
**cualquier** segmentador y evaluar con **cualquier** métrica, sin tocar el pipeline.

Regla de oro: **se programa contra las clases padre, nunca contra una implementación concreta.**

---

## 2. Arquitectura

```
                    configs/*.yaml
                          │
                          ▼
   data          preprocessing        segmentation          evaluation        reporting
┌──────────┐   ┌────────────────┐   ┌───────────────┐   ┌───────────────┐   ┌──────────┐
│ImageLoader│──▶│  Preprocessor  │──▶│   Segmenter   │──▶│    Metric     │──▶│ tablas + │
│  Sample   │   │ (+ Chain)      │   │ (+MaskRefiner)│   │ (+ Evaluator) │   │ figuras  │
└──────────┘   └────────────────┘   └───────────────┘   └───────────────┘   └──────────┘
      imagen BGR        imagen BGR          máscara bool        float (por imagen)
      + máscara GT      (misma H,W)         (misma H,W)
                          └──────────── pipeline.ExperimentRunner ───────────┘
```

Dependencias permitidas: `pipeline → bloques → core`. **Ningún bloque importa de `pipeline` ni de otro bloque hermano.**

### Estructura de carpetas

```
Proyecto_VP_segmentacion/
├── README.md                    ← este contrato
├── pyproject.toml / requirements.txt
├── configs/
│   ├── default.yaml             valores por defecto del pipeline
│   ├── split.json               partición dev/test fija (la genera make_split.py)
│   └── experiments/             un YAML por experimento
├── data/                        dataset (no versionado) — ver data/README.md
├── docs/                        guion de la memoria y notas de diseño
├── notebooks/                   exploración y depuración puntual
├── results/
│   ├── runs/<run_name>/         config + métricas + máscaras de cada ejecución
│   ├── figures/  tables/        entregables para la memoria
├── scripts/
│   ├── make_split.py            genera configs/split.json (una sola vez)
│   ├── explore_dataset.py       estadísticas e histogramas de color del dataset
│   └── run_experiment.py        lanza un experimento desde un YAML
├── src/apple_seg/
│   ├── core/        tipos, registro de componentes, configuración, E/S, logging
│   ├── data/        ImageLoader, AppleDataset, splits
│   ├── preprocessing/  BLOQUE 1  (base.py, chain.py, EJEMPLO_preprocesador.py)
│   ├── segmentation/   BLOQUE 2  (base.py, postprocess.py, EJEMPLO_segmentador.py)
│   ├── evaluation/     BLOQUE 3  (base.py, evaluator.py, EJEMPLO_metrica.py)
│   ├── pipeline/    ExperimentRunner, CombinationGrid, ResultStore
│   ├── reporting/   tablas y figuras
│   └── cli.py       interfaz de línea de comandos
└── tests/           test_contracts.py verifica automáticamente este README
```

---

## 3. Tipos comunes (`apple_seg.core.types`)

Son el idioma del sistema. **No negociables.**

| Concepto | Representación |
|---|---|
| Imagen en color | `np.ndarray (H, W, 3)`, `uint8`, canales **BGR** (como `cv2.imread`) |
| Imagen en gris | `np.ndarray (H, W)`, `uint8` |
| Máscara | `np.ndarray (H, W)`, `bool`, `True` = píxel de manzana |

- `Sample(sample_id, image, gt_mask, meta)` — lo que entrega el loader.
- `Prediction(sample_id, pred_mask, preprocessor_id, segmenter_id, runtime_s, intermediate)` — lo que produce el pipeline y consume la evaluación.
- `as_mask(array)` — único punto donde se decide qué es un píxel positivo al cargar.

---

## 4. Las cuatro clases padre

### 4.1 `data.ImageLoader` — carga de imágenes

```python
class ImageLoader(ABC):
    def __len__(self) -> int: ...
    def __getitem__(self, index: int) -> Sample: ...
    def sample_ids(self) -> list[str]: ...
    def __iter__(self) -> Iterator[Sample]      # ya implementado en la base
```

**Contrato**

1. Devuelve imágenes **BGR uint8** y máscaras **bool**, pase lo que pase en disco.
2. Es el **único** módulo que lee ficheros del dataset.
3. Si redimensiona, la máscara se reescala con interpolación `NEAREST`.

Implementación de referencia: `DiskImageLoader` (carpetas paralelas
`images/` + `masks/`, emparejadas por `mask_template`).

---

### 4.2 `preprocessing.Preprocessor` — BLOQUE 1

```python
class Preprocessor(ABC):
    registry_name: str
    def __init__(self, **params): ...
    def apply(self, image: Image) -> Image:   # ← lo único que implementas
    def __call__(self, image) -> Image        # = apply
    def get_params(self) -> dict
    @property
    def id(self) -> str
```

**Contrato**

1. `apply` recibe BGR uint8 `(H, W, 3)` y devuelve **BGR uint8 `(H, W, 3)` con el mismo alto y ancho**. Si trabajas en HSV/Lab/gris, **conviertes de vuelta** antes de devolver.
2. **No modifiques la imagen de entrada** (`image.copy()` si hace falta).
3. Todos los parámetros van en `__init__` y se pasan a `super().__init__(**params)`,
   para que aparezcan en el informe del experimento.
4. Registro obligatorio: `@PREPROCESSORS.register("nombre_unico")`.
5. Única excepción admitida: un preprocesador que redimensione o recorte. Debe dejar el
   tamaño original en `Sample.meta` para que el runner revierta la máscara antes de
   evaluar; si no, la comparación con el ground truth falla.

**Composición**: `PreprocessingChain` aplica N pasos y *es* un `Preprocessor`, así que
el pipeline trata igual «un paso» que «una cadena». La cadena vacía (`Identity`) es el
**baseline obligatorio** de todo experimento.

**Ficheros del bloque**

| Fichero | Contenido |
|---|---|
| `base.py` | `Preprocessor` (clase padre) |
| `chain.py` | `Identity` + `PreprocessingChain` |
| `EJEMPLO_preprocesador.py` | plantilla comentada a copiar — **no forma parte del sistema** |

Los preprocesadores reales van en módulos nuevos que crea el equipo, agrupados por
familia (ruido, contraste, iluminación, color…). Al crear un módulo, **impórtalo en
`preprocessing/__init__.py`** para que el registro lo conozca.

---

### 4.3 `segmentation.Segmenter` — BLOQUE 2

```python
class Segmenter(ABC):
    registry_name: str
    requires_fit: bool = False
    def __init__(self, refiner=None, **params): ...
    def segment(self, image: Image) -> Mask:    # ← lo único obligatorio
    def fit(self, samples: Iterable[Sample]) -> Segmenter   # opcional
    def predict(self, image) -> Mask            # segment + refiner (lo llama el pipeline)
    def get_params(self) -> dict
    @property
    def id(self) -> str
```

**Contrato**

1. `segment` recibe la imagen **ya preprocesada** y devuelve una máscara **bool `(H, W)`**
   con el mismo tamaño. Nada de `uint8`, nada de `{0,255}`.
2. `True` = manzana, siempre. Si tu método produce el fondo, inviértelo tú.
3. **No modifiques la imagen de entrada.**
4. Si el método necesita estimar algo a partir de datos (umbrales, centroides,
   covarianzas), se hace en `fit` y se declara `requires_fit = True`. El runner llama a
   `fit` **solo con el split `dev`**; usar `test` para ajustar invalida los resultados.
5. El refinado morfológico **no va dentro de `segment`**: se declara aparte como
   `refiner`, para poder medir cuánto aporta.
6. Registro obligatorio: `@SEGMENTERS.register("nombre_unico")`.
7. Solo técnicas vistas en la asignatura (restricción del enunciado).

**Ficheros del bloque**

| Fichero | Contenido |
|---|---|
| `base.py` | `Segmenter` (clase padre) |
| `postprocess.py` | `MaskRefiner` (clase padre) + `RefinementChain` |
| `EJEMPLO_segmentador.py` | plantilla comentada a copiar — **no forma parte del sistema** |

Los segmentadores reales van en módulos nuevos que crea el equipo, agrupados por
familia (umbralizado de color, umbralizado automático, regiones, bordes, forma…). Al
crear un módulo, **impórtalo en `segmentation/__init__.py`** para que el registro lo
conozca.

**Refinado de máscara** — `segmentation.postprocess.MaskRefiner`

```python
class MaskRefiner(ABC):
    def apply(self, mask: Mask) -> Mask      # bool (H,W) -> bool (H,W)
    def __call__(self, mask) -> Mask
```

Los refinadores concretos (morfología, relleno de huecos, filtrado por área o por
forma, separación de objetos en contacto…) los implementa el equipo con la misma
mecánica; `RefinementChain` encadena varios y es a su vez un `MaskRefiner`. Plantilla:
clase `EjemploRefinador` en `EJEMPLO_segmentador.py`.

---

### 4.4 `evaluation.Metric` — BLOQUE 3

```python
class Metric(ABC):
    registry_name: str
    higher_is_better: bool = True
    def compute(self, pred: Mask, gt: Mask) -> float:   # ← lo único obligatorio
    def __call__(self, pred, gt) -> float               # valida formas y llama a compute
    def aggregate(self, values: Sequence[float]) -> float   # media por defecto
    def get_params(self) -> dict
```

**Contrato**

1. `compute` devuelve **un único `float` por imagen**. Si la métrica no es promediable
   por imagen, sobrescribe `aggregate`.
2. `higher_is_better = False` en las métricas de error (`count_error`, `hausdorff95`);
   el reporting ordena y resalta las tablas a partir de ese atributo.
3. **Casos degenerados, misma convención en todas las métricas:**
   - `pred` y `gt` ambas vacías → `1.0` (acierto perfecto);
   - solo una vacía → `0.0`.
   Nada de `NaN` silenciosos.
4. Usa `base.confusion(pred, gt)` para contar TP/FP/FN/TN: una sola implementación para
   que todas las métricas cuenten lo mismo.
5. Registro obligatorio: `@METRICS.register("nombre_unico")`.

**Ficheros del bloque**

| Fichero | Contenido |
|---|---|
| `base.py` | `Metric` (clase padre) + `confusion()` (TP/FP/FN/TN, ya implementada) |
| `evaluator.py` | `Evaluator`, que produce la tabla larga |
| `EJEMPLO_metrica.py` | plantilla comentada a copiar — **no forma parte del sistema** |

Las métricas reales van en módulos nuevos que crea el equipo (a nivel de píxel, de
objeto, de contorno…). Al crear un módulo, **impórtalo en `evaluation/__init__.py`**
para que el registro lo conozca. Conviene fijar pronto cuál es la **métrica principal**
del proyecto y declararla en `output.main_metric` del YAML.

`Evaluator` recorre predicciones × métricas y produce la **tabla larga**, formato
canónico de resultados del proyecto:

| sample_id | preprocessor_id | segmenter_id | metric | value | runtime_s |
|---|---|---|---|---|---|
| `img_014` | `clahe_blur` | `watershed_otsu` | `iou` | `0.812` | `0.041` |

Todo lo demás (resúmenes, ranking, gráficos) se **deriva** de esa tabla.

---

## 5. El registro: cómo se hace dinámico el pipeline

`core.registry` mantiene tres diccionarios `nombre → clase`: `PREPROCESSORS`,
`SEGMENTERS`, `METRICS`. Añadir un método nuevo al sistema son **dos pasos**:

```python
# src/apple_seg/segmentation/mi_modulo.py   (y añadir el import en __init__.py)
@SEGMENTERS.register("mi_metodo")
class MiSegmentador(Segmenter):
    def __init__(self, umbral: int = 128, **kwargs):
        super().__init__(umbral=umbral, **kwargs)
    def segment(self, image):
        ...  # devuelve máscara bool (H, W)
```

```yaml
# configs/experiments/mi_experimento.yaml
segmenters:
  - {id: prueba_1, name: mi_metodo, params: {umbral: 140}}
```

No hay que tocar el runner, ni la evaluación, ni el código de nadie más.
`python -m apple_seg.cli list-components` lista lo que hay registrado.

---

## 6. El pipeline (objetivo final)

`pipeline.ExperimentRunner` ejecuta, para una configuración con **M** preprocesadores,
**N** segmentadores y **K** métricas, las **M × N** combinaciones sobre todo el dataset:

1. Carga el dataset con el `ImageLoader`.
2. Llama a `fit` en los segmentadores con `requires_fit` usando **solo el split `dev`**.
3. Para cada combinación e imagen: `preprocesador.apply` → `segmentador.predict` →
   `Prediction`, midiendo el tiempo.
4. `Evaluator` calcula las K métricas → tabla larga.
5. `reporting` escribe tablas y figuras.

Garantías que no deben romperse al modificarlo:

- **Determinismo**: misma configuración → mismos resultados (semillas fijadas).
- **Aislamiento**: si una combinación falla, se registra el error y el resto continúa.
- **Trazabilidad**: cada run guarda el `config.yaml` exacto con el que se generó.

Salida de un run:

```
results/runs/<run_name>/
├── config.yaml             configuración exacta ejecutada
├── run_meta.json           fecha, semilla, nº de imágenes, tiempos
├── metrics_raw.csv         tabla larga (una fila por muestra × combinación × métrica)
├── metrics_summary.csv     tabla agregada: media ± desviación por combinación
├── masks/<combo>/*.png     máscaras predichas
└── figures/                paneles cualitativos, barras, cajas, casos de fallo
```

Convención de color del mapa de errores, igual en todas las figuras:
**verde = TP**, **rojo = FP** (falsa alarma), **azul = FN** (fruto perdido).

---

## 7. Uso

```bash
# 1. Entorno
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .                  # opcional: deja disponible el comando `apple-seg`

# 2. Datos: copiar imágenes y máscaras en data/raw/ (ver data/README.md)

# 3. Partición fija dev/test (una sola vez, se versiona el JSON resultante)
python scripts/make_split.py --dev-ratio 0.3 --seed 42

# 4. Exploración del dataset (histogramas de color → rangos iniciales de umbrales)
python scripts/explore_dataset.py --config configs/default.yaml

# 5. Experimentos (copia EJEMPLO_experimento.yaml y edítalo)
python scripts/run_experiment.py configs/experiments/EJEMPLO_experimento.yaml

# 6. Qué hay disponible / regenerar informes
python -m apple_seg.cli list-components
python -m apple_seg.cli report results/runs/ejemplo

# 7. Pruebas (incluye la verificación automática de este contrato)
pytest
```

---

## 8. Reglas de trabajo en equipo

1. **Un bloque, una persona** (o pareja). El contrato permite trabajar en paralelo sin
   bloquearse: basta con que las firmas de las clases padre no cambien.
2. **Cambiar una clase padre se acuerda entre todos** y se actualiza este README en el
   mismo commit. Añadir implementaciones nuevas no requiere acuerdo alguno.
3. **Nunca se ajustan parámetros mirando `test`.** Para eso está el split `dev`.
4. **Todo resultado que vaya a la memoria sale de un run guardado en `results/runs/`**,
   con su `config.yaml`. Nada de números copiados de una ejecución a mano en un notebook.
5. Los notebooks son para explorar y depurar; el código que acaba funcionando **se mueve
   a `src/`**.
6. Antes de cada commit: `pytest` en verde. `test_contracts.py` recorre todo lo
   registrado y comprueba automáticamente las reglas de las secciones 4.2–4.4.

---

## 9. Estado de implementación

El repositorio contiene **la infraestructura y los contratos, no los métodos**: las
clases padre están escritas por completo, y de cada bloque hay **un único fichero de
ejemplo** (`EJEMPLO_*`) que sirve de plantilla y que se borrará cuando ya no haga falta.
Qué preprocesadores, segmentadores y métricas se implementan es una decisión del equipo
que este repositorio no prejuzga.

| Bloque | Contrato | Implementaciones |
|---|---|---|
| `core` | ✅ tipos y registro operativos | ⬜ config, E/S, logging |
| `data` | ✅ definido | ⬜ `DiskImageLoader`, splits |
| `preprocessing` | ✅ definido (`Identity` operativo) | 🟡 solo la plantilla de ejemplo |
| `segmentation` | ✅ definido | 🟡 solo la plantilla de ejemplo |
| `evaluation` | ✅ definido (`confusion` operativa) | 🟡 solo la plantilla de ejemplo |
| `pipeline` | ✅ definido | ⬜ runner, grid, store |
| `reporting` | ✅ definido | ⬜ tablas y figuras |

Orden de desarrollo recomendado: `DiskImageLoader` → la métrica principal → un primer
segmentador → `ExperimentRunner` (en ese punto ya hay un pipeline de extremo a extremo
con el que medir) → el resto de componentes, en paralelo y sin pisarse.
