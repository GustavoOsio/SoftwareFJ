"""
╔══════════════════════════════════════════════════════════╗
║           SISTEMA DE RESERVAS — SOFTWARE FJ              ║
╚══════════════════════════════════════════════════════════╝
"""

INTEGRANTES = [
    ("Luis Gustavo Osio Salazar",       "Arquitecto / Excepciones"),
    ("Ana María Fernández López",       "Módulo Cliente / Logs"),
    ("Carlos Eduardo Martínez Ruiz",    "Módulo Servicio / Simulación"),
    ("Diana Patricia Torres Gómez",     "Servicios Derivados / Documentación"),
    ("Jose Alejandro Munoz Cerpa",  "Módulo Reserva"),
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

"""
Clase Reserva
Representa una reserva dentro del sistema software FJ.

"""
class Reserva:
    
    def __init__(self , cliente, servicio, duracion):
        if cliente is None:
            raise ValueError("El cliente no puede ser None")
        
        if servicio is None:
            raise ValueError("El servicio no puede ser None")
        
        if duracion <= 0:
            raise ValueError("La duracion no puede ser 0")
        
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "pendiente"
        
    def confirmar(self):
        # Confirma si la reserva esta en estado pendiente
        
        if self.estado != "pendiente":
            raise Exception("solo se puenden confirmar reservas pendientes.")
        
        self.estado = "confirmada"
        
    def cancelar(self):
        # Cancela la reserva
    
        if self.estado == "cancelada":
            raise Exception("La reserva ya está cancelada")
        
        self.estado = "cancelada"
        
    def calcualar_total(self):
        # Obtiene el costo del servicio
        
        try:
            # Obtiene el costo del servicio
            costo = self.sevicio.calcular_costo()
            
            # Calcula el costo del servicio
            return costo * self.duracion
        
        except Exception as e:
            raise Exception("Error al calcualar el costo") from e
    
    def procesar(self):
        # Calcular el total de la reserva
        
        try:
            total = self.calcular_total()
            
            # Confirmar la reserva
            self.confirmar()

            # Retorna mensaje exitoso
            return f"Reserva confirmada. Total:{total}"
        
        except Exception as e:
            self.estado = "cancelada"
            return f"Error al procesar la reserva:{str(e)}"
        
        print("cambio para git")
            
            
    

        
        

        