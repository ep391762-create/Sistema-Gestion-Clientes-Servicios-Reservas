"""
Módulo de excepciones personalizadas del sistema.
Permite controlar errores relacionados con clientes,
servicios y reservas.
"""


class SistemaError(Exception):
    """Excepción base para los errores del sistema."""


class ValidacionError(SistemaError):
    """Se produce cuando un dato no cumple las validaciones."""


class ClienteError(SistemaError):
    """Se produce cuando ocurre un error relacionado con un cliente."""


class ServicioError(SistemaError):
    """Se produce cuando ocurre un error relacionado con un servicio."""


class ReservaError(SistemaError):
    """Se produce cuando ocurre un error relacionado con una reserva."""


class ParametroFaltanteError(SistemaError):
    """Se produce cuando falta un parámetro obligatorio."""


class RecursoNoDisponibleError(SistemaError):
    """Se produce cuando un servicio o recurso no está disponible."""


class OperacionNoPermitidaError(SistemaError):
    """Se produce cuando se intenta realizar una operación no permitida."""