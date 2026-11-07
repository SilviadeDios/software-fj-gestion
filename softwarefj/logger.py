"""Configuración centralizada del archivo de logs (eventos y errores)."""

import logging  # Módulo estándar de registro de eventos
from pathlib import Path  # Manejo de rutas independiente del sistema operativo

# Carpeta logs/ ubicada en la raíz del proyecto (un nivel arriba de este archivo)
RUTA_LOGS = Path(__file__).resolve().parent.parent / "logs"
# Archivo donde se guardan todos los eventos y errores
ARCHIVO_LOG = RUTA_LOGS / "software_fj.log"


def obtener_logger(nombre: str = "software_fj") -> logging.Logger:
    """Devuelve un logger único que escribe en logs/software_fj.log."""
    # Se crea la carpeta de logs si todavía no existe
    RUTA_LOGS.mkdir(parents=True, exist_ok=True)
    # Se obtiene (o crea) el logger con el nombre indicado
    logger = logging.getLogger(nombre)
    # Si ya tiene manejadores, no se duplican (evita líneas repetidas en el log)
    if logger.handlers:
        return logger
    # Nivel mínimo: se registra desde DEBUG hacia arriba
    logger.setLevel(logging.DEBUG)
    # Formato de cada línea: fecha, nivel y mensaje
    formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
    # Manejador que escribe en archivo con codificación UTF-8
    manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
    # Se asigna el formato al manejador
    manejador.setFormatter(formato)
    # Se agrega el manejador al logger
    logger.addHandler(manejador)
    # Evita que los mensajes suban al logger raíz y salgan duplicados
    logger.propagate = False
    return logger


# Logger compartido que importan los demás módulos
log = obtener_logger()
