git
 
# reportes.py — Módulo de reportes del sistema

# Proyecto: software_fi

# Aporte colaborativo: genera resumen general sin alterar la lógica

# ============================================================
 
from datetime import datetime
 
 
def _ejecutar_metodo_seguro(objeto, nombre_metodo, valor_defecto=None):

    """

    Ejecuta un método si existe en el objeto.

    Evita que el reporte dañe la ejecución principal del sistema.

    """

    metodo = getattr(objeto, nombre_metodo, None)
 
    if callable(metodo):

        try:

            return metodo()

        except Exception:

            return valor_defecto
 
    return valor_defecto
 
 
def generar_reporte_general(clientes, servicios, reservas):

    """

    Genera un resumen general del estado actual del sistema.

    No modifica clientes, servicios ni reservas.

    """
 
    reservas_activas = []

    reservas_canceladas = []

    costo_total_activo = 0
 
    for reserva in reservas:

        esta_activa = _ejecutar_metodo_seguro(reserva, "esta_activa", False)
 
        if esta_activa:

            reservas_activas.append(reserva)

            costo = _ejecutar_metodo_seguro(reserva, "get_costo", 0)
 
            try:

                costo_total_activo += float(costo)

            except (TypeError, ValueError):

                costo_total_activo += 0

        else:

            reservas_canceladas.append(reserva)
 
    reporte = {

        "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "total_clientes": len(clientes),

        "total_servicios": len(servicios),

        "total_reservas": len(reservas),

        "reservas_activas": len(reservas_activas),

        "reservas_canceladas": len(reservas_canceladas),

        "costo_total_reservas_activas": costo_total_activo,

    }
 
    return reporte
 
 
def imprimir_reporte_general(clientes, servicios, reservas):

    """

    Imprime en consola el reporte general del sistema.

    """
 
    reporte = generar_reporte_general(clientes, servicios, reservas)
 
    print("\n========== REPORTE GENERAL DEL SISTEMA ==========")

    print(f"Fecha de generación: {reporte['fecha_generacion']}")

    print(f"Total de clientes registrados: {reporte['total_clientes']}")

    print(f"Total de servicios registrados: {reporte['total_servicios']}")

    print(f"Total de reservas registradas: {reporte['total_reservas']}")

    print(f"Reservas activas: {reporte['reservas_activas']}")

    print(f"Reservas canceladas: {reporte['reservas_canceladas']}")

    print(f"Costo total de reservas activas: ${reporte['costo_total_reservas_activas']:.2f}")

    print("=================================================\n")
 
 
def guardar_reporte_general(clientes, servicios, reservas, ruta_archivo="reporte_sistema.txt"):

    """

    Guarda el reporte general en un archivo .txt.

    """
 
    reporte = generar_reporte_general(clientes, servicios, reservas)
 
    contenido = [

        "========== REPORTE GENERAL DEL SISTEMA ==========",

        f"Fecha de generación: {reporte['fecha_generacion']}",

        f"Total de clientes registrados: {reporte['total_clientes']}",

        f"Total de servicios registrados: {reporte['total_servicios']}",

        f"Total de reservas registradas: {reporte['total_reservas']}",

        f"Reservas activas: {reporte['reservas_activas']}",

        f"Reservas canceladas: {reporte['reservas_canceladas']}",

        f"Costo total de reservas activas: ${reporte['costo_total_reservas_activas']:.2f}",

        "=================================================",

    ]
 
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:

        archivo.write("\n".join(contenido))
 
    return ruta_archivo
 