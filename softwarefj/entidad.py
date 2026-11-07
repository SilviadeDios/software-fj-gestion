"""Clase abstracta base para las entidades generales del sistema."""

from abc import ABC, abstractmethod  # Herramientas para clases abstractas
from itertools import count  # Generador de números consecutivos


class Entidad(ABC):
    """Representa cualquier entidad del sistema (cliente, servicio, reserva)."""

    # Contador compartido: cada entidad creada recibe un id único
    _contador = count(1)

    def __init__(self):
        # El id es de solo lectura (encapsulado con un atributo privado)
        self._id = next(Entidad._contador)

    @property
    def id(self) -> int:
        """Identificador único de la entidad (solo lectura)."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción legible; cada subclase la implementa."""

    def __str__(self) -> str:
        # La representación en texto reutiliza la descripción polimórfica
        return self.describir()
