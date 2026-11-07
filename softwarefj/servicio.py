"""Clase abstracta Servicio: contrato común de todos los servicios."""

from abc import abstractmethod

from .entidad import Entidad
from .excepciones import (CalculoInconsistenteError, ParametroFaltanteError,
                          ServicioInvalidoError)
from .logger import log


class Servicio(Entidad):
    """Servicio ofrecido por Software FJ (clase abstracta)."""

    def __init__(self, nombre: str = None, tarifa_hora: float = None):
        super().__init__()  # Id único
        # Parámetros obligatorios
        if nombre is None or tarifa_hora is None:
            raise ParametroFaltanteError("Faltan datos del servicio",
                                         "nombre y tarifa_hora son obligatorios")
        # Validación de nombre y tarifa
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("Nombre de servicio inválido", repr(nombre))
        if isinstance(tarifa_hora, bool) or not isinstance(tarifa_hora, (int, float)) \
                or tarifa_hora <= 0:
            raise ServicioInvalidoError("Tarifa inválida", repr(tarifa_hora))
        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = True  # Todo servicio nace disponible

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_hora(self) -> float:
        return self._tarifa_hora

    @property
    def disponible(self) -> bool:
        return self._disponible

    def cambiar_disponibilidad(self, disponible: bool):
        """Activa o desactiva el servicio y deja registro en el log."""
        self._disponible = bool(disponible)
        log.info("Servicio %s disponible=%s", self._nombre, self._disponible)

    # ---- Métodos abstractos (cada servicio los sobrescribe) ----
    @abstractmethod
    def validar_parametros(self, duracion: float) -> None:
        """Valida la duración según las reglas propias del servicio."""

    @abstractmethod
    def costo_base(self, duracion: float) -> float:
        """Calcula el costo sin impuestos ni descuentos."""

    # ---- "Sobrecarga" de métodos ----
    # Python no tiene sobrecarga nativa: se simula con parámetros opcionales
    # y con *args (distintas firmas de llamada para el mismo método).
    def calcular_costo(self, duracion: float, impuesto: float = 0.0,
                       descuento: float = 0.0) -> float:
        """Costo con impuesto y descuento opcionales (fracciones: 0.19 = 19%)."""
        self.validar_parametros(duracion)
        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:
            raise CalculoInconsistenteError(
                "Impuesto o descuento fuera de rango [0, 1]",
                f"impuesto={impuesto}, descuento={descuento}")
        total = self.costo_base(duracion) * (1 - descuento) * (1 + impuesto)
        if total < 0:  # Defensa contra resultados imposibles
            raise CalculoInconsistenteError("Costo negativo", str(total))
        return round(total, 2)

    def cotizar(self, *args) -> float:
        """Variantes: cotizar(dur) | cotizar(dur, impuesto) | cotizar(dur, imp, desc)."""
        if not 1 <= len(args) <= 3:
            raise ParametroFaltanteError("cotizar() recibe de 1 a 3 argumentos",
                                         f"recibió {len(args)}")
        return self.calcular_costo(*args)

    @abstractmethod
    def describir(self) -> str:
        """Descripción del servicio (polimórfica)."""
