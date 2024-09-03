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
    
#***********************************************************Funciones y vista del usuario administrador************************************************************
def obtener_usuarios():
    conexion = get_db_conexion()
    cursor = conexion.cursor()
    sql= 'SELECT * FROM usuarios ORDER BY codigo ASC'
    cursor.execute(sql)
    usuarios = cursor.fetchall()
    conexion.commit()
    conexion.close()
    return usuarios

def validar_formulario():
        if len(lbl_tipo_doc.get()) !=0 and len(lbl_numero_doc.get()) !=0 and len(lbl_nombre.get()) !=0 and len(lbl_apellido.get()) !=0 and len(lbl_telefono.get()) !=0 and len(lbl_usuario_info.get()) !=0 and len(lbl_contrasena_info.get()) !=0 and len(lbl_email.get()) !=0 and len(lbl_rol.get()):
            return True
        else:
             messagebox.showerror("ERROR", "Complete todos los campos del formulario")

def validar_registrar():
        conexion = get_db_conexion()
        cursor = conexion.cursor()
        parameters= (lbl_numero_doc.get(),)
        sql="SELECT * FROM usuarios WHERE numero_doc = %s"
        cursor.execute(sql,parameters)
        dato = cursor.fetchall()
        conexion.commit()
        conexion.close()

        if not dato:
            return True
        else:
            messagebox.showerror("ERROR EN REGISTRO", "Usuario registrado")
            return False
        
def limpiar_formulario():
    lbl_tipo_doc.delete(0,END)
    lbl_numero_doc.delete(0,END)
    lbl_nombre.delete(0,END)
    lbl_apellido.delete(0,END)
    lbl_telefono.delete(0,END)
    lbl_usuario_info.delete(0,END)
    lbl_contrasena_info.delete(0,END)
    lbl_email.delete(0,END)
    lbl_rol.delete(0,END)



def agregar_usuario():
        if validar_formulario() and validar_registrar():
            conexion = get_db_conexion()
            cursor = conexion.cursor()
            sql='INSERT INTO usuarios (tipo_doc, numero_doc, nombre, apellido, usuario, contrasena, telefono, correo, rol) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            parameters = (lbl_tipo_doc.get(),lbl_numero_doc.get(),lbl_nombre.get(),lbl_apellido.get(),lbl_telefono.get(),lbl_usuario_info.get(),lbl_contrasena_info.get(),lbl_email.get(),lbl_rol.get())
            print("sql=",sql)
            print("parametros=",parameters)
            cursor.execute(sql, parameters)
            conexion.commit()
            messagebox.showinfo("REGISTRO EXITOSO", f'Usuario registrado: {lbl_nombre.get()}')
            print('REGISTRADO')
            conexion.close()
            limpiar_formulario()
            obtener_usuarios()
            

