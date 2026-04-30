"""
╔══════════════════════════════════════════════════════════╗
║           SISTEMA DE RESERVAS — SOFTWARE FJ              ║
╚══════════════════════════════════════════════════════════╝
"""

INTEGRANTES = [
    ("Luis Gustavo Osio Salazar",       "Arquitecto / Excepciones"),
    ("Jose Miguel Garcia Fernandez",       "Módulo Cliente / Logs"),
    ("Carlos Eduardo Martínez Ruiz",    "Módulo Servicio / Simulación"),
    ("Diana Patricia Torres Gómez",     "Servicios Derivados / Documentación"),
    ("Javier Andrés Herrera Castillo",  "Módulo Reserva"),
]

MODULOS = [
    ("modelo",      "Cliente, Servicio (abstracta), Reserva"),
    ("excepciones", "ReservaException y derivadas"),
    ("servicios",   "ClienteService, ReservaService"),
    ("logs",        "SistemaLogger"),
    ("simulacion",  "Simulacion — 10 operaciones"),
]


def banner():
    print("\n" + "═" * 60)
    print("   SISTEMA DE RESERVAS — SOFTWARE FJ")
    print("   Ingeniería de Software  |  v1.0  |  2025")
    print("═" * 60)


def mostrar_equipo():
    print("\n  EQUIPO DE DESARROLLO")
    print("  " + "─" * 56)
    for i, (nombre, rol) in enumerate(INTEGRANTES, 1):
        print(f"  {i}. {nombre}")
        print(f"     └─ {rol}")
    print("  " + "─" * 56)


def mostrar_modulos():
    print("\n  MÓDULOS DEL SISTEMA")
    print("  " + "─" * 56)
    for modulo, descripcion in MODULOS:
        print(f"  src/{modulo}/")
        print(f"     └─ {descripcion}")
    print("  " + "─" * 56)


def mostrar_estado():
    print("\n  ESTADO DEL PROYECTO")
    print("  " + "─" * 56)
    print("  [✓] Estructura de carpetas lista")
    print("  [✓] Repositorio inicializado")
    print("  [ ] Clases del modelo          → en desarrollo")
    print("  [ ] Excepciones personalizadas → en desarrollo")
    print("  [ ] Lógica de servicios        → en desarrollo")
    print("  [ ] Sistema de logging         → en desarrollo")
    print("  [ ] Simulación 10 operaciones  → en desarrollo")
    print("  " + "─" * 56)


def main():
    banner()
    mostrar_equipo()
    mostrar_modulos()
    mostrar_estado()
    print("\n  Ejecuta: pytest tests/  para correr las pruebas")
    print("═" * 60 + "\n")


if __name__ == "__main__":
    main()
