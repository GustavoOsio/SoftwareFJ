# ============================================================
# cliente.py — Clase Cliente
# Proyecto: software_fi
# POO: Encapsulación (atributos privados + getters/setters)
# ============================================================

from excepciones import ClienteInvalidoError


class Cliente:
    """
    Representa a un cliente del sistema.
    Aplica encapsulación mediante atributos privados.
    """

    def __init__(self, id_cliente: int, nombre: str, correo: str) -> None:
        # Validación antes de asignar
        if not nombre or not correo:
            raise ClienteInvalidoError("El nombre y el correo del cliente no pueden estar vacíos.")
        self.__id_cliente = id_cliente
        self.__nombre = nombre
        self.__correo = correo

    # ── Getters ──────────────────────────────────────────────
    def get_id(self) -> int:
        return self.__id_cliente

    def get_nombre(self) -> str:
        return self.__nombre

    def get_correo(self) -> str:
        return self.__correo

    # ── Setters ──────────────────────────────────────────────
    def set_nombre(self, nuevo_nombre: str) -> None:
        if not nuevo_nombre:
            raise ClienteInvalidoError("El nombre no puede estar vacío.")
        self.__nombre = nuevo_nombre

    def set_correo(self, nuevo_correo: str) -> None:
        if not nuevo_correo:
            raise ClienteInvalidoError("El correo no puede estar vacío.")
        self.__correo = nuevo_correo

    # ── Representación ───────────────────────────────────────
    def __str__(self) -> str:
        return f"Cliente(id={self.__id_cliente}, nombre='{self.__nombre}', correo='{self.__correo}')"
    


