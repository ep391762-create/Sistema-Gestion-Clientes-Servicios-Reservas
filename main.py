"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas.

Archivo principal:
Coordina los módulos, ejecuta operaciones y realiza pruebas.
"""

import logging
from pathlib import Path

from clientes import Cliente
from servicios import (
    ReservaSala,
    AlquilerEquipos,
    AsesoriaEspecializada
)
from reservas import Reserva
from excepciones import SistemaError


# =====================================================
# CONFIGURACIÓN DEL SISTEMA DE REGISTROS
# =====================================================

CARPETA_LOGS = Path(__file__).parent / "logs"
CARPETA_LOGS.mkdir(exist_ok=True)

ARCHIVO_LOG = CARPETA_LOGS / "sistema.log"

logging.basicConfig(
    filename=ARCHIVO_LOG,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
    force=True
)

logger = logging.getLogger(__name__)


# =====================================================
# FUNCIÓN PARA EJECUTAR Y CONTROLAR OPERACIONES
# =====================================================

def ejecutar_prueba(numero, descripcion, operacion):
    """
    Ejecuta una operación utilizando manejo de excepciones.
    """

    print(f"\nPRUEBA {numero}: {descripcion}")

    try:
        resultado = operacion()

    except SistemaError as error:
        print(f"ERROR CONTROLADO: {error}")
        logger.warning(
            "Prueba %s: %s | %s",
            numero,
            descripcion,
            error
        )

    except (TypeError, ValueError) as error:
        print(f"ERROR DE DATOS: {error}")
        logger.error(
            "Prueba %s: %s | %s",
            numero,
            descripcion,
            error
        )

    except Exception as error:
        print(f"ERROR INESPERADO: {error}")
        logger.exception(
            "Prueba %s: %s",
            numero,
            descripcion
        )

    else:
        print(f"OPERACIÓN EXITOSA: {resultado}")
        logger.info(
            "Prueba %s: %s | Operación exitosa",
            numero,
            descripcion
        )

    finally:
        print(f"Finalización de la prueba {numero}.")


# =====================================================
# OPERACIONES DEL SISTEMA
# =====================================================

def crear_cliente_valido():
    """Registra un cliente con información correcta."""

    cliente = Cliente(
        "Carlos Ramirez",
        "carlos@gmail.com",
        "3101234567"
    )

    sistema["clientes"].append(cliente)

    return cliente


def crear_cliente_invalido():
    """Intenta registrar un cliente con correo incorrecto."""

    return Cliente(
        "Maria Lopez",
        "correo_incorrecto",
        "3101234567"
    )


def crear_servicios():
    """Registra los tres servicios especializados."""

    sala = ReservaSala(
        "Sala de reuniones",
        "Espacio para reuniones empresariales",
        50000,
        capacidad=20
    )

    equipos = AlquilerEquipos(
        "Computadores portátiles",
        "Alquiler de equipos tecnológicos",
        30000,
        unidades_disponibles=5
    )

    asesoria = AsesoriaEspecializada(
        "Asesoría tecnológica",
        "Consultoría profesional en tecnología",
        80000,
        especialidad="Sistemas"
    )

    sistema["servicios"] = [sala, equipos, asesoria]

    return "Tres servicios registrados correctamente."


def validar_sala():
    """Valida una reserva de sala."""

    sala = sistema["servicios"][0]

    return sala.validar_parametros(personas=10)


def crear_reserva():
    """Crea una reserva válida."""

    cliente = sistema["clientes"][0]
    sala = sistema["servicios"][0]

    reserva = Reserva(
        cliente,
        sala,
        duracion=2,
        parametros_servicio={"personas": 10}
    )

    sistema["reservas"].append(reserva)

    return reserva


def confirmar_reserva():
    """Confirma la primera reserva."""

    reserva = sistema["reservas"][0]

    return reserva.confirmar()


def calcular_costo():
    """Calcula el costo con impuesto y descuento."""

    reserva = sistema["reservas"][0]

    return reserva.calcular_costo(
        impuesto=19,
        descuento=10
    )


def validar_alquiler_invalido():
    """Intenta alquilar más equipos de los disponibles."""

    equipos = sistema["servicios"][1]

    return equipos.validar_parametros(cantidad=10)


def cancelar_reserva():
    """Cancela una reserva confirmada."""

    reserva = sistema["reservas"][0]

    return reserva.cancelar("Solicitud del cliente")


def finalizar_reserva_invalida():
    """Intenta finalizar una reserva cancelada."""

    reserva = sistema["reservas"][0]

    return reserva.finalizar()


def consultar_reserva():
    """Consulta la información de una reserva."""

    reserva = sistema["reservas"][0]

    return reserva.obtener_informacion()


# =====================================================
# DEMOSTRACIÓN DE POLIMORFISMO
# =====================================================

def demostrar_polimorfismo():
    """
    Ejecuta los mismos métodos sobre diferentes servicios.
    """

    print("\n========== PRUEBA DE POLIMORFISMO ==========")

    for servicio in sistema["servicios"]:

        print("\nServicio:", servicio.describir_servicio())

        costo = servicio.calcular_costo(
            duracion=2,
            impuesto=19,
            descuento=5
        )

        print(f"Costo por dos horas: ${costo:,.2f}")

        logger.info(
            "Polimorfismo ejecutado para el servicio: %s",
            servicio.nombre
        )

    print("\n========== POLIMORFISMO COMPLETADO ==========")


# =====================================================
# FUNCIÓN PRINCIPAL
# =====================================================

def main():
    """Ejecuta las operaciones y pruebas del sistema."""

    sistema["clientes"] = []
    sistema["servicios"] = []
    sistema["reservas"] = []

    print("=" * 55)
    print(" SISTEMA INTEGRAL DE GESTIÓN")
    print(" CLIENTES, SERVICIOS Y RESERVAS")
    print("=" * 55)

    logger.info("Inicio de ejecución del sistema.")

    ejecutar_prueba(
        1,
        "Registro de un cliente válido",
        crear_cliente_valido
    )

    ejecutar_prueba(
        2,
        "Registro de un cliente con correo incorrecto",
        crear_cliente_invalido
    )

    ejecutar_prueba(
        3,
        "Registro de tres servicios especializados",
        crear_servicios
    )

    ejecutar_prueba(
        4,
        "Validación de capacidad de una sala",
        validar_sala
    )

    ejecutar_prueba(
        5,
        "Creación de una reserva válida",
        crear_reserva
    )

    ejecutar_prueba(
        6,
        "Confirmación de una reserva",
        confirmar_reserva
    )

    ejecutar_prueba(
        7,
        "Cálculo de costo con impuesto y descuento",
        calcular_costo
    )

    ejecutar_prueba(
        8,
        "Alquiler de equipos con cantidad no disponible",
        validar_alquiler_invalido
    )

    ejecutar_prueba(
        9,
        "Cancelación de una reserva",
        cancelar_reserva
    )

    ejecutar_prueba(
        10,
        "Intento de finalizar una reserva cancelada",
        finalizar_reserva_invalida
    )

    # Demostración adicional de polimorfismo.
    ejecutar_prueba(
        11,
        "Demostración de polimorfismo entre servicios",
        demostrar_polimorfismo
    )

    # Consulta adicional de información.
    ejecutar_prueba(
        12,
        "Consulta de información de una reserva",
        consultar_reserva
    )

    print("\n" + "=" * 55)
    print(" PRUEBAS DEL SISTEMA FINALIZADAS")
    print(" Total de operaciones: 12")
    print(f" Archivo de registros: {ARCHIVO_LOG}")
    print("=" * 55)

    logger.info("Finalización de ejecución del sistema.")


# Diccionario para almacenar los objetos del sistema.
sistema = {
    "clientes": [],
    "servicios": [],
    "reservas": []
}


if __name__ == "__main__":
    main()