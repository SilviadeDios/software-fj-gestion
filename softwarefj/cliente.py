"""Clase Cliente con encapsulación y validaciones robustas."""

import re  # Expresiones regulares para validar formatos

from .entidad import Entidad
from .excepciones import ClienteInvalidoError, ParametroFaltanteError
from .logger import log

# Patrón sencillo para correos: texto@dominio.ext
_PATRON_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")


class Cliente(Entidad):
    """Cliente de Software FJ. Sus datos personales son privados."""

    def __init__(self, nombre: str = None, documento: str = None,
                 email: str = None, telefono: str = None):
        super().__init__()  # Genera el id único de la entidad
        # Parámetros obligatorios: si falta alguno se lanza un error propio
        faltantes = [n for n, v in (("nombre", nombre), ("documento", documento),
                                    ("email", email), ("telefono", telefono))
                     if v is None]
        if faltantes:
            raise ParametroFaltanteError("Faltan datos del cliente",
                                         ", ".join(faltantes))
        # Cada asignación pasa por su setter, que valida el dato
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono
        # Se deja constancia del evento en el log
        log.info("Cliente creado: id=%s nombre=%s", self.id, self._nombre)

    # ---- nombre ----
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        # Debe ser texto con al menos 3 caracteres y sin números
        if not isinstance(valor, str) or len(valor.strip()) < 3 \
                or any(c.isdigit() for c in valor):
            raise ClienteInvalidoError("Nombre inválido", repr(valor))
        self._nombre = valor.strip().title()

    # ---- documento ----
    @property
    def documento(self) -> str:
        return self._documento

    @documento.setter
    def documento(self, valor: str):
        # Solo dígitos, entre 6 y 12 caracteres
        if not isinstance(valor, str) or not valor.isdigit() \
                or not 6 <= len(valor) <= 12:
            raise ClienteInvalidoError("Documento inválido", repr(valor))
        self._documento = valor

    # ---- email ----
    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        # Debe cumplir el patrón de correo electrónico
        if not isinstance(valor, str) or not _PATRON_EMAIL.match(valor):
            raise ClienteInvalidoError("Correo inválido", repr(valor))
        self._email = valor.lower()

    # ---- teléfono ----
    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        # Exactamente 10 dígitos (formato celular colombiano)
        if not isinstance(valor, str) or not valor.isdigit() or len(valor) != 10:
            raise ClienteInvalidoError("Teléfono inválido", repr(valor))
        self._telefono = valor

    def describir(self) -> str:
        """Implementación del método abstracto de Entidad."""
        return (f"Cliente #{self.id}: {self._nombre} | Doc: {self._documento} | "
                f"{self._email} | Tel: {self._telefono}")
