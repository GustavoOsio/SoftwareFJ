# ============================================================
# main.py — Punto de entrada principal del sistema Software FJ
# Proyecto: Sistema Integral de Gestión de Clientes, Servicios
#           y Reservas para Software FJ
# Curso: Programación 213023 — UNAD
# Interfaz gráfica desarrollada con Tkinter
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import datetime

# Importamos nuestros módulos propios
from cliente import Cliente
from servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada, formatear_cop
from reserva import Reserva
from excepciones import (
    ClienteInvalidoError,
    ClienteNoEncontradoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    ReservaNoEncontradaError,
    ReservaYaCanceladaError,
)
from logger import log_info, log_error, log_advertencia, obtener_logs, limpiar_logs


# ============================================================
# COLORES Y ESTILOS — Paleta de colores del sistema
# ============================================================
COLOR_FONDO = "#1C2B3A"          # azul oscuro principal
COLOR_PANEL = "#243447"          # panel lateral
COLOR_TARJETA = "#2E4057"        # tarjetas y secciones
COLOR_ACENTO = "#00C9A7"         # verde azulado — acento principal
COLOR_ACENTO2 = "#F7A440"        # naranja — acento secundario
COLOR_TEXTO = "#E8F4F8"          # texto claro
COLOR_TEXTO_GRIS = "#8BAABA"     # texto secundario gris
COLOR_ERROR = "#E74C3C"          # rojo para errores
COLOR_EXITO = "#2ECC71"          # verde para éxito
COLOR_ADVERTENCIA = "#F39C12"    # amarillo para advertencias
COLOR_BOTON = "#00C9A7"          # color de botones principales
COLOR_BOTON_HOVER = "#00A88A"    # color hover de botones
COLOR_BOTON_PELIGRO = "#C0392B"  # botón peligroso (cancelar)
COLOR_ENTRADA = "#1A2F40"        # fondo de campos de entrada
COLOR_BORDE = "#3D5A73"          # bordes


# ============================================================
# CLASE PRINCIPAL DE LA APLICACIÓN
# ============================================================

