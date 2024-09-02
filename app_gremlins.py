#!/usr/bin/python3
from tkinter import *
from tkinter import messagebox, ttk
#Importar librería para la conexión con base de datos.
import mysql.connector


# Conexión a la base de datos
def get_db_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="proyecto_comercializadoragremlins"
    )
    return conexion
#Se comprueba el usuario y contraseña para iniciar sesión
def inicio_sesion(usuario,contrasena):
    try:
        conexion = get_db_conexion()
        mycursor = conexion.cursor()
        sql = "SELECT * FROM usuarios WHERE usuario = %s AND contrasena = %s"
        mycursor.execute(sql,(usuario,contrasena))
        arreglo = mycursor.fetchone()
        conexion.close()
        if arreglo:
            return arreglo
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    
# Funciones y vista del usuario administrador
def obtener_usuarios():
    conexion = get_db_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conexion.close()
    return usuarios

def editar_usuario(codigo):
    # Aquí podrías abrir una nueva ventana para editar los datos del usuario
    messagebox.showinfo("Editar", f"Editar usuario con código: {codigo}")

def eliminar_usuario(codigo):
    conexion = get_db_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuarios WHERE codigo = %s", (codigo,))
    conexion.commit()
    conexion.close()
    messagebox.showinfo("Eliminado", "Usuario eliminado correctamente")
    vista_admin()

def seleccionar_usuario(tree):
    seleccionado = tree.focus()
    if seleccionado:
        codigo = tree.item(seleccionado)["values"][0]
        return codigo
    else:
        messagebox.showwarning("Seleccionar", "Por favor selecciona un usuario")


def vista_admin():
    global admin_window
    admin_window = Tk()
    # index_window = Toplevel()
    admin_window.geometry("800x500")
    admin_window.title("Vista Administrador")

    # Crear tabla
    tree = ttk.Treeview(admin_window, columns=("codigo", "tipo_doc", "numero_doc", "nombre", "apellido", "usuario","contrasena", "telefono", "correo", "rol"), show="headings")
    tree.heading("codigo", text="Código")
    tree.heading("tipo_doc", text="Tipo Documento")
    tree.heading("numero_doc", text="Número Documento")
    tree.heading("nombre", text="Nombre")
    tree.heading("apellido", text="Apellido")
    tree.heading("usuario", text="Usuario")
    tree.heading("contrasena", text="contrasena")
    tree.heading("telefono", text="Teléfono")
    tree.heading("correo", text="Correo")
    tree.heading("rol", text="Rol")
    tree.pack(side=LEFT, fill=BOTH, expand=True)
    
    # Definir el ancho de columnas
    tree.column("codigo", width=50, stretch=NO)
    tree.column("tipo_doc", width=50, stretch=NO)
    tree.column("numero_doc", width=70, stretch=NO)
    tree.column("nombre", width=100, stretch=NO)
    tree.column("apellido", width=100, stretch=NO)
    tree.column("usuario", width=100, stretch=NO)
    tree.column("contrasena", width=50, stretch=NO)
    tree.column("telefono", width=50, stretch=NO)
    tree.column("correo", width=50, stretch=NO)
    tree.column("rol", width=50, stretch=NO)
    
    # Obtener usuarios y llenar la tabla
    usuarios = obtener_usuarios()
    for usuario in usuarios:
        tree.insert("", "end", values=usuario)
    
    # Crear botones
    btn_frame = Frame(admin_window)
    btn_frame.pack(fill=X)

    btn_editar = Button(admin_window, text="Editar", command=lambda: editar_usuario(seleccionar_usuario(tree)))
    btn_editar.pack(side=LEFT, padx=10, pady=5, fill=X, expand=True)

    btn_eliminar = Button(admin_window, text="Eliminar", command=lambda: eliminar_usuario(seleccionar_usuario(tree)))
    btn_eliminar.pack(side=RIGHT, padx=10, pady=5, fill=X, expand=True)
    
    admin_window.mainloop()

def login():
    usuario = lbl_usuario.get()
    contrasena = lbl_contrasena.get()
    arreglo = inicio_sesion(usuario,contrasena)
    print(arreglo)
    
    if arreglo:
        messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
        rol = arreglo[9]
        print(f"Rol de usuario:{rol}")
        login_window.destroy()
        if rol == "admin":
            vista_admin()
        elif rol == "empacador":
            # vista_empacador()
            vista_admin()
        elif rol == "transportador":
            # vista_transportador()
            vista_admin()       
        elif rol == "recepcionista":
            # vista_recepcionista()
            vista_admin()
        else:
            messagebox.showerror("Error", "rol de usuario incorrecto")
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        

def main():
    global login_window
    login_window = Tk()
    login_window.geometry("800x500")
    login_window.title("Inicio de Sesión")

    Label(login_window, text="Usuario:").pack(pady=5)
    global lbl_usuario
    lbl_usuario = Entry(login_window)
    lbl_usuario.pack(pady=5)

    Label(login_window, text="Contraseña:").pack(pady=5)
    global lbl_contrasena
    lbl_contrasena = Entry(login_window, show='*')
    lbl_contrasena.pack(pady=5)

    Button(login_window, text="Iniciar sesión", command=login).pack(pady=20)

    login_window.mainloop()

if __name__ == '__main__':
    main()