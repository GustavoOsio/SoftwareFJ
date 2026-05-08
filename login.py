import tkinter as tk
from tkinter import messagebox

ventana = tk.Tk()

ventana.title("Login - Software FJ")
ventana.geometry("500x400")
ventana.configure(bg="#1C2B3A")
ventana.resizable(False, False)

titulo = tk.Label(
    ventana,
    text="Software FJ",
    font=("Courier", 24, "bold"),
    fg="#00C9A7",
    bg="#1C2B3A"
)

titulo.pack(pady=40)

lbl_usuario = tk.Label(
    ventana,
    text="Usuario",
    font=("Courier", 12),
    fg="white",
    bg="#1C2B3A"
)

lbl_usuario.pack(pady=5)

entrada_usuario = tk.Entry(
    ventana,
    font=("Courier", 12),
    width=25
)

entrada_usuario.pack(pady=5)

lbl_clave = tk.Label(
    ventana,
    text="Contraseña",
    font=("Courier", 12),
    fg="white",
    bg="#1C2B3A"
)

lbl_clave.pack(pady=5)

entrada_clave = tk.Entry(
    ventana,
    font=("Courier", 12),
    width=25,
    show="*"
)

entrada_clave.pack(pady=5)

def iniciar_sesion():

    usuario = entrada_usuario.get()
    clave = entrada_clave.get()

    if usuario == "admin" and clave == "1234":

        ventana.destroy()

        import main

    else:
        messagebox.showerror(
            "Error",
            "Usuario o contraseña incorrectos"
        )

btn_login = tk.Button(
    ventana,
    text="Iniciar Sesión",
    font=("Courier", 12, "bold"),
    bg="#00C9A7",
    fg="black",
    padx=10,
    pady=5,
    command=iniciar_sesion
)

btn_login.pack(pady=30)

ventana.mainloop()
