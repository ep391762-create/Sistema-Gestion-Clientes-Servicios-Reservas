"""
Módulo de gestión de clientes.
Implementa la clase Cliente con validaciones y encapsulamiento.
"""

import re

from entidades import EntidadSistema
from excepciones import ValidacionError, ClienteError


class Cliente(EntidadSistema):
    """
    Representa un cliente registrado en el sistema.
    """

    def __init__(self, nombre, correo, telefono):
        """Inicializa un cliente y valida sus datos."""
        super().__init__()

        self._nombre = self._validar_nombre(nombre)
        self._correo = self._validar_correo(correo)
        self._telefono = self._validar_telefono(telefono)

    @staticmethod
    def _validar_nombre(nombre):
        """Comprueba que el nombre sea válido."""
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValidacionError("El nombre es obligatorio.")

        nombre = nombre.strip()

        if len(nombre) < 3 or len(nombre) > 80:
            raise ValidacionError(
                "El nombre debe tener entre 3 y 80 caracteres."
            )

        if not all(
            caracter.isalpha() or caracter.isspace()
            or caracter in "-'"
            for caracter in nombre
        ):
            raise ValidacionError(
                "El nombre contiene caracteres no permitidos."
            )

        return nombre

    @staticmethod
    def _validar_correo(correo):
        """Comprueba que el correo tenga un formato válido."""
        if not isinstance(correo, str) or not correo.strip():
            raise ValidacionError("El correo electrónico es obligatorio.")

        correo = correo.strip().lower()

        patron = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

        if not re.fullmatch(patron, correo):
            raise ValidacionError("El correo electrónico no es válido.")

        return correo

    @staticmethod
    def _validar_telefono(telefono):
        """Comprueba que el teléfono contenga entre 7 y 15 dígitos."""
        if not isinstance(telefono, str):
            raise ValidacionError("El teléfono debe ser texto.")

        telefono = telefono.strip()

        if not re.fullmatch(r"\+?\d{7,15}", telefono):
            raise ValidacionError(
                "El teléfono debe contener entre 7 y 15 dígitos."
            )

        return telefono

    @property
    def nombre(self):
        """Retorna el nombre del cliente."""
        return self._nombre

    @property
    def correo(self):
        """Retorna el correo del cliente."""
        return self._correo

    @property
    def telefono(self):
        """Retorna el teléfono del cliente."""
        return self._telefono

    def actualizar_datos(self, nombre=None, correo=None, telefono=None):
        """Actualiza los datos del cliente después de validarlos."""
        if nombre is not None:
            self._nombre = self._validar_nombre(nombre)

        if correo is not None:
            self._correo = self._validar_correo(correo)

        if telefono is not None:
            self._telefono = self._validar_telefono(telefono)

    def validar(self):
        """Verifica que los datos del cliente sean correctos."""
        try:
            self._validar_nombre(self._nombre)
            self._validar_correo(self._correo)
            self._validar_telefono(self._telefono)
            return True

        except ValidacionError as error:
            raise ClienteError(
                f"Error en los datos del cliente: {error}"
            ) from error

    def obtener_informacion(self):
        """Devuelve la información general del cliente."""
        return {
            "identificador": self.identificador,
            "nombre": self.nombre,
            "correo": self.correo,
            "telefono": self.telefono,
            "activo": self.activo,
            "fecha_creacion": self.fecha_creacion.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

    def __str__(self):
        """Representación textual del cliente."""
        return (
            f"Cliente: {self.nombre} | "
            f"Correo: {self.correo} | "
            f"Teléfono: {self.telefono}"
        )