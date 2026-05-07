# ============================================================
# excepciones.py — Excepciones personalizadas del sistema
# Proyecto: Software FJ - Sistema de Gestión de Reservas
# ============================================================


class ClienteNoEncontradoError(Exception):
    """Se lanza cuando no se encuentra un cliente por su ID."""
    pass


class ClienteInvalidoError(Exception):
    """Se lanza cuando los datos del cliente son inválidos."""
    pass


class ServicioNoDisponibleError(Exception):
    """Se lanza cuando un servicio no está disponible para reservar."""
    pass


class ReservaInvalidaError(Exception):
    """Se lanza cuando se intenta crear una reserva con datos incorrectos."""
    pass


class ReservaNoEncontradaError(Exception):
    """Se lanza cuando no se encuentra una reserva por su ID."""
    pass


class ReservaYaCanceladaError(Exception):
    """Se lanza cuando se intenta cancelar una reserva que ya fue cancelada."""
    pass
