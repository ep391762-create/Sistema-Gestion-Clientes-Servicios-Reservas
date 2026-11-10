
"""
Módulo de gestión de servicios.
Implementa una clase abstracta y tres servicios especializados.
"""

from abc import abstractmethod

from entidades import EntidadSistema
from excepciones import (
    ValidacionError,
    ServicioError,
    RecursoNoDisponibleError
)


class Servicio(EntidadSistema):
    """
    Clase abstracta que representa un servicio general.
    """

    def __init__(self, nombre, descripcion, precio_base):
        super().__init__()

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValidacionError("El nombre del servicio es obligatorio.")

        if not isinstance(descripcion, str) or not descripcion.strip():
            raise ValidacionError("La descripción es obligatoria.")

        if (
            isinstance(precio_base, bool)
            or not isinstance(precio_base, (int, float))
            or precio_base <= 0
        ):
            raise ValidacionError("El precio base debe ser mayor que cero.")

        self._nombre = nombre.strip()
        self._descripcion = descripcion.strip()
        self._precio_base = float(precio_base)
        self._disponible = True

    @property
    def nombre(self):
        return self._nombre

    @property
    def descripcion(self):
        return self._descripcion

    @property
    def precio_base(self):
        return self._precio_base

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, disponible):
        """Modifica la disponibilidad del servicio."""
        if not isinstance(disponible, bool):
            raise ValidacionError(
                "La disponibilidad debe ser verdadera o falsa."
            )

        self._disponible = disponible

    def validar(self):
        """Comprueba que el servicio esté correctamente configurado."""
        if not self._activo:
            raise ServicioError("El servicio se encuentra inactivo.")

        if not self._disponible:
            raise RecursoNoDisponibleError(
                f"El servicio {self.nombre} no está disponible."
            )

        return True

    def _validar_parametros_costo(
        self, duracion, impuesto=0, descuento=0
    ):
        """Valida los parámetros utilizados para calcular costos."""
        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or duracion <= 0
        ):
            raise ValidacionError(
                "La duración debe ser un número mayor que cero."
            )

        if (
            isinstance(impuesto, bool)
            or not isinstance(impuesto, (int, float))
            or not 0 <= impuesto <= 100
        ):
            raise ValidacionError(
                "El impuesto debe estar entre 0 y 100."
            )

        if (
            isinstance(descuento, bool)
            or not isinstance(descuento, (int, float))
            or not 0 <= descuento <= 100
        ):
            raise ValidacionError(
                "El descuento debe estar entre 0 y 100."
            )

    def _calcular_total(self, costo, impuesto=0, descuento=0):
        """Calcula el costo final aplicando impuesto y descuento."""
        subtotal = costo * (1 - descuento / 100)
        total = subtotal * (1 + impuesto / 100)
        return round(total, 2)

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        """Calcula el costo del servicio."""
        pass

    @abstractmethod
    def describir_servicio(self):
        """Describe las características del servicio."""
        pass

    @abstractmethod
    def validar_parametros(self, **parametros):
        """Valida los parámetros específicos del servicio."""
        pass

    def obtener_informacion(self):
        """Devuelve la información general del servicio."""
        return {
            "identificador": self.identificador,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio_base": self.precio_base,
            "disponible": self.disponible,
            "activo": self.activo
        }


class ReservaSala(Servicio):
    """Servicio especializado de reserva de salas."""

    def __init__(
        self, nombre, descripcion, precio_base, capacidad=10
    ):
        super().__init__(nombre, descripcion, precio_base)

        self._capacidad = self._validar_capacidad(capacidad)

    @staticmethod
    def _validar_capacidad(capacidad):
        if (
            isinstance(capacidad, bool)
            or not isinstance(capacidad, int)
            or capacidad <= 0
        ):
            raise ValidacionError(
                "La capacidad debe ser un entero mayor que cero."
            )

        return capacidad

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        self.validar()
        self._validar_parametros_costo(
            duracion, impuesto, descuento
        )

        costo = self.precio_base * duracion
        return self._calcular_total(costo, impuesto, descuento)

    def describir_servicio(self):
        return (
            f"Sala: {self.nombre}. "
            f"Capacidad máxima: {self._capacidad} personas."
        )

    def validar_parametros(self, **parametros):
        personas = parametros.get("personas")

        if (
            isinstance(personas, bool)
            or not isinstance(personas, int)
            or personas <= 0
        ):
            raise ValidacionError(
                "Debe indicar una cantidad válida de personas."
            )

        if personas > self._capacidad:
            raise ValidacionError(
                "La cantidad de personas supera la capacidad de la sala."
            )

        return True


class AlquilerEquipos(Servicio):
    """Servicio especializado de alquiler de equipos tecnológicos."""

    def __init__(
        self, nombre, descripcion, precio_base, unidades_disponibles=1
    ):
        super().__init__(nombre, descripcion, precio_base)

        self._unidades_disponibles = self._validar_unidades(
            unidades_disponibles
        )
    @staticmethod
    def _validar_unidades(unidades):
        if (
            isinstance(unidades, bool)
            or not isinstance(unidades, int)
            or unidades < 0
        ):
            raise ValidacionError(
                "Las unidades disponibles deben ser un entero no negativo."
            )
        return unidades

    def calcular_costo(self, duracion, cantidad=1, impuesto=0, descuento=0):
        self.validar()
        self._validar_parametros_costo(duracion, impuesto, descuento)
        self.validar_parametros(cantidad=cantidad)

        costo = self.precio_base * duracion * cantidad
        return self._calcular_total(costo, impuesto, descuento)
    
    def describir_servicio(self):
        return (
            f"Alquiler de equipos: {self.nombre}. "
            f"Unidades disponibles: {self._unidades_disponibles}."
        )

    def validar_parametros(self, **parametros):
        cantidad = parametros.get("cantidad")

        if (
            isinstance(cantidad, bool)
            or not isinstance(cantidad, int)
            or cantidad <= 0
        ):
            raise ValidacionError(
                "La cantidad de equipos debe ser mayor que cero."
            )

        if cantidad > self._unidades_disponibles:
            raise RecursoNoDisponibleError(
                "No hay suficientes equipos disponibles."
            )

        return True


class AsesoriaEspecializada(Servicio):
    """Servicio especializado de asesoría profesional."""

    def __init__(
        self, nombre, descripcion, precio_base, especialidad="General"
    ):
        super().__init__(nombre, descripcion, precio_base)

        if (
            not isinstance(especialidad, str)
            or not especialidad.strip()
        ):
            raise ValidacionError(
                "La especialidad de la asesoría es obligatoria."
            )

        self._especialidad = especialidad.strip()

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        self.validar()
        self._validar_parametros_costo(
            duracion, impuesto, descuento
        )

        costo = self.precio_base * duracion
        return self._calcular_total(costo, impuesto, descuento)

    def describir_servicio(self):
        return (
            f"Asesoría: {self.nombre}. "
            f"Especialidad: {self._especialidad}."
        )

    def validar_parametros(self, **parametros):
        modalidad = parametros.get("modalidad")

        modalidades_validas = (
            "presencial",
            "virtual"
        )

        if (
            not isinstance(modalidad, str)
            or modalidad.strip().lower() not in modalidades_validas
        ):
            raise ValidacionError(
                "La modalidad debe ser presencial o virtual."
            )

        return True
