# ============================================================
# cliente.py — Clase Cliente
# Proyecto: Software FJ - Sistema de Gestión de Reservas
# POO: Encapsulación (atributos privados + getters/setters)
# ============================================================

from excepciones import ClienteInvalidoError


class Cliente:
    """
    Representa a un cliente del sistema Software FJ.
    Aplica encapsulación: los datos se guardan de forma privada
    y solo se acceden mediante métodos controlados.
    """

    def __init__(self, id_cliente: int, nombre: str, correo: str, telefono: str = "") -> None:
        """
        Crea un nuevo cliente con validaciones de datos.
        Lanza ClienteInvalidoError si el nombre o correo están vacíos.
        """
        # Validamos antes de guardar los datos
        if not nombre or not nombre.strip():
            raise ClienteInvalidoError("El nombre del cliente no puede estar vacío.")
        if not correo or not correo.strip():
            raise ClienteInvalidoError("El correo del cliente no puede estar vacío.")
        if "@" not in correo:
            raise ClienteInvalidoError("El correo ingresado no tiene un formato válido.")

        # Atributos privados (encapsulación)
        self.__id_cliente = id_cliente
        self.__nombre = nombre.strip()
        self.__correo = correo.strip()
        self.__telefono = telefono.strip()

    # ── Getters (acceso controlado a los datos) ──────────────
    def get_id(self) -> int:
        return self.__id_cliente

    def get_nombre(self) -> str:
        return self.__nombre

    def get_correo(self) -> str:
        return self.__correo

    def get_telefono(self) -> str:
        return self.__telefono

    # ── Setters (modificación controlada de los datos) ───────
    def set_nombre(self, nuevo_nombre: str) -> None:
        if not nuevo_nombre or not nuevo_nombre.strip():
            raise ClienteInvalidoError("El nombre no puede estar vacío.")
        self.__nombre = nuevo_nombre.strip()

    def set_correo(self, nuevo_correo: str) -> None:
        if not nuevo_correo or not nuevo_correo.strip():
            raise ClienteInvalidoError("El correo no puede estar vacío.")
        if "@" not in nuevo_correo:
            raise ClienteInvalidoError("El correo ingresado no tiene un formato válido.")
        self.__correo = nuevo_correo.strip()

    def set_telefono(self, nuevo_telefono: str) -> None:
        self.__telefono = nuevo_telefono.strip()

    # ── Representación del objeto como texto ─────────────────
    def __str__(self) -> str:
        return (f"Cliente(id={self.__id_cliente}, "
                f"nombre='{self.__nombre}', "
                f"correo='{self.__correo}', "
                f"telefono='{self.__telefono}')")
