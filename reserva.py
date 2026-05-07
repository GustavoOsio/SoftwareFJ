# ============================================================
# reserva.py — Clase Reserva
# Proyecto: Software FJ - Sistema de Gestión de Reservas
# POO: Encapsulación, relación entre Cliente y Servicio
# ============================================================

import datetime
from cliente import Cliente
from servicio import ServicioBase, formatear_cop
from excepciones import ReservaInvalidaError, ReservaYaCanceladaError


class Reserva:
    """
    Representa una reserva que une un Cliente con un Servicio.
    Gestiona el ciclo de vida: creación, confirmación y cancelación.
    Aplica manejo de excepciones para garantizar operaciones seguras.
    """

    # Estados posibles de una reserva
    ESTADO_ACTIVA = "Activa"
    ESTADO_CANCELADA = "Cancelada"

    def __init__(self, id_reserva: int, cliente: Cliente,
                 servicio: ServicioBase, horas: int = 1,
                 descuento: float = 0.0, impuesto: float = 0.0) -> None:
        """
        Crea una nueva reserva.
        Verifica que el cliente y el servicio sean válidos.
        Lanza excepciones si hay algún problema.
        """
        # Validamos que existan cliente y servicio
        if cliente is None or servicio is None:
            raise ReservaInvalidaError("La reserva requiere un cliente y un servicio válidos.")

        # Validamos horas
        if horas < 1:
            raise ReservaInvalidaError("La duración mínima debe ser de 1 hora.")

        # Verificamos que el servicio esté disponible (puede lanzar excepción)
        servicio.verificar_disponibilidad()

        # Guardamos los datos de la reserva (atributos privados)
        self.__id_reserva = id_reserva
        self.__cliente = cliente
        self.__servicio = servicio
        self.__horas = horas
        self.__descuento = descuento
        self.__impuesto = impuesto
        self.__estado = self.ESTADO_ACTIVA
        self.__fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ── Getters ──────────────────────────────────────────────
    def get_id(self) -> int:
        return self.__id_reserva

    def get_cliente(self) -> Cliente:
        return self.__cliente

    def get_servicio(self) -> ServicioBase:
        return self.__servicio

    def get_estado(self) -> str:
        return self.__estado

    def get_fecha(self) -> str:
        return self.__fecha

    def get_horas(self) -> int:
        return self.__horas

    def get_descuento(self) -> float:
        return self.__descuento

    def get_impuesto(self) -> float:
        return self.__impuesto

    # ── Operaciones principales ───────────────────────────────
    def cancelar(self) -> None:
        """
        Cancela la reserva.
        Lanza ReservaYaCanceladaError si ya estaba cancelada.
        Uso de try/except para manejo de excepciones.
        """
        if self.__estado == self.ESTADO_CANCELADA:
            raise ReservaYaCanceladaError(
                f"La reserva #{self.__id_reserva} ya fue cancelada anteriormente."
            )
        self.__estado = self.ESTADO_CANCELADA

    def esta_activa(self) -> bool:
        """Retorna True si la reserva está activa."""
        return self.__estado == self.ESTADO_ACTIVA

    def get_costo(self) -> float:
        """
        Calcula el costo de la reserva usando polimorfismo:
        cada servicio calcula su costo de forma diferente.
        """
        return self.__servicio.calcular_costo(
            horas=self.__horas,
            descuento=self.__descuento,
            impuesto=self.__impuesto
        )

    # ── Representación del objeto como texto ─────────────────
    def __str__(self) -> str:
        return (f"Reserva(id={self.__id_reserva}, "
                f"cliente='{self.__cliente.get_nombre()}', "
                f"servicio='{self.__servicio.get_nombre()}', "
                f"estado={self.__estado}, "
                f"fecha={self.__fecha}, "
                f"costo={formatear_cop(self.get_costo())})")
