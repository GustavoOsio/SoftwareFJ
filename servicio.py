# ============================================================
# servicio.py — Clases de Servicio (abstracta y derivadas)
# Proyecto: Software FJ - Sistema de Gestión de Reservas
# POO: Abstracción, Herencia, Polimorfismo, Encapsulación
# ============================================================

from abc import ABC, abstractmethod
from excepciones import ServicioNoDisponibleError


def formatear_cop(valor: float) -> str:
    """Convierte un valor numérico al formato colombiano: $75.000 COP."""
    try:
        numero = int(round(float(valor)))
    except (TypeError, ValueError):
        numero = 0
    return f"${numero:,}".replace(",", ".") + " COP"


class ServicioBase(ABC):
    """
    Clase ABSTRACTA base para todos los servicios del sistema.
    Define la interfaz común que deben cumplir todos los servicios.
    No se puede instanciar directamente — es solo una plantilla.
    """

    def __init__(self, id_servicio: int, nombre: str, disponible: bool = True) -> None:
        # Atributos privados (encapsulación)
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

    # ── Método abstracto: DEBE ser implementado por las subclases ──
    @abstractmethod
    def calcular_costo(self, horas: int = 1, descuento: float = 0.0, impuesto: float = 0.0) -> float:
        """
        Calcula el costo del servicio.
        Cada subclase define cómo se calcula según sus propias reglas.
        Parámetros opcionales permiten simular sobrecarga de métodos.
        """
        pass

    @abstractmethod
    def describir(self) -> str:
        """Retorna una descripción detallada del servicio."""
        pass

    def verificar_disponibilidad(self) -> None:
        """
        Verifica si el servicio está disponible.
        Lanza ServicioNoDisponibleError si no lo está.
        """
        if not self.__disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.__nombre}' no está disponible actualmente."
            )

    def get_tipo(self) -> str:
        """Retorna el tipo/nombre de la clase del servicio."""
        return self.__class__.__name__

    def __str__(self) -> str:
        estado = "Disponible" if self.__disponible else "No disponible"
        return (f"{self.__class__.__name__}(id={self.__id_servicio}, "
                f"nombre='{self.__nombre}', estado={estado}, "
                f"costo={formatear_cop(self.calcular_costo())})")


# ── Subclase 1: Reserva de Sala ───────────────────────────────
class ReservaSala(ServicioBase):
    """
    Servicio de reserva de salas de trabajo o reuniones.
    HEREDA de ServicioBase e implementa sus métodos abstractos.
    Costo: tarifa por hora × número de horas.
    """

    TARIFA_POR_HORA = 40000.0  # precio base por hora

    def __init__(self, id_servicio: int, nombre: str,
                 capacidad: int = 10, disponible: bool = True) -> None:
        super().__init__(id_servicio, nombre, disponible)
        self.__capacidad = capacidad  # cantidad de personas que caben

    def get_capacidad(self) -> int:
        return self.__capacidad

    def calcular_costo(self, horas: int = 1, descuento: float = 0.0, impuesto: float = 0.0) -> float:
        """
        POLIMORFISMO: implementa cálculo específico para salas.
        Costo = tarifa × horas, con descuento e impuesto opcionales.
        """
        costo_base = self.TARIFA_POR_HORA * horas
        costo_con_descuento = costo_base * (1 - descuento / 100)
        costo_final = costo_con_descuento * (1 + impuesto / 100)
        return round(costo_final, 2)

    def describir(self) -> str:
        """POLIMORFISMO: descripción propia de este tipo de servicio."""
        return (f"Reserva de sala '{self.get_nombre()}' "
                f"| Capacidad: {self.__capacidad} personas "
                f"| Tarifa: {formatear_cop(self.TARIFA_POR_HORA)}/hora")


# ── Subclase 2: Alquiler de Equipos ──────────────────────────
class AlquilerEquipo(ServicioBase):
    """
    Servicio de alquiler de equipos tecnológicos.
    HEREDA de ServicioBase e implementa sus métodos abstractos.
    Costo: tarifa diaria × número de días.
    """

    TARIFA_POR_DIA = 80000.0  # precio base por día

    def __init__(self, id_servicio: int, nombre: str,
                 tipo_equipo: str = "General", disponible: bool = True) -> None:
        super().__init__(id_servicio, nombre, disponible)
        self.__tipo_equipo = tipo_equipo

    def get_tipo_equipo(self) -> str:
        return self.__tipo_equipo

    def calcular_costo(self, horas: int = 1, descuento: float = 0.0, impuesto: float = 0.0) -> float:
        """
        POLIMORFISMO: implementa cálculo específico para equipos.
        Aquí 'horas' representa días de alquiler.
        """
        dias = horas  # reutilizamos el parámetro como días
        costo_base = self.TARIFA_POR_DIA * dias
        costo_con_descuento = costo_base * (1 - descuento / 100)
        costo_final = costo_con_descuento * (1 + impuesto / 100)
        return round(costo_final, 2)

    def describir(self) -> str:
        """POLIMORFISMO: descripción propia de este tipo de servicio."""
        return (f"Alquiler de equipo '{self.get_nombre()}' "
                f"| Tipo: {self.__tipo_equipo} "
                f"| Tarifa: {formatear_cop(self.TARIFA_POR_DIA)}/día")


# ── Subclase 3: Asesoría Especializada ───────────────────────
class AsesoriaEspecializada(ServicioBase):
    """
    Servicio de asesorías por expertos en diferentes áreas.
    HEREDA de ServicioBase e implementa sus métodos abstractos.
    Costo: tarifa base × factor de especialización × horas.
    """

    TARIFA_BASE = 60000.0  # precio base por hora

    def __init__(self, id_servicio: int, nombre: str,
                 area: str = "General", factor_especialidad: float = 1.0,
                 disponible: bool = True) -> None:
        super().__init__(id_servicio, nombre, disponible)
        self.__area = area
        self.__factor_especialidad = factor_especialidad  # entre 1.0 y 3.0

    def get_area(self) -> str:
        return self.__area

    def get_factor(self) -> float:
        return self.__factor_especialidad

    def calcular_costo(self, horas: int = 1, descuento: float = 0.0, impuesto: float = 0.0) -> float:
        """
        POLIMORFISMO: implementa cálculo específico para asesorías.
        Costo = tarifa_base × factor_especialidad × horas.
        """
        costo_base = self.TARIFA_BASE * self.__factor_especialidad * horas
        costo_con_descuento = costo_base * (1 - descuento / 100)
        costo_final = costo_con_descuento * (1 + impuesto / 100)
        return round(costo_final, 2)

    def describir(self) -> str:
        """POLIMORFISMO: descripción propia de este tipo de servicio."""
        return (f"Asesoría '{self.get_nombre()}' "
                f"| Área: {self.__area} "
                f"| Factor especialidad: x{self.__factor_especialidad} "
                f"| Tarifa base: {formatear_cop(self.TARIFA_BASE)}/hora")
