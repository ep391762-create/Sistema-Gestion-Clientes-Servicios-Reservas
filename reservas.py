
"""
Módulo de gestión de reservas.
Administra clientes, servicios, fechas, costos y estados.
"""

from datetime import datetime, timedelta
from uuid import uuid4

from excepciones import (
    ValidacionError,
    ReservaError,
    OperacionNoPermitidaError
)


class Reserva:
    """Representa una reserva realizada por un cliente."""

    ESTADOS_VALIDOS = (
        "Pendiente",
        "Confirmada",
        "Cancelada",
        "Finalizada"
    )

    def __init__(
        self,
        cliente,
        servicio,
        duracion,
        fecha_inicio=None,
        parametros_servicio=None
    ):
        """Inicializa una reserva y valida sus datos."""

        from clientes import Cliente
        from servicios import Servicio

        if not isinstance(cliente, Cliente):
            raise ValidacionError(
                "La reserva requiere un cliente válido."
            )

        if not isinstance(servicio, Servicio):
            raise ValidacionError(
                "La reserva requiere un servicio válido."
            )

        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or duracion <= 0
        ):
            raise ValidacionError(
                "La duración debe ser mayor que cero."
            )

        if not cliente.activo:
            raise ReservaError(
                "No se puede reservar con un cliente inactivo."
            )

        servicio.validar()

        if fecha_inicio is None:
            fecha_inicio = datetime.now()

        if not isinstance(fecha_inicio, datetime):
            raise ValidacionError(
                "La fecha de inicio debe ser un objeto datetime."
            )

        self._parametros_servicio = parametros_servicio or {}

        servicio.validar_parametros(**self._parametros_servicio)

        self._identificador = str(uuid4())
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = float(duracion)
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = fecha_inicio + timedelta(
            hours=self._duracion
        )
        self._estado = "Pendiente"
        self._fecha_creacion = datetime.now()
        self._costo = servicio.calcular_costo(self._duracion)

    @property
    def identificador(self):
        return self._identificador

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def fecha_inicio(self):
        return self._fecha_inicio

    @property
    def fecha_fin(self):
        return self._fecha_fin

    @property
    def estado(self):
        return self._estado

    @property
    def costo(self):
        return self._costo

    def confirmar(self):
        """Confirma una reserva pendiente."""
        if self._estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solamente se pueden confirmar reservas pendientes."
            )

        self._servicio.validar()
        self._estado = "Confirmada"

        return True

    def cancelar(self, motivo="Sin especificar"):
        """Cancela una reserva pendiente o confirmada."""
        if self._estado not in ("Pendiente", "Confirmada"):
            raise OperacionNoPermitidaError(
                "No se puede cancelar una reserva finalizada o cancelada."
            )

        if not isinstance(motivo, str) or not motivo.strip():
            raise ValidacionError(
                "Debe proporcionar un motivo de cancelación."
            )

        self._estado = "Cancelada"
        self._motivo_cancelacion = motivo.strip()

        return True

    def finalizar(self):
        """Finaliza una reserva confirmada."""
        if self._estado != "Confirmada":
            raise OperacionNoPermitidaError(
                "Solamente se pueden finalizar reservas confirmadas."
            )

        self._estado = "Finalizada"

        return True

    def calcular_costo(
        self,
        impuesto=0,
        descuento=0
    ):
        """Calcula el costo actualizado de la reserva."""
        self._costo = self._servicio.calcular_costo(
            self._duracion,
            impuesto,
            descuento
        )

        return self._costo

    def validar(self):
        """Comprueba la coherencia de la reserva."""
        if self._duracion <= 0:
            raise ReservaError(
                "La duración de la reserva no es válida."
            )

        if self._estado not in self.ESTADOS_VALIDOS:
            raise ReservaError(
                "El estado de la reserva no es válido."
            )

        return True

    def obtener_informacion(self):
        """Devuelve toda la información de la reserva."""
        informacion = {
            "identificador": self.identificador,
            "cliente": self.cliente.nombre,
            "correo": self.cliente.correo,
            "servicio": self.servicio.nombre,
            "duracion_horas": self.duracion,
            "fecha_inicio": self.fecha_inicio.strftime(
                "%Y-%m-%d %H:%M"
            ),
            "fecha_fin": self.fecha_fin.strftime(
                "%Y-%m-%d %H:%M"
            ),
            "estado": self.estado,
            "costo": self.costo,
            "fecha_creacion": self._fecha_creacion.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        if hasattr(self, "_motivo_cancelacion"):
            informacion["motivo_cancelacion"] = (
                self._motivo_cancelacion
            )

        return informacion

    def __str__(self):
        """Representación textual de la reserva."""
        return (
            f"Reserva {self.identificador[:8]} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Estado: {self.estado} | "
            f"Costo: ${self.costo:.2f}"
        )
