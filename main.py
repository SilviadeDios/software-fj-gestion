"""Simulación de 20 operaciones del sistema Software FJ (sin base de datos)."""

from softwarefj.cliente import Cliente
from softwarefj.excepciones import SoftwareFJError
from softwarefj.logger import ARCHIVO_LOG, log
from softwarefj.reserva import Reserva
from softwarefj.servicios import AlquilerEquipo, Asesoria, ReservaSala

# Listas internas que reemplazan a una base de datos
clientes, servicios, reservas = [], [], []


def ejecutar(numero: int, titulo: str, accion):
    """Ejecuta una operación; ante cualquier error lo registra y continúa."""
    print(f"\n[{numero:02d}] {titulo}")
    try:
        resultado = accion()
    except SoftwareFJError as e:
        # Error controlado del dominio (se muestra la causa encadenada si existe)
        causa = f" <- causa: {e.__cause__}" if e.__cause__ else ""
        print(f"   ERROR controlado: {e}{causa}")
        log.error("Operación %02d '%s' falló: %s%s", numero, titulo, e, causa)
    except Exception as e:  # Error inesperado: el sistema tampoco se detiene
        print(f"   ERROR inesperado: {type(e).__name__}: {e}")
        log.exception("Operación %02d '%s' error inesperado", numero, titulo)
    else:
        print(f"   OK -> {resultado}")
        log.info("Operación %02d '%s' exitosa", numero, titulo)
        return resultado
    finally:
        log.debug("Operación %02d finalizada", numero)


def registrar_cliente(*args):
    c = Cliente(*args)
    clientes.append(c)
    return c


def registrar_servicio(clase, *args, **kw):
    s = clase(*args, **kw)
    servicios.append(s)
    return s


def reservar(cliente, servicio, duracion):
    r = Reserva(cliente, servicio, duracion)
    reservas.append(r)
    return r


def main():
    log.info("===== INICIO DE LA SIMULACIÓN =====")
    # 1-3 Clientes (válido, inválido por correo, inválido por parámetro faltante)
    ana = ejecutar(1, "Cliente válido", lambda: registrar_cliente(
        "ana maría gómez", "1012345678", "ana@correo.com", "3101234567"))
    ejecutar(2, "Cliente con correo inválido", lambda: registrar_cliente(
        "Luis Pérez", "87654321", "luis-correo", "3207654321"))
    ejecutar(3, "Cliente con parámetro faltante", lambda: registrar_cliente(
        "Carlos Ruiz", "11223344"))
    luis = ejecutar(4, "Segundo cliente válido", lambda: registrar_cliente(
        "Luis Pérez", "87654321", "luis@correo.com", "3207654321"))
    # 5-7 Servicios (válidos e inválido)
    sala = ejecutar(5, "Sala válida", lambda: registrar_servicio(
        ReservaSala, "Sala Innovación", 50000, capacidad=12))
    ejecutar(6, "Servicio con tarifa inválida", lambda: registrar_servicio(
        AlquilerEquipo, "Portátil Pro", -100))
    equipo = ejecutar(7, "Alquiler de equipo válido", lambda: registrar_servicio(
        AlquilerEquipo, "Portátil Pro", 8000, tipo_equipo="Portátil"))
    asesoria = ejecutar(8, "Asesoría válida", lambda: registrar_servicio(
        Asesoria, "Arquitectura de software", 90000, nivel="experto"))
    # 9-10 Reservas fallidas
    ejecutar(9, "Reserva con duración fuera de rango (sala 20h)",
             lambda: reservar(ana, sala, 20))
    ejecutar(10, "Reserva con cliente inexistente", lambda: reservar(None, sala, 2))
    # 11 Servicio no disponible
    equipo.cambiar_disponibilidad(False)
    ejecutar(11, "Reserva de servicio no disponible", lambda: reservar(luis, equipo, 5))
    equipo.cambiar_disponibilidad(True)
    # 12-14 Reservas exitosas
    r1 = ejecutar(12, "Reserva de sala exitosa", lambda: reservar(ana, sala, 3))
    r2 = ejecutar(13, "Reserva de asesoría exitosa", lambda: reservar(luis, asesoria, 2))
    r3 = ejecutar(14, "Reserva de equipo exitosa", lambda: reservar(ana, equipo, 24))
    # 15-19 Ciclo de vida: confirmar, procesar, errores de estado, cancelar
    ejecutar(15, "Procesar reserva sin confirmar (error)", lambda: r1.procesar())
    ejecutar(16, "Confirmar reserva", lambda: (r1.confirmar(), r1)[1])
    ejecutar(17, "Procesar con IVA 19%", lambda: (r1.procesar(), r1)[1])
    ejecutar(18, "Procesar con descuento inválido (150%)",
             lambda: (r2.confirmar(), r2.procesar(descuento=1.5))[1])
    ejecutar(19, "Cancelar reserva y reintentar cancelar", lambda: (
        r3.cancelar(), r3.cancelar())[1])
    # 20 Sobrecarga de métodos (cotizar con 1, 2 y 3 argumentos)
    ejecutar(20, "Cotizaciones sobrecargadas de asesoría (2h)", lambda: (
        asesoria.cotizar(2), asesoria.cotizar(2, 0.19), asesoria.cotizar(2, 0.19, 0.1)))
    # Resumen polimórfico
    print("\n" + "=" * 60 + "\nRESUMEN")
    for entidad in (*clientes, *servicios, *reservas):
        print(" ", entidad.describir())  # Polimorfismo: cada clase se describe sola
    print(f"\nEl sistema terminó sin caerse. Log en: {ARCHIVO_LOG}")
    log.info("===== FIN DE LA SIMULACIÓN =====")


if __name__ == "__main__":
    main()
