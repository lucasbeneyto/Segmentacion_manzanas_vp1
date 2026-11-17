# Datos

Las imágenes **no se versionan** en el repositorio (ver `.gitignore`).

Estructura esperada:

```
data/
├── raw/
│   ├── images/   # imágenes originales del árbol (RGB)
│   └── masks/    # máscaras de referencia, mismo nombre base que su imagen
└── processed/    # caché opcional de imágenes preprocesadas
```

Convenciones:

- Cada imagen `data/raw/images/<nombre>.<ext>` tiene su máscara en
  `data/raw/masks/`, cuyo nombre se obtiene con la plantilla `mask_template` del YAML (por defecto `{stem}.png`).
- Las máscaras pueden venir en {0,255}, {0,1} o en color: `DiskImageLoader` las binariza a `bool` (`True` = manzana). Cualquier píxel distinto de 0 es manzana.
- Si el dataset original trae otra organización, **no se renombran los ficheros a mano**: se ajusta `image_glob` / `mask_template` en la configuración.
