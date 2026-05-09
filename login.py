import tkinter as tk
from tkinter import messagebox


class LoginApp:

    def __init__(self, on_login_success=None):
        self.on_login_success = on_login_success

        self.ventana = tk.Tk()

        self.ventana.title("Login - Software FJ")
        self.ventana.geometry("500x400")
        self.ventana.configure(bg="#1C2B3A")
        self.ventana.resizable(False, False)

        # -------- CENTRAR VENTANA --------

        ancho_ventana = 500
        alto_ventana = 400

        pantalla_ancho = self.ventana.winfo_screenwidth()
        pantalla_alto = self.ventana.winfo_screenheight()

        x = int((pantalla_ancho / 2) - (ancho_ventana / 2))
        y = int((pantalla_alto / 2) - (alto_ventana / 2))

        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        # -------- LOGO --------

        self.logo = tk.PhotoImage(file="logo.png")
        self.logo = self.logo.subsample(2, 2)

        lbl_logo = tk.Label(
            self.ventana,
            image=self.logo,
            bg="#1C2B3A"
        )

        lbl_logo.pack(pady=10)

        # -------- TITULO --------

        titulo = tk.Label(
            self.ventana,
            text="Software FJ",
            font=("Courier", 24, "bold"),
            fg="#00C9A7",
            bg="#1C2B3A"
        )

        titulo.pack(pady=20)

        # -------- USUARIO --------

        lbl_usuario = tk.Label(
            self.ventana,
            text="Usuario",
            font=("Courier", 12),
            fg="white",
            bg="#1C2B3A"
        )

        lbl_usuario.pack(pady=5)

        self.entrada_usuario = tk.Entry(
            self.ventana,
            font=("Courier", 12),
            width=25,
            bg="#243447",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        self.entrada_usuario.pack(pady=5)
        self.entrada_usuario.focus()

        # -------- CONTRASEÑA --------

        lbl_clave = tk.Label(
            self.ventana,
            text="Contraseña",
            font=("Courier", 12),
            fg="white",
            bg="#1C2B3A"
        )

        lbl_clave.pack(pady=5)

        self.entrada_clave = tk.Entry(
            self.ventana,
            font=("Courier", 12),
            width=25,
            show="*",
            bg="#243447",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        self.entrada_clave.pack(pady=5)

        self.mostrar_clave = False

        # -------- MOSTRAR / OCULTAR --------

        self.btn_mostrar = tk.Button(
            self.ventana,
            text="Mostrar",
            font=("Arial", 10),
            bg="#243447",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.mostrar_ocultar_clave
        )

        self.btn_mostrar.pack(pady=5)

        # -------- LOGIN --------

        btn_login = tk.Button(
            self.ventana,
            text="Iniciar Sesión",
            font=("Courier", 12, "bold"),
            bg="#00C9A7",
            fg="#1C2B3A",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.iniciar_sesion
        )

        btn_login.pack(pady=20)

        self.ventana.bind("<Return>", lambda event: self.iniciar_sesion())

    # ---------------------------------------

    def mostrar_ocultar_clave(self):

        if self.mostrar_clave:

            self.entrada_clave.config(show="*")
            self.btn_mostrar.config(text="Mostrar")

            self.mostrar_clave = False

        else:

            self.entrada_clave.config(show="")
            self.btn_mostrar.config(text="Ocultar")

            self.mostrar_clave = True

    # ---------------------------------------

    def iniciar_sesion(self):

        usuario = self.entrada_usuario.get().strip()
        clave = self.entrada_clave.get().strip()

        if usuario == "admin" and clave == "1234":

            self.ventana.destroy()

            if self.on_login_success:
                self.on_login_success()

        else:

            messagebox.showerror(
                "Error",
                "Usuario o contraseña incorrectos"
            )

    # ---------------------------------------

    def ejecutar(self):
        self.ventana.mainloop()