def editar_usuario(tree):
    try:
        seleccionado = tree.focus()
        codigo = tree.item(seleccionado)["values"][0]
        numero_doc = tree.item(seleccionado)["values"][1]
        nombre = tree.item(seleccionado)["values"][2]
        apellido = tree.item(seleccionado)["values"][3]
        telefono = tree.item(seleccionado)["values"][4]
        usuario = tree.item(seleccionado)["values"][5]
        contrasena = tree.item(seleccionado)["values"][6]
        email = tree.item(seleccionado)["values"][7]
        rol = tree.item(seleccionado)["values"][8]
    except IndexError:
        messagebox.showerror("ERROR","Porfavor selecciona un elemento") 
        return
    
    ventana_editar = Toplevel()
    ventana_editar.title('EDITAR PRODUCTO')
    ventana_editar.resizable(0,0)

    #Tipo Documento
    Label(ventana_editar, text="Tipo documento:", font=(" ",10,"bold")).grid(row=0,column=0,sticky="s",padx=5,pady=8)
    global nuevo_tipo_doc
    nuevo_tipo_doc = Entry(ventana_editar, width=25)
    nuevo_tipo_doc.grid(row=0,column=1,padx=5,pady=8)

    #Número del Documento
    Label(ventana_editar, text="Número del documento:", font=(" ",10,"bold")).grid(row=1,column=0,sticky="s",padx=5,pady=8)
    global nuevo_numero_doc
    nuevo_numero_doc = Entry(ventana_editar, width=25)
    nuevo_numero_doc.focus()
    nuevo_numero_doc.grid(row=1,column=1,padx=5,pady=8)

    #Nombre del Usuario
    Label(ventana_editar, text="Nombre:", font=(" ",10,"bold")).grid(row=2,column=0,sticky="s",padx=5,pady=8)
    global nuevo_nombre
    nuevo_nombre = Entry(ventana_editar, width=25)
    nuevo_nombre.grid(row=2,column=1,padx=5,pady=8)

    #Apellido del Usuario
    Label(ventana_editar, text="Apellido:", font=(" ",10,"bold")).grid(row=3,column=0,sticky="s",padx=5,pady=8)
    global nuevo_apellido
    nuevo_apellido = Entry(ventana_editar, width=25)
    nuevo_apellido.grid(row=3,column=1,padx=5,pady=8)

    #Teléfono del Usuario
    Label(ventana_editar, text="Teléfono:", font=(" ",10,"bold")).grid(row=4,column=0,sticky="s",padx=5,pady=8)
    global nuevo_telefono
    nuevo_telefono = Entry(ventana_editar, width=25)
    nuevo_telefono.grid(row=4,column=1,padx=5,pady=8)

    #Usuario del Usuario
    Label(ventana_editar, text="Usuario:", font=(" ",10,"bold")).grid(row=0,column=2,sticky="s",padx=5,pady=8)
    global nuevo_usuario_info
    nuevo_usuario_info = Entry(ventana_editar, width=25)
    nuevo_usuario_info.grid(row=0,column=3,padx=5,pady=8)

    #Contraseña del Usuario
    Label(ventana_editar, text="Contrasena:", font=(" ",10,"bold")).grid(row=1,column=2,sticky="s",padx=5,pady=8)
    global nuevo_contrasena_info
    nuevo_contrasena_info = Entry(ventana_editar, width=25)
    nuevo_contrasena_info.grid(row=1,column=3,padx=5,pady=8)

    #Correo del Usuario
    Label(ventana_editar, text="Email:", font=(" ",10,"bold")).grid(row=2,column=2,sticky="s",padx=5,pady=8)
    global nuevo_email
    nuevo_email = Entry(ventana_editar, width=25)
    nuevo_email.grid(row=2,column=3,padx=5,pady=8)

    #Rol del Usuario
    Label(ventana_editar, text="Rol:", font=(" ",10,"bold")).grid(row=3,column=2,sticky="s",padx=5,pady=9)
    global nuevo_rol
    nuevo_rol = ttk.Combobox(ventana_editar, values=["Administrador", "Empacador","Transportador", "Recepcionista"], width=22)
    nuevo_rol.current(0)
    nuevo_rol.grid(row=3,column=3,padx=5,pady=8)

    boton_actualizar=Button(ventana_editar,text="ACTUALIZAR",command= lambda: actualizar(nuevo_codigo.get(),nuevo_nombre.get(),nuevo_combo_categoria.get(),nueva_cantidad.get(),nuevo_precio.get(),nueva_descripcion.get(),codigo,nombre),height=2,width=20,bg="black",fg="white",font=("Comic Sans", 10,"bold"))
    boton_actualizar.grid(row=3, column=1,columnspan=2, padx=10, pady=15)
        
    ventana_editar.mainloop()  
        

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
    admin_window.geometry("900x600")
    admin_window.title("COMERCIALIZADORA GREMLINS")
    admin_window.resizable(0,0)
    admin_window.config(bd=50)
    titulo = Label(admin_window, text="COMERCIALIZADORA GREMLINS", fg="black", font=(" ", 17, "bold"),pady=10).pack()
    marcoAdmin = LabelFrame(admin_window, text="Información de usuario", font=("", 10, "bold"),pady=5, padx=50)
    marcoAdmin.config(bd=2)
    marcoAdmin.pack()

    #Formulario información de usuario
    #Tipo Documento
    Label(marcoAdmin, text="Tipo documento:", font=(" ",10,"bold")).grid(row=0,column=0,sticky="s",padx=5,pady=8)
    global lbl_tipo_doc
    lbl_tipo_doc = Entry(marcoAdmin, width=25)
    lbl_tipo_doc.grid(row=0,column=1,padx=5,pady=8)

    #Número del Documento
    Label(marcoAdmin, text="Número del documento:", font=(" ",10,"bold")).grid(row=1,column=0,sticky="s",padx=5,pady=8)
    global lbl_numero_doc
    lbl_numero_doc = Entry(marcoAdmin, width=25)
    lbl_numero_doc.focus()
    lbl_numero_doc.grid(row=1,column=1,padx=5,pady=8)

    #Nombre del Usuario
    Label(marcoAdmin, text="Nombre:", font=(" ",10,"bold")).grid(row=2,column=0,sticky="s",padx=5,pady=8)
    global lbl_nombre
    lbl_nombre = Entry(marcoAdmin, width=25)
    lbl_nombre.grid(row=2,column=1,padx=5,pady=8)

    #Apellido del Usuario
    Label(marcoAdmin, text="Apellido:", font=(" ",10,"bold")).grid(row=3,column=0,sticky="s",padx=5,pady=8)
    global lbl_apellido
    lbl_apellido = Entry(marcoAdmin, width=25)
    lbl_apellido.grid(row=3,column=1,padx=5,pady=8)

    #Teléfono del Usuario
    Label(marcoAdmin, text="Teléfono:", font=(" ",10,"bold")).grid(row=4,column=0,sticky="s",padx=5,pady=8)
    global lbl_telefono
    lbl_telefono = Entry(marcoAdmin, width=25)
    lbl_telefono.grid(row=4,column=1,padx=5,pady=8)

    #Usuario del Usuario
    Label(marcoAdmin, text="Usuario:", font=(" ",10,"bold")).grid(row=0,column=2,sticky="s",padx=5,pady=8)
    global lbl_usuario_info
    lbl_usuario_info = Entry(marcoAdmin, width=25)
    lbl_usuario_info.grid(row=0,column=3,padx=5,pady=8)

    #Contraseña del Usuario
    Label(marcoAdmin, text="Contrasena:", font=(" ",10,"bold")).grid(row=1,column=2,sticky="s",padx=5,pady=8)
    global lbl_contrasena_info
    lbl_contrasena_info = Entry(marcoAdmin, width=25)
    lbl_contrasena_info.grid(row=1,column=3,padx=5,pady=8)

    #Correo del Usuario
    Label(marcoAdmin, text="Email:", font=(" ",10,"bold")).grid(row=2,column=2,sticky="s",padx=5,pady=8)
    global lbl_email
    lbl_email = Entry(marcoAdmin, width=25)
    lbl_email.grid(row=2,column=3,padx=5,pady=8)

    #Rol del Usuario
    Label(marcoAdmin, text="Rol:", font=(" ",10,"bold")).grid(row=3,column=2,sticky="s",padx=5,pady=9)
    global lbl_rol
    lbl_rol = ttk.Combobox(marcoAdmin, values=["Administrador", "Empacador","Transportador", "Recepcionista"], width=22)
    lbl_rol.current(0)
    lbl_rol.grid(row=3,column=3,padx=5,pady=8)

    #Botones
    #Crear botones
    btn_frame = Frame(admin_window)
    btn_frame.pack()
    # btn_frame.grid(row=2,column=0,padx=5,pady=5)

    
    btn_agregar = Button(btn_frame, text="Agregar",command=lambda: agregar_usuario(),height=2,width=12,bg="green",fg="white",font=(" ", 10,"bold"))
    btn_agregar.grid(row=0,column=0,padx=10,pady=5)

    btn_editar = Button(btn_frame, text="Editar", command=lambda: editar_usuario(tree),height=2,width=12,bg="yellow",fg="black",font=(" ", 10,"bold"))
    btn_editar.grid(row=0, column=1,padx=10,pady=5)

    btn_eliminar = Button(btn_frame, text="Eliminar", command=lambda: eliminar_usuario(seleccionar_usuario(tree)),height=2,width=12,bg="red",fg="white",font=(" ", 10,"bold"))
    btn_eliminar.grid(row=0, column=2,padx=10,pady=5)



    # Crear tabla
    tree = ttk.Treeview(admin_window, columns=("codigo", "tipo_doc", "numero_doc", "nombre", "apellido", "usuario","contrasena", "telefono", "correo", "rol"), show="headings")
    tree.heading("codigo", text="Código", anchor=CENTER)
    tree.heading("tipo_doc", text="Tipo Documento", anchor=CENTER)
    tree.heading("numero_doc", text="Número Documento", anchor=CENTER)
    tree.heading("nombre", text="Nombre", anchor=CENTER)
    tree.heading("apellido", text="Apellido", anchor=CENTER)
    tree.heading("usuario", text="Usuario", anchor=CENTER)
    tree.heading("contrasena", text="contrasena", anchor=CENTER)
    tree.heading("telefono", text="Teléfono", anchor=CENTER)
    tree.heading("correo", text="Correo", anchor=CENTER)
    tree.heading("rol", text="Rol", anchor=CENTER)
    tree.pack(side=LEFT, fill=BOTH, expand=True)
    
    # Definir el ancho de columnas
    tree.column("codigo", width=50, stretch=NO)
    tree.column("tipo_doc", width=50, stretch=NO)
    tree.column("numero_doc", width=80, stretch=NO)
    tree.column("nombre", width=80, stretch=NO)
    tree.column("apellido", width=80, stretch=NO)
    tree.column("usuario", width=80, stretch=NO)
    tree.column("contrasena", width=80, stretch=NO)
    tree.column("telefono", width=80, stretch=NO)
    tree.column("correo", width=100, stretch=NO)
    tree.column("rol", width=80, stretch=NO)
    
    # Obtener usuarios y llenar la tabla
    usuarios = obtener_usuarios()
    for usuario in usuarios:
        tree.insert("", "end", values=usuario)
    
    admin_window.mainloop()

