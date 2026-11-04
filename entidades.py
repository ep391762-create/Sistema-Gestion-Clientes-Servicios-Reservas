"""
Módulo de entidades generales del sistema.
Implementa la clase abstracta EntidadSistema.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4


class EntidadSistema(ABC):
    """
    Clase abstracta que representa las entidades generales
    del sistema de gestión.
    """

    def __init__(self, identificador=None):
        """
        Inicializa los atributos generales de una entidad.
        """
        self._identificador = identificador or str(uuid4())
        self._fecha_creacion = datetime.now()
        self._activo = True

    @property
    def identificador(self):
        """Retorna el identificador único de la entidad."""
        return self._identificador

    @property
    def fecha_creacion(self):
        """Retorna la fecha de creación de la entidad."""
        return self._fecha_creacion

    @property
    def activo(self):
        """Indica si la entidad se encuentra activa."""
        return self._activo

    def activar(self):
        """Activa la entidad."""
        self._activo = True

    def desactivar(self):
        """Desactiva la entidad."""
        self._activo = False

    @abstractmethod
    def validar(self):
        """
        Método abstracto para validar los datos
        de cada entidad.
        """
        pass

    @abstractmethod
    def obtener_informacion(self):
        """
        Método abstracto para consultar la información
        de cada entidad.
        """
        pass