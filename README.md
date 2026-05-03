# Sistema de Reservas — Software FJ

Sistema orientado a objetos en Python para gestionar reservas de servicios,
con manejo de excepciones personalizadas, logging y simulación de operaciones.

---

## Integrantes

| # | Nombre | Rol |
|---|--------|-----|
| 1 | Luis Gustavo Osio Salazar | Arquitecto / Excepciones |
| 2 | Jose Alejandro | Módulo Cliente / Logs |
| 3 |  / Simulación |
| 4 |  | Servicios Derivados / Documentación |
| 5 |  | Módulo Reserva |

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
## estructura clientes 

SoftwareFJ/
│
├── clases/cliente.py
├── servicios/servicio.py
├── servicios/sala.py
├── servicios/equipos.py
├── servicios/asesoria.py
├── reservas/reserva.py
├── excepciones/excepciones.py
├── logs/logger.py
├── simulacion.py
└── main.py
