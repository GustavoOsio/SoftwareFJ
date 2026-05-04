# ============================================================

# main.py — Punto de entrada del programa

# Proyecto: software_fi

# Simula mínimo 10 operaciones del sistema

# ============================================================
 
from cliente import Cliente

from servicio import ServicioBasico, ServicioPremium

from reserva import Reserva

from excepciones import (

    ClienteInvalidoError,

    ClienteNoEncontradoError,

    ServicioNoDisponibleError,

    ReservaYaCanceladaError,

    ReservaNoEncontradaError,

)

from logger import log_info, log_error, mostrar_logs

from reportes import imprimir_reporte_general, guardar_reporte_general
 
 
# ── Almacenamiento en memoria (listas) ───────────────────────

clientes = []

servicios = []

reservas = []
 
 
# ── Funciones auxiliares ─────────────────────────────────────

def buscar_cliente(id_cliente: int) -> Cliente:

    for c in clientes:

        if c.get_id() == id_cliente:

            return c

    raise ClienteNoEncontradoError(f"No se encontró el cliente con ID {id_cliente}.")
 
 
def buscar_reserva(id_reserva: int) -> Reserva:

    for r in reservas:

        if r.get_id() == id_reserva:

            return r

    raise ReservaNoEncontradaError(f"No se encontró la reserva con ID {id_reserva}.")
 
 
# ── Operaciones del sistema ───────────────────────────────────

def main():

    print("\n========== INICIO DEL SISTEMA software_fi ==========\n")
 
    # ── Operación 1: Crear clientes válidos ──────────────────

    print("--- Operación 1: Crear clientes ---")

    try:

        c1 = Cliente(1, "Ana García", "ana@email.com")

        c2 = Cliente(2, "Luis Pérez", "luis@email.com")

        c3 = Cliente(3, "María López", "maria@email.com")

        clientes.extend([c1, c2, c3])

        log_info(f"Cliente creado: {c1}")

        log_info(f"Cliente creado: {c2}")

        log_info(f"Cliente creado: {c3}")

    except ClienteInvalidoError as e:

        log_error(f"Error al crear cliente: {e}")
 
    # ── Operación 2: Crear cliente con datos inválidos ────────

    print("\n--- Operación 2: Cliente con datos inválidos ---")

    try:

        c_malo = Cliente(99, "", "")

        clientes.append(c_malo)

    except ClienteInvalidoError as e:

        log_error(f"ClienteInvalidoError capturado: {e}")
 
    # ── Operación 3: Crear servicios básicos ──────────────────

    print("\n--- Operación 3: Crear servicios básicos ---")

    s1 = ServicioBasico(1, "Corte de cabello")

    s2 = ServicioBasico(2, "Manicure")

    servicios.extend([s1, s2])

    log_info(f"Servicio creado: {s1}")

    log_info(f"Servicio creado: {s2}")
 
    # ── Operación 4: Crear servicio premium ───────────────────

    print("\n--- Operación 4: Crear servicio premium ---")

    s3 = ServicioPremium(3, "Spa completo", multiplicador=3.0)

    s4 = ServicioPremium(4, "Masaje relajante", multiplicador=2.5, disponible=False)

    servicios.extend([s3, s4])

    log_info(f"Servicio creado: {s3}")

    log_info(f"Servicio creado: {s4} (no disponible)")
 
    # ── Operación 5: Realizar reservas válidas ────────────────

    print("\n--- Operación 5: Crear reservas válidas ---")

    try:

        r1 = Reserva(1, c1, s1)

        r2 = Reserva(2, c2, s3)

        reservas.extend([r1, r2])

        log_info(f"Reserva creada: {r1}")

        log_info(f"Reserva creada: {r2}")

    except Exception as e:

        log_error(f"Error al crear reserva: {e}")
 
    # ── Operación 6: Reservar servicio no disponible ──────────

    print("\n--- Operación 6: Reservar servicio no disponible ---")

    try:

        r_mala = Reserva(99, c3, s4)

        reservas.append(r_mala)

    except ServicioNoDisponibleError as e:

        log_error(f"ServicioNoDisponibleError capturado: {e}")
 
    # ── Operación 7: Listar reservas activas ──────────────────

    print("\n--- Operación 7: Listar reservas activas ---")

    activas = [r for r in reservas if r.esta_activa()]

    if activas:

        for r in activas:

            print(f"  {r}")

        log_info(f"Consulta: {len(activas)} reserva(s) activa(s) encontradas.")

    else:

        print("  No hay reservas activas.")
 
    # ── Operación 8: Cancelar una reserva ────────────────────

    print("\n--- Operación 8: Cancelar reserva #1 ---")

    try:

        r = buscar_reserva(1)

        r.cancelar()

        log_info(f"Reserva #{r.get_id()} cancelada exitosamente.")

    except ReservaNoEncontradaError as e:

        log_error(f"ReservaNoEncontradaError: {e}")
 
    # ── Operación 9: Cancelar reserva ya cancelada ────────────

    print("\n--- Operación 9: Cancelar reserva ya cancelada ---")

    try:

        r = buscar_reserva(1)

        r.cancelar()

    except ReservaYaCanceladaError as e:

        log_error(f"ReservaYaCanceladaError capturado: {e}")
 
    # ── Operación 10: Buscar cliente inexistente ──────────────

    print("\n--- Operación 10: Buscar cliente que no existe ---")

    try:

        buscar_cliente(999)

    except ClienteNoEncontradoError as e:

        log_error(f"ClienteNoEncontradoError capturado: {e}")
 
    # ── Operación 11: Calcular costo total (polimorfismo) ─────

    print("\n--- Operación 11: Costo total de reservas activas ---")

    activas = [r for r in reservas if r.esta_activa()]

    total = sum(r.get_costo() for r in activas)

    log_info(f"Costo total de {len(activas)} reserva(s) activa(s): ${total:.2f}")
 
    # ── Operación 12: Generar reporte general ─────────────────

    print("\n--- Operación 12: Reporte general del sistema ---")

    try:

        imprimir_reporte_general(clientes, servicios, reservas)

        archivo_reporte = guardar_reporte_general(clientes, servicios, reservas)

        log_info(f"Reporte general generado correctamente en: {archivo_reporte}")

    except Exception as e:

        log_error(f"No se pudo generar el reporte general: {e}")
 
    # ── Operación 13: Mostrar historial de logs ───────────────

    print("\n--- Operación 13: Historial de logs ---")

    mostrar_logs()
 
    print("\n========== FIN DEL SISTEMA software_fj ==========\n")
 
 
if __name__ == "__main__":

    main()
 