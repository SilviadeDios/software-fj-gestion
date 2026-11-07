"""Clase Reserva: integra cliente, servicio, duración y estado."""

from .cliente import Cliente
from .entidad import Entidad
from .excepciones import (OperacionNoPermitidaError, ReservaInvalidaError,
                          ServicioNoDisponibleError, SoftwareFJError)
from .logger import log
from .servicio import Servicio

# Estados posibles de una reserva
PENDIENTE, CONFIRMADA, CANCELADA, PROCESADA = (
    "PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA")


class Reserva(Entidad):
    """Reserva de un servicio por un cliente durante cierta duración."""

    IVA = 0.19  # Impuesto aplicado al procesar

    def __init__(self, cliente: Cliente, servicio: Servicio, duracion: float):
        super().__init__()
        # Validación de tipos de los participantes
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("Cliente inválido", repr(cliente))
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Servicio inválido", repr(servicio))
        # El servicio debe estar disponible
        if not servicio.disponible:
            raise ServicioNoDisponibleError("Servicio no disponible", servicio.nombre)
        # Se valida la duración con las reglas propias del servicio;
        # si falla, se encadena la causa original con "raise ... from"
        try:
            servicio.validar_parametros(duracion)
        except SoftwareFJError as causa:
            raise ReservaInvalidaError("Duración inválida para la reserva",
                                       str(causa)) from causa
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = PENDIENTE
        self._total = None  # Se calcula al procesar
        log.info("Reserva creada: id=%s cliente=%s servicio=%s duración=%s",
                 self.id, cliente.nombre, servicio.nombre, duracion)

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def total(self):
        return self._total

    def confirmar(self) -> None:
        """PENDIENTE -> CONFIRMADA."""
        if self._estado != PENDIENTE:
            raise OperacionNoPermitidaError("Solo se confirma una reserva pendiente",
                                            f"estado actual: {self._estado}")
        self._estado = CONFIRMADA
        log.info("Reserva %s confirmada", self.id)

    def cancelar(self) -> None:
        """Cancela una reserva que no esté ya cancelada o procesada."""
        if self._estado in (CANCELADA, PROCESADA):
            raise OperacionNoPermitidaError("No se puede cancelar",
                                            f"estado actual: {self._estado}")
        self._estado = CANCELADA
        log.warning("Reserva %s cancelada", self.id)

    def procesar(self, descuento: float = 0.0) -> float:
        """CONFIRMADA -> PROCESADA, calculando el total con IVA y descuento.

        Usa try/except/else/finally y encadenamiento de excepciones.
        """
        try:
            if self._estado != CONFIRMADA:
                raise OperacionNoPermitidaError("Solo se procesa una reserva confirmada",
                                                f"estado actual: {self._estado}")
            total = self._servicio.calcular_costo(self._duracion, self.IVA, descuento)
        except SoftwareFJError as error:
            # Se registra y se vuelve a lanzar encadenada con contexto adicional
            log.error("Fallo al procesar reserva %s: %s", self.id, error)
            raise ReservaInvalidaError("No fue posible procesar la reserva",
                                       str(error)) from error
        else:
            # Solo se ejecuta si no hubo excepción
            self._total = total
            self._estado = PROCESADA
            log.info("Reserva %s procesada. Total=$%s", self.id, f"{total:,.2f}")
            return total
        finally:
            # Se ejecuta siempre, haya o no error
            log.debug("Fin de procesamiento de reserva %s (estado=%s)",
                      self.id, self._estado)

    def describir(self) -> str:
        total = f"${self._total:,.2f}" if self._total is not None else "sin calcular"
        return (f"Reserva #{self.id} [{self._estado}] {self._cliente.nombre} -> "
                f"{self._servicio.nombre} x {self._duracion}h | Total: {total}")
