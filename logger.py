# ============================================================
# logger.py — Módulo de registro de errores y eventos
# Proyecto: Software FJ - Sistema de Gestión de Reservas
# ============================================================

import datetime
import os

# Nombre del archivo donde se guardan los registros del sistema
ARCHIVO_LOGS = "logs.txt"


def _escribir_log(nivel: str, mensaje: str) -> None:
    """
    Escribe una entrada en el archivo de logs con marca de tiempo.
    Esta función es privada (uso interno del módulo).
    """
    marca_tiempo = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entrada = f"[{marca_tiempo}] [{nivel}] {mensaje}\n"

    # Guardamos el log en el archivo de texto
    with open(ARCHIVO_LOGS, "a", encoding="utf-8") as archivo:
        archivo.write(entrada)


def log_info(mensaje: str) -> None:
    """Registra un evento informativo en el sistema."""
    _escribir_log("INFO", mensaje)


def log_error(mensaje: str) -> None:
    """Registra un error ocurrido en el sistema."""
    _escribir_log("ERROR", mensaje)


def log_advertencia(mensaje: str) -> None:
    """Registra una advertencia en el sistema."""
    _escribir_log("ADVERTENCIA", mensaje)


def obtener_logs() -> str:
    """
    Retorna el contenido completo del archivo de logs como texto.
    Si el archivo no existe, retorna un mensaje indicándolo.
    """
    try:
        with open(ARCHIVO_LOGS, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            return contenido if contenido else "(Sin registros aún)"
    except FileNotFoundError:
        return "(El archivo de logs aún no existe)"


def limpiar_logs() -> None:
    """Elimina todos los registros del archivo de logs."""
    with open(ARCHIVO_LOGS, "w", encoding="utf-8") as archivo:
        archivo.write("")
