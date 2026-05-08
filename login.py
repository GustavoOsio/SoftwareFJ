import tkinter as tk
from tkinter import messagebox

ventana = tk.Tk()

ventana.title("Login - Software FJ")
ventana.geometry("500x400")
ventana.configure(bg="#1C2B3A")
ventana.resizable(False, False)

# ------ CENTRAR VENTANA --------

ancho_ventana = 500
alto_ventana = 400

pantalla_ancho = ventana. winfo_screenwidth()
pantalla_alto = ventana.winfo_screenheight()

x = int((pantalla_ancho / 2) - (ancho_ventana / 2))
y = int((pantalla_alto / 2) - (alto_ventana / 2))

ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

titulo = tk.Label(
    ventana,
    text="Software FJ",
    font=("Courier", 24, "bold"),
    fg="#00C9A7",
    bg="#1C2B3A"
)

titulo.pack(pady=40)

# -------- USUARIO -----------

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
    width=25,
    bg="#243447",
    fg="white",
    insertbackground="white",
    relief="flat"
    )

entrada_usuario.pack(pady=5)

# --------- CONTRASEÑA ----------------

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
    show="*",
    bg="#243447",
    fg="white",
    insertbackground="white",
    relief="flat"
)

entrada_clave.pack(pady=5)

mostrar_clave = False

# --------- MOSTRAR OCULTAR CONTRASEÑA ----------------

def mostrar_ocultar_clave():
    
    global mostrar_clave
    
    if mostrar_clave:
    
        entrada_clave.config(show="*")
        btn_mostrar.config(text="Mostrar")
        
        mostrar_clave = False
        
    else:
        entrada_clave.config(show="")
        btn_mostrar.config(text="Ocultar")
        
        mostrar_clave = True
        
btn_mostrar = tk.Button(
    ventana,
    text="Mostrar",
    font=("Arial", 10),
    bg="#243447",
    fg="white",
    relief="flat",
    cursor="hand2",
    command=mostrar_ocultar_clave
)

btn_mostrar.pack(pady=5)

# ------------- LOGIN ------------------

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
