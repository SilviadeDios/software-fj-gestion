"""Tres servicios especializados que heredan de Servicio (polimorfismo)."""

from .excepciones import ServicioInvalidoError
from .servicio import Servicio


def _validar_numero(valor, nombre: str, minimo: float, maximo: float):
    """Auxiliar: verifica que valor sea numérico y esté en [minimo, maximo]."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ServicioInvalidoError(f"{nombre} debe ser numérico", repr(valor))
    if not minimo <= valor <= maximo:
        raise ServicioInvalidoError(f"{nombre} fuera de rango [{minimo}, {maximo}]",
                                    repr(valor))


class ReservaSala(Servicio):
    """Reserva de salas de reuniones, con capacidad máxima."""

    def __init__(self, nombre=None, tarifa_hora=None, capacidad: int = 10):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError("Capacidad inválida", repr(capacidad))
        self._capacidad = capacidad

    def validar_parametros(self, duracion: float) -> None:
        # Una sala se reserva entre 1 y 8 horas
        _validar_numero(duracion, "Duración de sala", 1, 8)

    def costo_base(self, duracion: float) -> float:
        # Tarifa por hora multiplicada por las horas reservadas
        return self._tarifa_hora * duracion

    def describir(self) -> str:
        return (f"Sala '{self._nombre}' (capacidad {self._capacidad}) - "
                f"${self._tarifa_hora:,.0f}/h")


class AlquilerEquipo(Servicio):
    """Alquiler de equipos tecnológicos con un cargo fijo de seguro."""

    SEGURO = 20000.0  # Cargo fijo por equipo alquilado

    def __init__(self, nombre=None, tarifa_hora=None, tipo_equipo: str = "Portátil"):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ServicioInvalidoError("Tipo de equipo inválido", repr(tipo_equipo))
        self._tipo_equipo = tipo_equipo.strip()

    def validar_parametros(self, duracion: float) -> None:
        # Un equipo se alquila entre 1 y 72 horas
        _validar_numero(duracion, "Duración de alquiler", 1, 72)

    def costo_base(self, duracion: float) -> float:
        # Tarifa por horas más el seguro fijo
        return self._tarifa_hora * duracion + self.SEGURO

    def describir(self) -> str:
        return (f"Equipo '{self._nombre}' tipo {self._tipo_equipo} - "
                f"${self._tarifa_hora:,.0f}/h + seguro ${self.SEGURO:,.0f}")


class Asesoria(Servicio):
    """Asesoría especializada; la tarifa sube según la especialidad."""

    RECARGOS = {"basica": 1.0, "senior": 1.5, "experto": 2.0}  # Multiplicadores

    def __init__(self, nombre=None, tarifa_hora=None, nivel: str = "basica"):
        super().__init__(nombre, tarifa_hora)
        if nivel not in self.RECARGOS:
            raise ServicioInvalidoError("Nivel de asesoría inválido", repr(nivel))
        self._nivel = nivel

    def validar_parametros(self, duracion: float) -> None:
        # Una asesoría dura entre 0.5 y 6 horas
        _validar_numero(duracion, "Duración de asesoría", 0.5, 6)

    def costo_base(self, duracion: float) -> float:
        # La tarifa se multiplica por el recargo del nivel
        return self._tarifa_hora * self.RECARGOS[self._nivel] * duracion

    def describir(self) -> str:
        return (f"Asesoría '{self._nombre}' nivel {self._nivel} - "
                f"${self._tarifa_hora:,.0f}/h x{self.RECARGOS[self._nivel]}")
