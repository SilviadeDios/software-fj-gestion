"""Excepciones personalizadas del sistema Software FJ.

Todas heredan de SoftwareFJError, de modo que el sistema pueda capturar
cualquier error propio con un solo bloque ``except SoftwareFJError``.
"""


class SoftwareFJError(Exception):
    """Excepción base de la que heredan todos los errores del sistema."""

    def __init__(self, mensaje: str, detalle: str = ""):
        # Se guarda el mensaje principal en la clase base de Python
        super().__init__(mensaje)
        # Se guarda un detalle opcional para el registro en el log
        self.detalle = detalle

    def __str__(self) -> str:
        # Si hay detalle, se muestra junto al mensaje principal
        base = super().__str__()
        return f"{base} ({self.detalle})" if self.detalle else base


class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un cliente no cumplen las validaciones."""


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un parámetro obligatorio."""


class ServicioInvalidoError(SoftwareFJError):
    """Se lanza cuando los parámetros de un servicio son inválidos."""


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta reservar un servicio no disponible."""


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva se crea con datos incorrectos."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se pide una operación no válida para el estado actual."""


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un cálculo de costos produce un resultado inválido."""
