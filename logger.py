# ============================================================
# logger.py — Módulo de registro de errores y eventos
# Proyecto: software_fi
# ============================================================

import datetime


ARCHIVO_LOGS = "logs.txt"


def _escribir_log(nivel: str, mensaje: str) -> None:
    """Escribe una entrada en el archivo de logs con marca de tiempo."""
    marca_tiempo = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entrada = f"[{marca_tiempo}] [{nivel}] {mensaje}\n"
    with open(ARCHIVO_LOGS, "a", encoding="utf-8") as archivo:
        archivo.write(entrada)
    print(entrada.strip())


def log_info(mensaje: str) -> None:
    """Registra un evento informativo."""
    _escribir_log("INFO", mensaje)


def log_error(mensaje: str) -> None:
    """Registra un error en el sistema."""
    _escribir_log("ERROR", mensaje)


def log_advertencia(mensaje: str) -> None:
    """Registra una advertencia."""
    _escribir_log("ADVERTENCIA", mensaje)


def mostrar_logs() -> None:
    """Muestra el contenido completo del archivo de logs."""
    print("\n===== HISTORIAL DE LOGS =====")
    try:
        with open(ARCHIVO_LOGS, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            print(contenido if contenido else "(sin registros aún)")
    except FileNotFoundError:
        print("(el archivo logs.txt aún no existe)")
    print("=" * 30)