class AplicacionSoftwareFJ:
    """
    Clase principal que gestiona toda la interfaz gráfica del sistema.
    Contiene las listas en memoria de clientes, servicios y reservas.
    """

    def __init__(self, ventana_raiz: tk.Tk) -> None:
        """Inicializa la aplicación y configura la ventana principal."""
        self.ventana = ventana_raiz
        self.ventana.title("Software FJ — Sistema de Gestión de Reservas")
        self.ventana.geometry("1200x750")
        self.ventana.minsize(1000, 650)
        self.ventana.configure(bg=COLOR_FONDO)

        # ── Listas en memoria (sin base de datos) ────────────
        self.clientes = []       # lista de objetos Cliente
        self.servicios = []      # lista de objetos Servicio
        self.reservas = []       # lista de objetos Reserva
        self.contador_clientes = 1   # ID autoincremental
        self.contador_servicios = 1
        self.contador_reservas = 1

        # ── Variables de la interfaz ──────────────────────────
        self.pagina_actual = None   # controla qué panel está visible

        # Construimos la interfaz
        self._construir_interfaz()

        # Cargamos datos de ejemplo para demostrar el sistema
        self._cargar_datos_iniciales()

        # Mostramos la página de inicio por defecto
        self._mostrar_pagina("inicio")

    # ============================================================
    # CONSTRUCCIÓN DE LA INTERFAZ PRINCIPAL
    # ============================================================

    def _construir_interfaz(self) -> None:
        """Construye el esqueleto principal de la interfaz."""

        # ── Encabezado superior ──────────────────────────────
        self._crear_encabezado()

        # ── Marco contenedor principal (menú + contenido) ────
        marco_principal = tk.Frame(self.ventana, bg=COLOR_FONDO)
        marco_principal.pack(fill="both", expand=True)

        # ── Panel de menú lateral ────────────────────────────
        self._crear_menu_lateral(marco_principal)

        # ── Área de contenido dinámico ───────────────────────
        self.area_contenido = tk.Frame(marco_principal, bg=COLOR_FONDO)
        self.area_contenido.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # ── Creamos todos los paneles (páginas) ──────────────
        self.paginas = {}
        self._crear_pagina_inicio()
        self._crear_pagina_clientes()
        self._crear_pagina_servicios()
        self._crear_pagina_reservas()
        self._crear_pagina_logs()

    def _crear_encabezado(self) -> None:
        """Crea la barra superior de la aplicación."""
        encabezado = tk.Frame(self.ventana, bg=COLOR_PANEL, height=60)
        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)

        # Logo / nombre del sistema
        tk.Label(
            encabezado,
            text="◈  Software FJ",
            font=("Courier", 18, "bold"),
            fg=COLOR_ACENTO,
            bg=COLOR_PANEL
        ).pack(side="left", padx=20, pady=10)

        tk.Label(
            encabezado,
            text="Sistema Integral de Gestión de Reservas",
            font=("Courier", 10),
            fg=COLOR_TEXTO_GRIS,
            bg=COLOR_PANEL
        ).pack(side="left", padx=5, pady=10)

        # Fecha y hora en el lado derecho
        self.lbl_hora = tk.Label(
            encabezado,
            text="",
            font=("Courier", 10),
            fg=COLOR_TEXTO_GRIS,
            bg=COLOR_PANEL
        )
        self.lbl_hora.pack(side="right", padx=20)
        self._actualizar_hora()

    def _actualizar_hora(self) -> None:
        """Actualiza el reloj del encabezado cada segundo."""
        ahora = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        self.lbl_hora.configure(text=f"🕐  {ahora}")
        self.ventana.after(1000, self._actualizar_hora)

    def _crear_menu_lateral(self, padre: tk.Frame) -> None:
        """Crea el panel de navegación lateral."""
        menu = tk.Frame(padre, bg=COLOR_PANEL, width=200)
        menu.pack(side="left", fill="y", padx=(10, 0), pady=10)
        menu.pack_propagate(False)

        # Título del menú
        tk.Label(
            menu,
            text="NAVEGACIÓN",
            font=("Courier", 9, "bold"),
            fg=COLOR_TEXTO_GRIS,
            bg=COLOR_PANEL
        ).pack(pady=(20, 10), padx=15, anchor="w")

        # Opciones del menú con sus íconos y páginas destino
        opciones_menu = [
            ("🏠  Inicio",        "inicio"),
            ("👥  Clientes",      "clientes"),
            ("🛎  Servicios",     "servicios"),
            ("📋  Reservas",      "reservas"),
            ("📝  Logs del Sistema", "logs"),
        ]

        self.botones_menu = {}
        for texto, pagina in opciones_menu:
            btn = tk.Button(
                menu,
                text=texto,
                font=("Courier", 11),
                fg=COLOR_TEXTO,
                bg=COLOR_PANEL,
                activeforeground=COLOR_ACENTO,
                activebackground=COLOR_TARJETA,
                relief="flat",
                cursor="hand2",
                anchor="w",
                padx=15,
                pady=8,
                command=lambda p=pagina: self._mostrar_pagina(p)
            )
            btn.pack(fill="x", padx=5, pady=2)
            self.botones_menu[pagina] = btn

        # Separador
        tk.Frame(menu, bg=COLOR_BORDE, height=1).pack(fill="x", padx=10, pady=15)

        # Contador de registros
        self.lbl_contador = tk.Label(
            menu,
            text="",
            font=("Courier", 9),
            fg=COLOR_TEXTO_GRIS,
            bg=COLOR_PANEL,
            justify="left"
        )
        self.lbl_contador.pack(padx=15, anchor="w")
        self._actualizar_contadores()

    def _actualizar_contadores(self) -> None:
        """Actualiza los contadores del menú lateral."""
        texto = (
            f"Clientes:  {len(self.clientes)}\n"
            f"Servicios: {len(self.servicios)}\n"
            f"Reservas:  {len(self.reservas)}\n"
            f"  Activas:   {sum(1 for r in self.reservas if r.esta_activa())}"
        )
        self.lbl_contador.configure(text=texto)

    def _mostrar_pagina(self, nombre_pagina: str) -> None:
        """Oculta la página actual y muestra la nueva página seleccionada."""
        # Ocultamos todas las páginas
        for pagina in self.paginas.values():
            pagina.pack_forget()

        # Resaltamos el botón activo en el menú
        for nombre, btn in self.botones_menu.items():
            if nombre == nombre_pagina:
                btn.configure(fg=COLOR_ACENTO, bg=COLOR_TARJETA, font=("Courier", 11, "bold"))
            else:
                btn.configure(fg=COLOR_TEXTO, bg=COLOR_PANEL, font=("Courier", 11))

        # Mostramos la página seleccionada
        self.paginas[nombre_pagina].pack(fill="both", expand=True)
        self.pagina_actual = nombre_pagina

    # ============================================================
    # PÁGINA: INICIO (Dashboard)
    # ============================================================

    def _crear_pagina_inicio(self) -> None:
        """Crea el panel de inicio con resumen del sistema."""
        pagina = tk.Frame(self.area_contenido, bg=COLOR_FONDO)
        self.paginas["inicio"] = pagina

        # Título
        tk.Label(
            pagina,
            text="Panel de Control",
            font=("Courier", 20, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        ).pack(anchor="w", padx=10, pady=(10, 5))

        tk.Label(
            pagina,
            text="Bienvenido al Sistema de Gestión de Reservas — Software FJ",
            font=("Courier", 11),
            fg=COLOR_TEXTO_GRIS,
            bg=COLOR_FONDO
        ).pack(anchor="w", padx=10, pady=(0, 20))

        # ── Tarjetas de estadísticas ──────────────────────────
        marco_tarjetas = tk.Frame(pagina, bg=COLOR_FONDO)
        marco_tarjetas.pack(fill="x", padx=10, pady=5)

        # Guardamos referencias para actualizar después
        self.tarjetas_stats = {}

        datos_tarjetas = [
            ("👥", "Clientes", "clientes"),
            ("🛎", "Servicios", "servicios"),
            ("📋", "Reservas Totales", "reservas_total"),
            ("✅", "Reservas Activas", "reservas_activas"),
        ]

        for icono, titulo, clave in datos_tarjetas:
            tarjeta = self._crear_tarjeta_stat(marco_tarjetas, icono, titulo, "0")
            tarjeta.pack(side="left", padx=8, pady=5, expand=True, fill="x")
            self.tarjetas_stats[clave] = tarjeta

        # ── Sección: Accesos rápidos ──────────────────────────
        tk.Label(
            pagina,
            text="Accesos Rápidos",
            font=("Courier", 14, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        ).pack(anchor="w", padx=10, pady=(25, 10))

        marco_accesos = tk.Frame(pagina, bg=COLOR_FONDO)
        marco_accesos.pack(fill="x", padx=10)

        accesos = [
            ("➕  Registrar Cliente",  "clientes", COLOR_ACENTO),
            ("➕  Agregar Servicio",   "servicios", COLOR_ACENTO2),
            ("📋  Nueva Reserva",      "reservas",  "#9B59B6"),
            ("📝  Ver Logs",           "logs",      COLOR_TEXTO_GRIS),
        ]

        for texto, destino, color in accesos:
            tk.Button(
                marco_accesos,
                text=texto,
                font=("Courier", 11, "bold"),
                fg=COLOR_FONDO,
                bg=color,
                activeforeground=COLOR_FONDO,
                activebackground=color,
                relief="flat",
                cursor="hand2",
                padx=15,
                pady=10,
                command=lambda d=destino: self._mostrar_pagina(d)
            ).pack(side="left", padx=8)

        # ── Últimas reservas ─────────────────────────────────
        tk.Label(
            pagina,
            text="Últimas Reservas",
            font=("Courier", 14, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        ).pack(anchor="w", padx=10, pady=(25, 10))

        # Marco para la tabla de últimas reservas
        marco_tabla = tk.Frame(pagina, bg=COLOR_TARJETA, padx=2, pady=2)
        marco_tabla.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.tabla_inicio = self._crear_tabla(
            marco_tabla,
            columnas=("ID", "Cliente", "Servicio", "Costo", "Estado", "Fecha"),
            anchos=(50, 150, 180, 80, 80, 160)
        )

        self._actualizar_dashboard()

    def _crear_tarjeta_stat(self, padre, icono, titulo, valor):
        """Crea una tarjeta de estadística para el dashboard."""
        tarjeta = tk.Frame(padre, bg=COLOR_TARJETA, padx=20, pady=15)

        tk.Label(tarjeta, text=icono, font=("Courier", 22),
                 fg=COLOR_ACENTO, bg=COLOR_TARJETA).pack(anchor="w")
        lbl_valor = tk.Label(tarjeta, text=valor, font=("Courier", 28, "bold"),
                              fg=COLOR_TEXTO, bg=COLOR_TARJETA)
        lbl_valor.pack(anchor="w")
        tk.Label(tarjeta, text=titulo, font=("Courier", 10),
                 fg=COLOR_TEXTO_GRIS, bg=COLOR_TARJETA).pack(anchor="w")

        tarjeta._lbl_valor = lbl_valor  # guardamos referencia
        return tarjeta

    def _actualizar_dashboard(self) -> None:
        """Actualiza las estadísticas mostradas en el dashboard."""
        reservas_activas = sum(1 for r in self.reservas if r.esta_activa())

        # Actualizamos las tarjetas
        stats = {
            "clientes": len(self.clientes),
            "servicios": len(self.servicios),
            "reservas_total": len(self.reservas),
            "reservas_activas": reservas_activas,
        }
        for clave, valor in stats.items():
            if clave in self.tarjetas_stats:
                self.tarjetas_stats[clave]._lbl_valor.configure(text=str(valor))

        # Actualizamos tabla de últimas reservas
        for fila in self.tabla_inicio.get_children():
            self.tabla_inicio.delete(fila)

        for reserva in reversed(self.reservas[-10:]):  # últimas 10
            self.tabla_inicio.insert("", "end", values=(
                reserva.get_id(),
                reserva.get_cliente().get_nombre(),
                reserva.get_servicio().get_nombre(),
                formatear_cop(reserva.get_costo()),
                reserva.get_estado(),
                reserva.get_fecha()
            ))

        self._actualizar_contadores()

    # ============================================================
    # PÁGINA: CLIENTES
    # ============================================================

    def _crear_pagina_clientes(self) -> None:
        """Crea el panel de gestión de clientes."""
        pagina = tk.Frame(self.area_contenido, bg=COLOR_FONDO)
        self.paginas["clientes"] = pagina

        # Título de la sección
        self._crear_titulo_seccion(pagina, "👥  Gestión de Clientes")

        # ── Formulario para agregar cliente ──────────────────
        marco_form = tk.LabelFrame(
            pagina, text="  Registrar Nuevo Cliente  ",
            font=("Courier", 11, "bold"), fg=COLOR_ACENTO,
            bg=COLOR_TARJETA, padx=15, pady=10
        )
        marco_form.pack(fill="x", padx=10, pady=(0, 10))

        # Campos del formulario en grilla
        campos_clientes = [
            ("Nombre completo *", "nombre"),
            ("Correo electrónico *", "correo"),
            ("Teléfono", "telefono"),
        ]

        self.entradas_cliente = {}
        for i, (etiqueta, clave) in enumerate(campos_clientes):
            tk.Label(marco_form, text=etiqueta, font=("Courier", 10),
                     fg=COLOR_TEXTO_GRIS, bg=COLOR_TARJETA).grid(
                row=0, column=i * 2, padx=(0, 5), pady=5, sticky="w")

            entrada = tk.Entry(marco_form, font=("Courier", 11),
                               bg=COLOR_ENTRADA, fg=COLOR_TEXTO,
                               insertbackground=COLOR_TEXTO,
                               relief="flat", width=22)
            entrada.grid(row=1, column=i * 2, padx=(0, 15), pady=5, sticky="ew")
            self.entradas_cliente[clave] = entrada

        # Botón registrar
        tk.Button(
            marco_form,
            text="➕  Registrar",
            font=("Courier", 11, "bold"),
            fg=COLOR_FONDO, bg=COLOR_ACENTO,
            relief="flat", cursor="hand2",
            padx=15, pady=6,
            command=self._registrar_cliente
        ).grid(row=1, column=6, padx=10)

        # ── Tabla de clientes registrados ────────────────────
        tk.Label(pagina, text="Clientes Registrados",
                 font=("Courier", 12, "bold"),
                 fg=COLOR_TEXTO, bg=COLOR_FONDO).pack(anchor="w", padx=12, pady=(5, 5))

        marco_tabla = tk.Frame(pagina, bg=COLOR_TARJETA, padx=2, pady=2)
        marco_tabla.pack(fill="both", expand=True, padx=10, pady=(0, 5))

        self.tabla_clientes = self._crear_tabla(
            marco_tabla,
            columnas=("ID", "Nombre", "Correo", "Teléfono"),
            anchos=(50, 200, 220, 140)
        )

        # Botón eliminar (panel inferior)
        marco_botones = tk.Frame(pagina, bg=COLOR_FONDO)
        marco_botones.pack(fill="x", padx=10, pady=5)

        tk.Button(
            marco_botones,
            text="🗑  Eliminar Seleccionado",
            font=("Courier", 10),
            fg=COLOR_TEXTO, bg=COLOR_BOTON_PELIGRO,
            relief="flat", cursor="hand2", padx=10, pady=5,
            command=self._eliminar_cliente
        ).pack(side="left", padx=(0, 10))

        self._actualizar_tabla_clientes()

    def _registrar_cliente(self) -> None:
        """Valida y registra un nuevo cliente en el sistema."""
        nombre = self.entradas_cliente["nombre"].get()
        correo = self.entradas_cliente["correo"].get()
        telefono = self.entradas_cliente["telefono"].get()

        try:
            # Intentamos crear el cliente (puede lanzar ClienteInvalidoError)
            nuevo_cliente = Cliente(self.contador_clientes, nombre, correo, telefono)
            self.clientes.append(nuevo_cliente)
            self.contador_clientes += 1

            log_info(f"Cliente registrado: {nuevo_cliente}")
            self._limpiar_entradas(self.entradas_cliente)
            self._actualizar_tabla_clientes()
            self._actualizar_dashboard()
            messagebox.showinfo("✅ Éxito", f"Cliente '{nombre}' registrado correctamente.")

        except ClienteInvalidoError as e:
            # Manejamos el error de datos inválidos
            log_error(f"ClienteInvalidoError: {e}")
            messagebox.showerror("❌ Error de Validación", str(e))

        except Exception as e:
            # Capturamos cualquier otro error inesperado
            log_error(f"Error inesperado al registrar cliente: {e}")
            messagebox.showerror("❌ Error", f"Ocurrió un error inesperado:\n{e}")

    def _eliminar_cliente(self) -> None:
        """Elimina el cliente seleccionado en la tabla."""
        seleccion = self.tabla_clientes.selection()
        if not seleccion:
            messagebox.showwarning("⚠️ Aviso", "Por favor selecciona un cliente de la tabla.")
            return

        fila = self.tabla_clientes.item(seleccion[0])["values"]
        id_cliente = fila[0]
        nombre = fila[1]

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Deseas eliminar al cliente '{nombre}'?\nEsta acción no se puede deshacer."
        )
        if confirmar:
            try:
                self.clientes = [c for c in self.clientes if c.get_id() != id_cliente]
                log_advertencia(f"Cliente eliminado: ID={id_cliente}, nombre='{nombre}'")
                self._actualizar_tabla_clientes()
                self._actualizar_dashboard()
                messagebox.showinfo("✅ Éxito", f"Cliente '{nombre}' eliminado.")
            except Exception as e:
                log_error(f"Error al eliminar cliente: {e}")
                messagebox.showerror("❌ Error", str(e))

    def _actualizar_tabla_clientes(self) -> None:
        """Recarga los datos de la tabla de clientes."""
        for fila in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(fila)
        for cliente in self.clientes:
            self.tabla_clientes.insert("", "end", values=(
                cliente.get_id(),
                cliente.get_nombre(),
                cliente.get_correo(),
                cliente.get_telefono() or "—"
            ))

    # ============================================================
    # PÁGINA: SERVICIOS
    # ============================================================

    def _crear_pagina_servicios(self) -> None:
        """Crea el panel de gestión de servicios."""
        pagina = tk.Frame(self.area_contenido, bg=COLOR_FONDO)
        self.paginas["servicios"] = pagina

        self._crear_titulo_seccion(pagina, "🛎  Gestión de Servicios")

        # ── Formulario para agregar servicio ─────────────────
        marco_form = tk.LabelFrame(
            pagina, text="  Registrar Nuevo Servicio  ",
            font=("Courier", 11, "bold"), fg=COLOR_ACENTO2,
            bg=COLOR_TARJETA, padx=15, pady=10
        )
        marco_form.pack(fill="x", padx=10, pady=(0, 10))

        # Fila 1: tipo, nombre, disponible
        tk.Label(marco_form, text="Tipo de Servicio *", font=("Courier", 10),
                 fg=COLOR_TEXTO_GRIS, bg=COLOR_TARJETA).grid(row=0, column=0, sticky="w", padx=(0,5))
        tk.Label(marco_form, text="Nombre *", font=("Courier", 10),
                 fg=COLOR_TEXTO_GRIS, bg=COLOR_TARJETA).grid(row=0, column=2, sticky="w", padx=(0,5))
        tk.Label(marco_form, text="Disponible", font=("Courier", 10),
                 fg=COLOR_TEXTO_GRIS, bg=COLOR_TARJETA).grid(row=0, column=4, sticky="w", padx=(0,5))

        self.tipo_servicio = tk.StringVar(value="Reserva de Sala")
        combo_tipo = ttk.Combobox(
            marco_form,
            textvariable=self.tipo_servicio,
            values=["Reserva de Sala", "Alquiler de Equipo", "Asesoría Especializada"],
            state="readonly", width=22, font=("Courier", 11)
        )
        combo_tipo.grid(row=1, column=0, padx=(0, 15), sticky="ew")
        combo_tipo.bind("<<ComboboxSelected>>", self._cambiar_campo_extra)

        self.ent_nombre_serv = tk.Entry(marco_form, font=("Courier", 11),
                                        bg=COLOR_ENTRADA, fg=COLOR_TEXTO,
                                        insertbackground=COLOR_TEXTO, relief="flat", width=22)
        self.ent_nombre_serv.grid(row=1, column=2, padx=(0, 15), sticky="ew")

        self.var_disponible = tk.BooleanVar(value=True)
        tk.Checkbutton(
            marco_form, variable=self.var_disponible,
            text="Sí", font=("Courier", 11),
            fg=COLOR_TEXTO, bg=COLOR_TARJETA,
            activeforeground=COLOR_TEXTO, activebackground=COLOR_TARJETA,
            selectcolor=COLOR_ENTRADA
        ).grid(row=1, column=4, padx=(0, 15))

        # Fila 2: campo extra dinámico (capacidad / tipo equipo / área y factor)
        tk.Label(marco_form, text="Detalle extra", font=("Courier", 10),
                 fg=COLOR_TEXTO_GRIS, bg=COLOR_TARJETA).grid(row=2, column=0, sticky="w", pady=(8,0))

        self.lbl_extra = tk.Label(marco_form, text="Capacidad (personas)",
                                  font=("Courier", 10), fg=COLOR_TEXTO_GRIS, bg=COLOR_TARJETA)
        self.lbl_extra.grid(row=3, column=0, sticky="w", padx=(0,5))

        self.ent_extra = tk.Entry(marco_form, font=("Courier", 11),
                                  bg=COLOR_ENTRADA, fg=COLOR_TEXTO,
                                  insertbackground=COLOR_TEXTO, relief="flat", width=22)
        self.ent_extra.insert(0, "10")
        self.ent_extra.grid(row=3, column=2, padx=(0, 15), sticky="ew")

        # Botón agregar servicio
        tk.Button(
            marco_form,
            text="➕  Agregar",
            font=("Courier", 11, "bold"),
            fg=COLOR_FONDO, bg=COLOR_ACENTO2,
            relief="flat", cursor="hand2", padx=15, pady=6,
            command=self._agregar_servicio
        ).grid(row=3, column=4, padx=10)

        # ── Tabla de servicios ────────────────────────────────
        tk.Label(pagina, text="Servicios Registrados",
                 font=("Courier", 12, "bold"),
                 fg=COLOR_TEXTO, bg=COLOR_FONDO).pack(anchor="w", padx=12, pady=(5, 5))

        marco_tabla = tk.Frame(pagina, bg=COLOR_TARJETA, padx=2, pady=2)
        marco_tabla.pack(fill="both", expand=True, padx=10, pady=(0, 5))

        self.tabla_servicios = self._crear_tabla(
            marco_tabla,
            columnas=("ID", "Tipo", "Nombre", "Detalle", "Disponible", "Tarifa Base"),
            anchos=(40, 160, 180, 160, 80, 100)
        )

        # Botones inferiores
        marco_botones = tk.Frame(pagina, bg=COLOR_FONDO)
        marco_botones.pack(fill="x", padx=10, pady=5)

        tk.Button(
            marco_botones,
            text="🔄  Cambiar Disponibilidad",
            font=("Courier", 10),
            fg=COLOR_TEXTO, bg="#2980B9",
            relief="flat", cursor="hand2", padx=10, pady=5,
            command=self._cambiar_disponibilidad_servicio
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            marco_botones,
            text="🗑  Eliminar Seleccionado",
            font=("Courier", 10),
            fg=COLOR_TEXTO, bg=COLOR_BOTON_PELIGRO,
            relief="flat", cursor="hand2", padx=10, pady=5,
            command=self._eliminar_servicio
        ).pack(side="left")

        self._actualizar_tabla_servicios()

    def _cambiar_campo_extra(self, evento=None) -> None:
        """Actualiza el label del campo extra según el tipo de servicio."""
        tipo = self.tipo_servicio.get()
        self.ent_extra.delete(0, tk.END)
        if tipo == "Reserva de Sala":
            self.lbl_extra.configure(text="Capacidad (personas)")
            self.ent_extra.insert(0, "10")
        elif tipo == "Alquiler de Equipo":
            self.lbl_extra.configure(text="Tipo de equipo")
            self.ent_extra.insert(0, "Laptop")
        else:
            self.lbl_extra.configure(text="Área / Factor (ej: TI,1.5)")
            self.ent_extra.insert(0, "Tecnología,1.5")

    def _agregar_servicio(self) -> None:
        """Valida y agrega un nuevo servicio al sistema."""
        tipo = self.tipo_servicio.get()
        nombre = self.ent_nombre_serv.get().strip()
        disponible = self.var_disponible.get()
        extra = self.ent_extra.get().strip()

        if not nombre:
            messagebox.showwarning("⚠️ Aviso", "El nombre del servicio no puede estar vacío.")
            return

        try:
            if tipo == "Reserva de Sala":
                capacidad = int(extra) if extra.isdigit() else 10
                servicio = ReservaSala(self.contador_servicios, nombre, capacidad, disponible)

            elif tipo == "Alquiler de Equipo":
                tipo_equipo = extra if extra else "General"
                servicio = AlquilerEquipo(self.contador_servicios, nombre, tipo_equipo, disponible)

            else:  # Asesoría Especializada
                partes = extra.split(",")
                area = partes[0].strip() if partes else "General"
                try:
                    factor = float(partes[1].strip()) if len(partes) > 1 else 1.0
                except ValueError:
                    factor = 1.0
                servicio = AsesoriaEspecializada(
                    self.contador_servicios, nombre, area, factor, disponible
                )

            self.servicios.append(servicio)
            self.contador_servicios += 1
            log_info(f"Servicio registrado: {servicio}")

            self.ent_nombre_serv.delete(0, tk.END)
            self.ent_extra.delete(0, tk.END)
            self._cambiar_campo_extra()

            self._actualizar_tabla_servicios()
            self._actualizar_dashboard()
            messagebox.showinfo("✅ Éxito", f"Servicio '{nombre}' registrado correctamente.")

        except Exception as e:
            log_error(f"Error al registrar servicio: {e}")
            messagebox.showerror("❌ Error", f"No se pudo registrar el servicio:\n{e}")

    def _cambiar_disponibilidad_servicio(self) -> None:
        """Activa o desactiva el servicio seleccionado."""
        seleccion = self.tabla_servicios.selection()
        if not seleccion:
            messagebox.showwarning("⚠️ Aviso", "Selecciona un servicio de la tabla.")
            return

        fila = self.tabla_servicios.item(seleccion[0])["values"]
        id_serv = fila[0]

        for serv in self.servicios:
            if serv.get_id() == id_serv:
                nuevo_estado = not serv.esta_disponible()
                serv.set_disponible(nuevo_estado)
                estado_txt = "disponible" if nuevo_estado else "no disponible"
                log_info(f"Servicio '{serv.get_nombre()}' cambiado a: {estado_txt}")
                self._actualizar_tabla_servicios()
                messagebox.showinfo("✅ Actualizado",
                                    f"Servicio '{serv.get_nombre()}' ahora está {estado_txt}.")
                return

    def _eliminar_servicio(self) -> None:
        """Elimina el servicio seleccionado."""
        seleccion = self.tabla_servicios.selection()
        if not seleccion:
            messagebox.showwarning("⚠️ Aviso", "Selecciona un servicio de la tabla.")
            return

        fila = self.tabla_servicios.item(seleccion[0])["values"]
        id_serv = fila[0]
        nombre = fila[2]

        if messagebox.askyesno("Confirmar", f"¿Eliminar el servicio '{nombre}'?"):
            self.servicios = [s for s in self.servicios if s.get_id() != id_serv]
            log_advertencia(f"Servicio eliminado: ID={id_serv}, nombre='{nombre}'")
            self._actualizar_tabla_servicios()
            self._actualizar_dashboard()
            messagebox.showinfo("✅ Éxito", f"Servicio '{nombre}' eliminado.")

    def _actualizar_tabla_servicios(self) -> None:
        """Recarga los datos en la tabla de servicios."""
        for fila in self.tabla_servicios.get_children():
            self.tabla_servicios.delete(fila)

        for serv in self.servicios:
            tipo = serv.get_tipo()
            disponible = "✅ Sí" if serv.esta_disponible() else "❌ No"

            # Extraemos el detalle según el tipo
            if isinstance(serv, ReservaSala):
                detalle = f"Capacidad: {serv.get_capacidad()} pers."
            elif isinstance(serv, AlquilerEquipo):
                detalle = f"Equipo: {serv.get_tipo_equipo()}"
            elif isinstance(serv, AsesoriaEspecializada):
                detalle = f"Área: {serv.get_area()} | x{serv.get_factor()}"
            else:
                detalle = "—"

            self.tabla_servicios.insert("", "end", values=(
                serv.get_id(), tipo, serv.get_nombre(),
                detalle, disponible,
                formatear_cop(serv.calcular_costo())
            ))

    # ============================================================
    # PÁGINA: RESERVAS
    # ============================================================

    def _crear_pagina_reservas(self) -> None:
        """Crea el panel de gestión de reservas."""
        pagina = tk.Frame(self.area_contenido, bg=COLOR_FONDO)
        self.paginas["reservas"] = pagina

        self._crear_titulo_seccion(pagina, "📋  Gestión de Reservas")

        # ── Formulario para crear reserva ─────────────────────
        marco_form = tk.LabelFrame(
            pagina, text="  Crear Nueva Reserva  ",
            font=("Courier", 11, "bold"), fg="#9B59B6",
            bg=COLOR_TARJETA, padx=15, pady=10
        )
        marco_form.pack(fill="x", padx=10, pady=(0, 10))

        # Fila de etiquetas
        etiquetas = ["Cliente *", "Servicio *", "Duración (horas/días)", "Descuento (%)", "Impuesto (%)"]
        for i, texto in enumerate(etiquetas):
            tk.Label(marco_form, text=texto, font=("Courier", 10),
                     fg=COLOR_TEXTO_GRIS, bg=COLOR_TARJETA).grid(
                row=0, column=i, padx=(0, 10), pady=5, sticky="w")

        # Combo clientes
        self.var_cliente_reserva = tk.StringVar()
        self.combo_clientes_reserva = ttk.Combobox(
            marco_form, textvariable=self.var_cliente_reserva,
            state="readonly", width=20, font=("Courier", 10)
        )
        self.combo_clientes_reserva.grid(row=1, column=0, padx=(0, 10), sticky="ew")

        # Combo servicios
        self.var_servicio_reserva = tk.StringVar()
        self.combo_servicios_reserva = ttk.Combobox(
            marco_form, textvariable=self.var_servicio_reserva,
            state="readonly", width=22, font=("Courier", 10)
        )
        self.combo_servicios_reserva.grid(row=1, column=1, padx=(0, 10), sticky="ew")

        # Duración
        self.ent_horas = tk.Entry(marco_form, font=("Courier", 11),
                                   bg=COLOR_ENTRADA, fg=COLOR_TEXTO,
                                   insertbackground=COLOR_TEXTO, relief="flat", width=10)
        self.ent_horas.insert(0, "1")
        self.ent_horas.grid(row=1, column=2, padx=(0, 10))

        # Descuento
        self.ent_descuento = tk.Entry(marco_form, font=("Courier", 11),
                                       bg=COLOR_ENTRADA, fg=COLOR_TEXTO,
                                       insertbackground=COLOR_TEXTO, relief="flat", width=8)
        self.ent_descuento.insert(0, "0")
        self.ent_descuento.grid(row=1, column=3, padx=(0, 10))

        # Impuesto
        self.ent_impuesto = tk.Entry(marco_form, font=("Courier", 11),
                                      bg=COLOR_ENTRADA, fg=COLOR_TEXTO,
                                      insertbackground=COLOR_TEXTO, relief="flat", width=8)
        self.ent_impuesto.insert(0, "0")
        self.ent_impuesto.grid(row=1, column=4, padx=(0, 10))

        # Botón crear reserva
        tk.Button(
            marco_form,
            text="➕  Crear Reserva",
            font=("Courier", 11, "bold"),
            fg=COLOR_TEXTO, bg="#9B59B6",
            relief="flat", cursor="hand2", padx=15, pady=6,
            command=self._crear_reserva
        ).grid(row=1, column=5, padx=10)

        # Botón para refrescar combos
        tk.Button(
            marco_form,
            text="🔄",
            font=("Courier", 11),
            fg=COLOR_TEXTO_GRIS, bg=COLOR_TARJETA,
            relief="flat", cursor="hand2",
            command=self._actualizar_combos_reserva
        ).grid(row=0, column=5, padx=5)

        # ── Tabla de reservas ────────────────────────────────
        tk.Label(pagina, text="Reservas Registradas",
                 font=("Courier", 12, "bold"),
                 fg=COLOR_TEXTO, bg=COLOR_FONDO).pack(anchor="w", padx=12, pady=(5, 5))

        marco_tabla = tk.Frame(pagina, bg=COLOR_TARJETA, padx=2, pady=2)
        marco_tabla.pack(fill="both", expand=True, padx=10, pady=(0, 5))

        self.tabla_reservas = self._crear_tabla(
            marco_tabla,
            columnas=("ID", "Cliente", "Servicio", "Horas", "Descuento", "Impuesto", "Costo Total", "Estado", "Fecha"),
            anchos=(40, 140, 160, 55, 75, 70, 90, 75, 155)
        )

        # Botones inferiores
        marco_botones = tk.Frame(pagina, bg=COLOR_FONDO)
        marco_botones.pack(fill="x", padx=10, pady=5)

        tk.Button(
            marco_botones,
            text="❌  Cancelar Reserva",
            font=("Courier", 10),
            fg=COLOR_TEXTO, bg=COLOR_BOTON_PELIGRO,
            relief="flat", cursor="hand2", padx=10, pady=5,
            command=self._cancelar_reserva
        ).pack(side="left", padx=(0, 10))

        # Costo total de reservas activas
        self.lbl_costo_total = tk.Label(
            marco_botones,
            text="",
            font=("Courier", 11, "bold"),
            fg=COLOR_ACENTO, bg=COLOR_FONDO
        )
        self.lbl_costo_total.pack(side="right", padx=10)

        self._actualizar_combos_reserva()
        self._actualizar_tabla_reservas()

    def _actualizar_combos_reserva(self) -> None:
        """Actualiza las listas desplegables de clientes y servicios."""
        nombres_clientes = [f"{c.get_id()} - {c.get_nombre()}" for c in self.clientes]
        self.combo_clientes_reserva["values"] = nombres_clientes
        if nombres_clientes:
            self.combo_clientes_reserva.current(0)

        nombres_servicios = [
            f"{s.get_id()} - {s.get_nombre()} ({'✅' if s.esta_disponible() else '❌'})"
            for s in self.servicios
        ]
        self.combo_servicios_reserva["values"] = nombres_servicios
        if nombres_servicios:
            self.combo_servicios_reserva.current(0)

    def _crear_reserva(self) -> None:
        """Crea una nueva reserva con manejo de excepciones."""
        try:
            # Obtenemos los datos seleccionados
            cliente_sel = self.var_cliente_reserva.get()
            servicio_sel = self.var_servicio_reserva.get()

            if not cliente_sel or not servicio_sel:
                raise ReservaInvalidaError("Debes seleccionar un cliente y un servicio.")

            # Extraemos el ID del texto del combo (formato: "ID - Nombre")
            id_cliente = int(cliente_sel.split(" - ")[0])
            id_servicio = int(servicio_sel.split(" - ")[0])

            # Buscamos los objetos en memoria
            cliente = next((c for c in self.clientes if c.get_id() == id_cliente), None)
            servicio = next((s for s in self.servicios if s.get_id() == id_servicio), None)

            if cliente is None:
                raise ClienteNoEncontradoError(f"No se encontró el cliente con ID {id_cliente}.")

            # Validamos duración
            try:
                horas = int(self.ent_horas.get())
            except ValueError:
                raise ReservaInvalidaError("La duración debe ser un número entero.")

            # Validamos descuento e impuesto
            try:
                descuento = float(self.ent_descuento.get())
                impuesto = float(self.ent_impuesto.get())
            except ValueError:
                raise ReservaInvalidaError("El descuento e impuesto deben ser números.")

            if not (0 <= descuento <= 100) or not (0 <= impuesto <= 100):
                raise ReservaInvalidaError("El descuento e impuesto deben estar entre 0 y 100.")

            # Creamos la reserva (puede lanzar ServicioNoDisponibleError)
            nueva_reserva = Reserva(
                self.contador_reservas, cliente, servicio,
                horas, descuento, impuesto
            )
            self.reservas.append(nueva_reserva)
            self.contador_reservas += 1

            log_info(f"Reserva creada: {nueva_reserva}")
            self._actualizar_tabla_reservas()
            self._actualizar_dashboard()
            messagebox.showinfo(
                "✅ Reserva Creada",
                f"Reserva creada exitosamente.\n"
                f"Cliente: {cliente.get_nombre()}\n"
                f"Servicio: {servicio.get_nombre()}\n"
                f"Costo total: {formatear_cop(nueva_reserva.get_costo())}"
            )

        except ServicioNoDisponibleError as e:
            log_error(f"ServicioNoDisponibleError: {e}")
            messagebox.showerror("❌ Servicio No Disponible", str(e))

        except ReservaInvalidaError as e:
            log_error(f"ReservaInvalidaError: {e}")
            messagebox.showerror("❌ Reserva Inválida", str(e))

        except ClienteNoEncontradoError as e:
            log_error(f"ClienteNoEncontradoError: {e}")
            messagebox.showerror("❌ Cliente No Encontrado", str(e))

        except Exception as e:
            log_error(f"Error inesperado al crear reserva: {e}")
            messagebox.showerror("❌ Error", f"Error inesperado:\n{e}")

    def _cancelar_reserva(self) -> None:
        """Cancela la reserva seleccionada en la tabla."""
        seleccion = self.tabla_reservas.selection()
        if not seleccion:
            messagebox.showwarning("⚠️ Aviso", "Selecciona una reserva de la tabla.")
            return

        fila = self.tabla_reservas.item(seleccion[0])["values"]
        id_reserva = fila[0]

        try:
            reserva = next((r for r in self.reservas if r.get_id() == id_reserva), None)
            if reserva is None:
                raise ReservaNoEncontradaError(f"No se encontró la reserva con ID {id_reserva}.")

            if messagebox.askyesno("Confirmar", f"¿Cancelar la reserva #{id_reserva}?"):
                reserva.cancelar()  # puede lanzar ReservaYaCanceladaError
                log_info(f"Reserva #{id_reserva} cancelada exitosamente.")
                self._actualizar_tabla_reservas()
                self._actualizar_dashboard()
                messagebox.showinfo("✅ Cancelada", f"Reserva #{id_reserva} cancelada.")

        except ReservaYaCanceladaError as e:
            log_error(f"ReservaYaCanceladaError: {e}")
            messagebox.showerror("❌ Error", str(e))

        except ReservaNoEncontradaError as e:
            log_error(f"ReservaNoEncontradaError: {e}")
            messagebox.showerror("❌ Error", str(e))

        except Exception as e:
            log_error(f"Error inesperado al cancelar reserva: {e}")
            messagebox.showerror("❌ Error", str(e))

    def _actualizar_tabla_reservas(self) -> None:
        """Recarga la tabla de reservas y el costo total."""
        for fila in self.tabla_reservas.get_children():
            self.tabla_reservas.delete(fila)

        costo_total = 0.0
        for reserva in self.reservas:
            costo = reserva.get_costo()
            if reserva.esta_activa():
                costo_total += costo

            self.tabla_reservas.insert("", "end", values=(
                reserva.get_id(),
                reserva.get_cliente().get_nombre(),
                reserva.get_servicio().get_nombre(),
                reserva.get_horas(),
                f"{reserva.get_descuento():.1f}%",
                f"{reserva.get_impuesto():.1f}%",
                formatear_cop(costo),
                reserva.get_estado(),
                reserva.get_fecha()
            ))

        self.lbl_costo_total.configure(
            text=f"💰 Total activas: {formatear_cop(costo_total)}"
        )

    # ============================================================
    # PÁGINA: LOGS
    # ============================================================

    def _crear_pagina_logs(self) -> None:
        """Crea el panel de visualización de logs del sistema."""
        pagina = tk.Frame(self.area_contenido, bg=COLOR_FONDO)
        self.paginas["logs"] = pagina

        self._crear_titulo_seccion(pagina, "📝  Logs del Sistema")

        # Panel de texto para mostrar los logs
        marco_logs = tk.Frame(pagina, bg=COLOR_TARJETA, padx=2, pady=2)
        marco_logs.pack(fill="both", expand=True, padx=10, pady=(0, 5))

        self.area_logs = scrolledtext.ScrolledText(
            marco_logs,
            font=("Courier", 10),
            bg="#0D1B2A",
            fg="#00FF41",         # verde terminal clásico
            insertbackground=COLOR_TEXTO,
            relief="flat",
            wrap="word"
        )
        self.area_logs.pack(fill="both", expand=True)

        # Colores para diferentes niveles de log
        self.area_logs.tag_configure("INFO", foreground="#00FF41")
        self.area_logs.tag_configure("ERROR", foreground="#FF4444")
        self.area_logs.tag_configure("ADVERTENCIA", foreground="#FFA500")
        self.area_logs.tag_configure("ENCABEZADO", foreground="#00C9A7", font=("Courier", 10, "bold"))

        # Botones inferiores
        marco_botones = tk.Frame(pagina, bg=COLOR_FONDO)
        marco_botones.pack(fill="x", padx=10, pady=5)

        tk.Button(
            marco_botones,
            text="🔄  Actualizar Logs",
            font=("Courier", 10),
            fg=COLOR_FONDO, bg=COLOR_ACENTO,
            relief="flat", cursor="hand2", padx=10, pady=5,
            command=self._cargar_logs
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            marco_botones,
            text="🗑  Limpiar Logs",
            font=("Courier", 10),
            fg=COLOR_TEXTO, bg=COLOR_BOTON_PELIGRO,
            relief="flat", cursor="hand2", padx=10, pady=5,
            command=self._limpiar_logs
        ).pack(side="left")

        self._cargar_logs()

    def _cargar_logs(self) -> None:
        """Carga y muestra el contenido del archivo de logs con colores."""
        self.area_logs.configure(state="normal")
        self.area_logs.delete("1.0", tk.END)

        contenido = obtener_logs()
        self.area_logs.insert(tk.END, "═" * 60 + "\n", "ENCABEZADO")
        self.area_logs.insert(tk.END, "  HISTORIAL DE LOGS — Software FJ\n", "ENCABEZADO")
        self.area_logs.insert(tk.END, "═" * 60 + "\n\n", "ENCABEZADO")

        for linea in contenido.split("\n"):
            if "[INFO]" in linea:
                self.area_logs.insert(tk.END, linea + "\n", "INFO")
            elif "[ERROR]" in linea:
                self.area_logs.insert(tk.END, linea + "\n", "ERROR")
            elif "[ADVERTENCIA]" in linea:
                self.area_logs.insert(tk.END, linea + "\n", "ADVERTENCIA")
            else:
                self.area_logs.insert(tk.END, linea + "\n")

        self.area_logs.configure(state="disabled")
        self.area_logs.see(tk.END)

    def _limpiar_logs(self) -> None:
        """Limpia el archivo de logs tras confirmación del usuario."""
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar todos los logs del sistema?"):
            limpiar_logs()
            self._cargar_logs()
            messagebox.showinfo("✅ Éxito", "Los logs han sido eliminados.")

    # ============================================================
    # UTILIDADES GENERALES DE LA INTERFAZ
    # ============================================================

    def _crear_titulo_seccion(self, padre: tk.Frame, texto: str) -> None:
        """Crea un título estilizado para cada sección/página."""
        marco = tk.Frame(padre, bg=COLOR_FONDO)
        marco.pack(fill="x", padx=10, pady=(5, 10))

        tk.Label(
            marco,
            text=texto,
            font=("Courier", 16, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        ).pack(side="left")

        # Línea decorativa
        tk.Frame(marco, bg=COLOR_ACENTO, height=2).pack(
            side="left", fill="x", expand=True, padx=(15, 0), pady=8
        )

    def _crear_tabla(self, padre: tk.Frame, columnas: tuple, anchos: tuple) -> ttk.Treeview:
        """
        Crea una tabla (Treeview) con estilo personalizado.
        Retorna el objeto Treeview para manipularlo después.
        """
        # Estilo de la tabla
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Custom.Treeview",
                         background=COLOR_TARJETA,
                         foreground=COLOR_TEXTO,
                         fieldbackground=COLOR_TARJETA,
                         rowheight=28,
                         font=("Courier", 10))
        estilo.configure("Custom.Treeview.Heading",
                         background=COLOR_PANEL,
                         foreground=COLOR_ACENTO,
                         font=("Courier", 10, "bold"),
                         relief="flat")
        estilo.map("Custom.Treeview",
                   background=[("selected", COLOR_ACENTO)],
                   foreground=[("selected", COLOR_FONDO)])

        # Scrollbar vertical
        scroll = ttk.Scrollbar(padre, orient="vertical")
        scroll.pack(side="right", fill="y")

        tabla = ttk.Treeview(
            padre,
            columns=columnas,
            show="headings",
            yscrollcommand=scroll.set,
            style="Custom.Treeview"
        )
        scroll.configure(command=tabla.yview)

        # Configuramos columnas
        for col, ancho in zip(columnas, anchos):
            tabla.heading(col, text=col)
            tabla.column(col, width=ancho, minwidth=40, anchor="center")

        tabla.pack(fill="both", expand=True)
        return tabla

    def _limpiar_entradas(self, entradas: dict) -> None:
        """Limpia todos los campos de entrada de un formulario."""
        for entrada in entradas.values():
            entrada.delete(0, tk.END)

    # ============================================================
    # DATOS INICIALES DE DEMOSTRACIÓN
    # ============================================================

    def _cargar_datos_iniciales(self) -> None:
        """
        Carga datos de ejemplo para demostrar las funcionalidades.
        Simula las 10+ operaciones requeridas por la actividad.
        Incluye casos válidos e inválidos con manejo de excepciones.
        """
        log_info("=" * 50)
        log_info("INICIO DEL SISTEMA — Software FJ")
        log_info("=" * 50)

        # ── Op. 1: Clientes válidos ──────────────────────────
        try:
            c1 = Cliente(self.contador_clientes, "Ana García", "ana@email.com", "3001234567")
            self.clientes.append(c1)
            self.contador_clientes += 1
            log_info(f"Operación 1 — Cliente registrado: {c1}")
        except ClienteInvalidoError as e:
            log_error(f"Operación 1 fallida: {e}")

        try:
            c2 = Cliente(self.contador_clientes, "Luis Pérez", "luis@email.com", "3109876543")
            self.clientes.append(c2)
            self.contador_clientes += 1
            log_info(f"Operación 1 — Cliente registrado: {c2}")
        except ClienteInvalidoError as e:
            log_error(f"Operación 1 fallida: {e}")

        try:
            c3 = Cliente(self.contador_clientes, "María López", "maria@email.com", "")
            self.clientes.append(c3)
            self.contador_clientes += 1
            log_info(f"Operación 1 — Cliente registrado: {c3}")
        except ClienteInvalidoError as e:
            log_error(f"Operación 1 fallida: {e}")

        # ── Op. 2: Cliente con datos inválidos ───────────────
        log_info("Operación 2 — Intentando crear cliente inválido...")
        try:
            c_invalido = Cliente(99, "", "")
            self.clientes.append(c_invalido)
        except ClienteInvalidoError as e:
            log_error(f"Operación 2 — ClienteInvalidoError: {e}")

        # ── Op. 2b: Correo sin @ ─────────────────────────────
        try:
            c_invalido2 = Cliente(100, "Test User", "correo-sin-arroba")
            self.clientes.append(c_invalido2)
        except ClienteInvalidoError as e:
            log_error(f"Operación 2b — ClienteInvalidoError (correo inválido): {e}")

        # ── Op. 3: Servicios válidos ─────────────────────────
        try:
            s1 = ReservaSala(self.contador_servicios, "Sala Innovación", capacidad=20)
            self.servicios.append(s1)
            self.contador_servicios += 1
            log_info(f"Operación 3 — Servicio registrado: {s1}")
        except Exception as e:
            log_error(f"Operación 3 fallida: {e}")

        try:
            s2 = ReservaSala(self.contador_servicios, "Sala Reuniones A", capacidad=8)
            self.servicios.append(s2)
            self.contador_servicios += 1
            log_info(f"Operación 3 — Servicio registrado: {s2}")
        except Exception as e:
            log_error(f"Operación 3 fallida: {e}")

        # ── Op. 4: Equipos y asesorías ───────────────────────
        try:
            s3 = AlquilerEquipo(self.contador_servicios, "Laptop Dell XPS", tipo_equipo="Laptop")
            self.servicios.append(s3)
            self.contador_servicios += 1
            log_info(f"Operación 4 — Servicio registrado: {s3}")
        except Exception as e:
            log_error(f"Operación 4 fallida: {e}")

        try:
            s4 = AsesoriaEspecializada(
                self.contador_servicios, "Asesoría en IA",
                area="Inteligencia Artificial", factor_especialidad=2.5
            )
            self.servicios.append(s4)
            self.contador_servicios += 1
            log_info(f"Operación 4 — Servicio registrado: {s4}")
        except Exception as e:
            log_error(f"Operación 4 fallida: {e}")

        # Servicio NO disponible
        try:
            s5 = ReservaSala(
                self.contador_servicios, "Sala VIP", capacidad=5, disponible=False
            )
            self.servicios.append(s5)
            self.contador_servicios += 1
            log_advertencia(f"Operación 4 — Servicio creado como NO disponible: {s5}")
        except Exception as e:
            log_error(f"Operación 4 fallida: {e}")

        # ── Op. 5: Reservas válidas ──────────────────────────
        if len(self.clientes) >= 1 and len(self.servicios) >= 1:
            try:
                r1 = Reserva(self.contador_reservas, self.clientes[0], self.servicios[0], horas=3)
                self.reservas.append(r1)
                self.contador_reservas += 1
                log_info(f"Operación 5 — Reserva creada: {r1}")
            except Exception as e:
                log_error(f"Operación 5 fallida: {e}")

        if len(self.clientes) >= 2 and len(self.servicios) >= 3:
            try:
                r2 = Reserva(
                    self.contador_reservas, self.clientes[1], self.servicios[3],
                    horas=2, descuento=10.0, impuesto=5.0
                )
                self.reservas.append(r2)
                self.contador_reservas += 1
                log_info(f"Operación 5 — Reserva con descuento creada: {r2}")
            except Exception as e:
                log_error(f"Operación 5 fallida: {e}")

        # ── Op. 6: Reservar servicio NO disponible ───────────
        log_info("Operación 6 — Intentando reservar servicio no disponible...")
        if len(self.clientes) >= 3 and len(self.servicios) >= 5:
            try:
                r_mala = Reserva(99, self.clientes[2], self.servicios[4])
                self.reservas.append(r_mala)
            except ServicioNoDisponibleError as e:
                log_error(f"Operación 6 — ServicioNoDisponibleError: {e}")

        # ── Op. 7: Reserva con duración inválida ─────────────
        log_info("Operación 7 — Intentando reserva con 0 horas...")
        if len(self.clientes) >= 1 and len(self.servicios) >= 1:
            try:
                r_inv = Reserva(98, self.clientes[0], self.servicios[0], horas=0)
                self.reservas.append(r_inv)
            except ReservaInvalidaError as e:
                log_error(f"Operación 7 — ReservaInvalidaError: {e}")

        # ── Op. 8: Cancelar una reserva ──────────────────────
        if self.reservas:
            try:
                self.reservas[0].cancelar()
                log_info(f"Operación 8 — Reserva #{self.reservas[0].get_id()} cancelada.")
            except Exception as e:
                log_error(f"Operación 8 fallida: {e}")

        # ── Op. 9: Cancelar reserva ya cancelada ─────────────
        log_info("Operación 9 — Intentando cancelar reserva ya cancelada...")
        if self.reservas:
            try:
                self.reservas[0].cancelar()  # ya fue cancelada en Op. 8
            except ReservaYaCanceladaError as e:
                log_error(f"Operación 9 — ReservaYaCanceladaError: {e}")
            finally:
                log_info("Operación 9 — Bloque finally ejecutado (sistema sigue activo).")

        # ── Op. 10: Buscar cliente inexistente ───────────────
        log_info("Operación 10 — Buscando cliente inexistente (ID=9999)...")
        try:
            cliente_buscado = next(
                (c for c in self.clientes if c.get_id() == 9999), None
            )
            if cliente_buscado is None:
                raise ClienteNoEncontradoError("No se encontró el cliente con ID 9999.")
        except ClienteNoEncontradoError as e:
            log_error(f"Operación 10 — ClienteNoEncontradoError: {e}")

        # ── Op. 11: Cálculo total con polimorfismo ───────────
        activas = [r for r in self.reservas if r.esta_activa()]
        total = sum(r.get_costo() for r in activas)
        log_info(f"Operación 11 — Costo total de {len(activas)} reserva(s) activa(s): {formatear_cop(total)}")

        # ── Op. 12: Encadenamiento de excepciones ────────────
        log_info("Operación 12 — Demostración de encadenamiento de excepciones...")
        try:
            try:
                raise ValueError("Error de valor en la operación base.")
            except ValueError as e:
                raise ReservaInvalidaError("Error derivado de operación inválida.") from e
        except ReservaInvalidaError as e:
            log_error(f"Operación 12 — Excepción encadenada capturada: {e} (causa: {e.__cause__})")

        log_info("=" * 50)
        log_info("Sistema iniciado correctamente. Todas las operaciones completadas.")
        log_info("=" * 50)


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================

if __name__ == "__main__":
    # Creamos la ventana principal de Tkinter
    ventana = tk.Tk()

    # Iniciamos la aplicación
    app = AplicacionSoftwareFJ(ventana)

    # Iniciamos el bucle principal de la interfaz
    ventana.mainloop()
