# Sistema de Reservas — Software FJ

Sistema orientado a objetos en Python para gestionar reservas de servicios,
con manejo de excepciones personalizadas, logging y simulación de operaciones.

---

## Integrantes

| # | Nombre | Rol |
|---|--------|-----|
| 1 | Luis Gustavo Osio Salazar | Arquitecto / Excepciones |
| 2 | Ana María Fernández López | Módulo Cliente / Logs |
| 3 | Carlos Eduardo Martínez Ruiz | Módulo Servicio / Simulación |
| 4 | Diana Patricia Torres Gómez | Servicios Derivados / Documentación |
| 5 | Javier Andrés Herrera Castillo | Módulo Reserva |

---

## Requisitos

- Python 3.10+
- pip

## Instalación

```bash
git clone https://github.com/tu-usuario/SoftwareFJ.git
cd SoftwareFJ
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

## Pruebas

```bash
pytest tests/
```

## Estructura del proyecto

```
SoftwareFJ/
├── src/
│   ├── modelo/          # Clases del dominio
│   ├── excepciones/     # Excepciones personalizadas
│   ├── servicios/       # Lógica de negocio
│   └── logs/            # Sistema de logging
├── simulacion/          # Simulación de 10 operaciones
├── tests/               # Pruebas con pytest
├── docs/                # Documentación del proyecto
└── main.py              # Punto de entrada
```