def login():
    usuario = lbl_usuario.get()
    contrasena = lbl_contrasena.get()
    arreglo = inicio_sesion(usuario,contrasena)
    # print(arreglo)
    
    if arreglo:
        messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
        rol = arreglo[9]
        # print(f"Rol de usuario:{rol}")
        login_window.destroy()
        if rol == "Administrador":
            vista_admin()
        elif rol == "Empacador":
            # vista_empacador()
            vista_admin()
        elif rol == "Transportador":
            # vista_transportador()
            vista_admin()       
        elif rol == "Recepcionista":
            # vista_recepcionista()
            vista_admin()
        else:
            messagebox.showerror("Error", "rol de usuario incorrecto")
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        

def main():
    global login_window
    login_window = Tk()
    login_window.geometry("900x600")
    #Título del aplicativo
    login_window.title("COMERCIALIZADORA GREMLINS")
    login_window.resizable(0,0)
    login_window.config(bd=50)
    #Creación del título de la ventana titulo
    titulo = Label(login_window, text="COMERCIALIZADORA GREMLINS", fg="black", font=(" ", 17, "bold"),pady=30).pack()
    #Creación de un marco
    marco = LabelFrame(login_window, text="Inicio de sesión", font=("", 10, "bold"),pady=5, padx=50)
    marco.config(bd=2)
    marco.pack()

    #Formulario usuario y contraseña
    Label(marco, text="Usuario:").pack(pady=5)
    global lbl_usuario
    lbl_usuario = Entry(marco)
    lbl_usuario.pack(pady=5)

    Label(marco, text="Contraseña:").pack(pady=5)
    global lbl_contrasena
    lbl_contrasena = Entry(marco, show='*')
    lbl_contrasena.pack(pady=5)

    Button(marco, text="Iniciar sesión", command=login).pack(pady=20)

    login_window.mainloop()

if __name__ == '__main__':
    main()