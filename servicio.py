# ============================================================
# servicio.py — Clase base Servicio y subclases
# Proyecto: software_fi
# POO: Abstracción, Herencia, Polimorfismo
# ============================================================

from abc import ABC, abstractmethod
from excepciones import ServicioNoDisponibleError


class ServicioBase(ABC):
    """
    Clase abstracta base para todos los servicios.
    Aplica abstracción: define la interfaz común.
    """

    def __init__(self, id_servicio: int, nombre: str, disponible: bool = True) -> None:
        self.__id_servicio = id_servicio
        self.__nombre = nombre
        self.__disponible = disponible

    # ── Getters ──────────────────────────────────────────────
    def get_id(self) -> int:
        return self.__id_servicio

    def get_nombre(self) -> str:
        return self.__nombre

    def esta_disponible(self) -> bool:
        return self.__disponible

    # ── Setters ──────────────────────────────────────────────
    def set_disponible(self, estado: bool) -> None:
        self.__disponible = estado

    # ── Método abstracto (polimorfismo) ──────────────────────
    @abstractmethod
    def calcular_costo(self) -> float:
        """Cada subclase implementa su propio cálculo de costo."""
        pass

    def verificar_disponibilidad(self) -> None:
        """Lanza excepción si el servicio no está disponible."""
        if not self.__disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.__nombre}' no está disponible actualmente."
            )

    def __str__(self) -> str:
        estado = "disponible" if self.__disponible else "no disponible"
        return (f"{self.__class__.__name__}(id={self.__id_servicio}, "
                f"nombre='{self.__nombre}', estado={estado}, "
                f"costo=${self.calcular_costo():.2f})")


# ── Subclase: ServicioBasico ──────────────────────────────────
class ServicioBasico(ServicioBase):
    """
    Servicio estándar con tarifa fija.
    Hereda de ServicioBase.
    """

    TARIFA = 50.0  # tarifa base en pesos/dólares

    def __init__(self, id_servicio: int, nombre: str, disponible: bool = True) -> None:
        super().__init__(id_servicio, nombre, disponible)

    def calcular_costo(self) -> float:
        """Polimorfismo: retorna tarifa fija."""
        return self.TARIFA


# ── Subclase: ServicioPremium ─────────────────────────────────
class ServicioPremium(ServicioBase):
    """
    Servicio premium con costo variable según multiplicador.
    Hereda de ServicioBase.
    """

    TARIFA_BASE = 50.0

    def __init__(self, id_servicio: int, nombre: str,
                 multiplicador: float = 2.0, disponible: bool = True) -> None:
        super().__init__(id_servicio, nombre, disponible)
        self.__multiplicador = multiplicador

    def calcular_costo(self) -> float:
        """Polimorfismo: retorna tarifa base × multiplicador."""
        return self.TARIFA_BASE * self.__multiplicador
