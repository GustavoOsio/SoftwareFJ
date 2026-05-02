# ============================================================
# reserva.py — Clase Reserva
# Proyecto: software_fi
# POO: Encapsulación, relación entre Cliente y Servicio
# ============================================================

import datetime
from cliente import Cliente
from servicio import ServicioBase
from excepciones import ReservaInvalidaError, ReservaYaCanceladaError


class Reserva:
    """
    Representa una reserva que asocia un Cliente con un Servicio.
    Gestiona el estado del ciclo de vida de la reserva.
    """

    ESTADO_ACTIVA = "activa"
    ESTADO_CANCELADA = "cancelada"

    def __init__(self, id_reserva: int, cliente: Cliente, servicio: ServicioBase) -> None:
        if cliente is None or servicio is None:
            raise ReservaInvalidaError("La reserva requiere un cliente y un servicio válidos.")
        # Verificar disponibilidad (puede lanzar ServicioNoDisponibleError)
        servicio.verificar_disponibilidad()

        self.__id_reserva = id_reserva
        self.__cliente = cliente
        self.__servicio = servicio
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

    # ── Operaciones ──────────────────────────────────────────
    def cancelar(self) -> None:
        """Cancela la reserva; lanza excepción si ya está cancelada."""
        if self.__estado == self.ESTADO_CANCELADA:
            raise ReservaYaCanceladaError(
                f"La reserva #{self.__id_reserva} ya fue cancelada anteriormente."
            )
        self.__estado = self.ESTADO_CANCELADA

    def esta_activa(self) -> bool:
        return self.__estado == self.ESTADO_ACTIVA

    def get_costo(self) -> float:
        return self.__servicio.calcular_costo()
    
        # ── Procesa la reserva calculando su costo total ───────── 
        # ── Si ocurre un error, la reserva se cancela automaticamente ───────── 
    def procesar(self) -> str:
        try:
            costo =self.get_costo()
            return f"Reserva #{self.__id_reserva} procesada correctamente. costo: ${costo:.2f}"
        
        except Exception as e:
            self.cancelar()
            return f"Error al procesar la reserva: {str(e)}"

    # ── Representación ───────────────────────────────────────
    def __str__(self) -> str:
        return (f"Reserva(id={self.__id_reserva}, "
                f"cliente='{self.__cliente.get_nombre()}', "
                f"servicio='{self.__servicio.get_nombre()}', "
                f"estado={self.__estado}, fecha={self.__fecha}, "
                f"costo=${self.get_costo():.2f})")
        


