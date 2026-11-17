"""Registro de componentes: permite instanciar preprocesadores, segmentadores y
métricas a partir de su nombre en texto (el que aparece en los YAML de configuración).

Es la pieza que hace dinámico el pipeline: añadir un nuevo método consiste en
escribir la clase y decorarla con @PREPROCESSORS.register("mi_metodo"); no hay
que tocar ni el runner ni la configuración del resto del equipo.

Ejemplo:
    @SEGMENTERS.register("mi_segmentador")
    class MiSegmentador(Segmenter):
        ...

    seg = SEGMENTERS.create("mi_segmentador", umbral=140)
"""

from __future__ import annotations

from typing import Any, Callable, Iterable, TypeVar

T = TypeVar("T")


class Registry:
    """Diccionario nombre -> clase, con decorador de registro y factoría."""

    def __init__(self, kind: str) -> None:
        self.kind = kind
        self._items: dict[str, type] = {}

    def register(self, name: str) -> Callable[[type[T]], type[T]]:
        """Decorador que da de alta una clase bajo un nombre único."""

        def _wrap(cls: type[T]) -> type[T]:
            key = name.lower()
            if key in self._items:
                raise KeyError(f"Ya existe un {self.kind} registrado como '{key}'")
            self._items[key] = cls
            setattr(cls, "registry_name", key)
            return cls

        return _wrap

    def get(self, name: str) -> type:
        """Devuelve la clase registrada; error explícito con las opciones válidas."""
        key = name.lower()
        if key not in self._items:
            raise KeyError(
                f"{self.kind} desconocido: '{name}'. Disponibles: {sorted(self._items)}"
            )
        return self._items[key]

    def create(self, name: str, **params: Any) -> Any:
        """Instancia el componente registrado con los parámetros dados."""
        return self.get(name)(**params)

    def available(self) -> list[str]:
        """Nombres registrados, ordenados."""
        return sorted(self._items)

    def __contains__(self, name: object) -> bool:
        return isinstance(name, str) and name.lower() in self._items

    def __iter__(self) -> Iterable[str]:
        return iter(sorted(self._items))

    def __len__(self) -> int:
        return len(self._items)


PREPROCESSORS = Registry("preprocessor")
SEGMENTERS = Registry("segmenter")
METRICS = Registry("metric")
