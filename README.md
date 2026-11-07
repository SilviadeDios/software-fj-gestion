# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto de la **Fase 4 – Programación (213023), UNAD**. Aplicación orientada a objetos
en Python, **sin base de datos**: todo se maneja con objetos y listas, y solo se usan
archivos para el registro de eventos y errores (`logs/software_fj.log`).

## Requisitos
Python 3.8 o superior. No requiere librerías externas.

## Ejecución
```bash
python main.py
```
Simula 20 operaciones (válidas e inválidas) y el programa nunca se detiene por un error.

## Estructura
| Archivo | Contenido |
|---|---|
| `softwarefj/excepciones.py` | Excepciones personalizadas (`SoftwareFJError` y 7 derivadas) |
| `softwarefj/logger.py` | Configuración del archivo de logs |
| `softwarefj/entidad.py` | Clase abstracta `Entidad` |
| `softwarefj/cliente.py` | `Cliente` con encapsulación y validaciones |
| `softwarefj/servicio.py` | Clase abstracta `Servicio` + métodos sobrecargados |
| `softwarefj/servicios.py` | `ReservaSala`, `AlquilerEquipo`, `Asesoria` |
| `softwarefj/reserva.py` | `Reserva`: confirmar, cancelar, procesar |
| `main.py` | Simulación de 20 operaciones |
| `logs/software_fj.log` | Registro de eventos y errores |

## Conceptos aplicados
- **Abstracción:** `Entidad` y `Servicio` son clases abstractas (`ABC`).
- **Herencia y polimorfismo:** tres servicios sobrescriben `costo_base`, `validar_parametros` y `describir`.
- **Encapsulación:** atributos privados con `@property` y validación en los setters.
- **Sobrecarga:** Python no la trae nativa; se simula con parámetros opcionales (`calcular_costo`) y `*args` (`cotizar`).
- **Excepciones:** personalizadas, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento (`raise ... from`).

## Autoras
- Parte A (base: excepciones, logs, entidad, cliente, servicio abstracto): _nombre estudiante 1_
- Parte B (servicios, reserva, simulación): _nombre estudiante 2_
