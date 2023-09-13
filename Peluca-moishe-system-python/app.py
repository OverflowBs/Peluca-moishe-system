#--------------------------------------------------------------------
from flask import Flask, render_template, request, redirect, flash
from flaskext.mysql import MySQL
from datetime import datetime
import os

#--------------------------------------------------------------------

# Creamos la aplicación
app = Flask(__name__) 
app.secret_key = 'aplicacionDelRuso'

#--------------------------------------------------------------------

#Parametros
database = "bhocwgxnnjmfqcmhrc1i"
nombreApellidoUsuarioLogueado = ""
errorLogIn = ""

#--------------------------------------------------------------------

#Clase para usuario logueado


#--------------------------------------------------------------------

# Creamos la conexión con la base de datos:
mysql = MySQL()
# Creamos la referencia al host, para que se conecte a la base
# de datos MYSQL utilizamos el host localhost
app.config['MYSQL_DATABASE_HOST']='bhocwgxnnjmfqcmhrc1i-mysql.services.clever-cloud.com' 
# Indicamos el usuario, por defecto es user
app.config['MYSQL_DATABASE_USER']='uywodavtoil562jo' 
# Sin contraseña, se puede omitir
app.config['MYSQL_DATABASE_PASSWORD']="VCd1dfWY2oaSgZ3QYBvA"
# Nombre de nuestra BD
app.config['MYSQL_DATABASE_BD']=database
# Creamos la conexión con los datos
mysql.init_app(app)

#--------------------------------------------------------------------
# Guardamos la ruta de la carpeta "uploads" en nuestra app
CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA

#--------------------------------------------------------------------
# Proporcionamos la ruta a la raiz del sitio
# @app.route('/', methods=["GET", "POST"]) 
# def index_old():
#     # Creamos una variable que va a contener la consulta sql:
#     sql = "SELECT * FROM " + database + ".USUARIOS"    
#     # Nos conectamos a la base de datos 
#     conn = mysql.connect()    
#     # Sobre el cursor vamos a realizar las operaciones
#     cursor = conn.cursor()     
#     # Ejecutamos la sentencia SQL sobre el cursor
#     cursor.execute(sql)     
#     # Copiamos el contenido del cursor a una variable
#     db_empleados = cursor.fetchall()
#     # "Commiteamos" (Cerramos la conexión)
#     conn.commit()     
#     # Devolvemos código HTML para ser renderizado
#     return render_template('index.html', empleados = db_empleados)

#--------------------------------------------------------------------
@app.route('/', methods=["GET", "POST"])
def index():

    errorLogIn = ""
    global nombreApellidoUsuarioLogueado

    if request.method == "POST":
        email = request.form.get("txtEmail")
        contraseña = request.form.get("txtContraseña")

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT ID, NOMBRE, APELLIDO, EMAIL, ROL, FECHA_REGISTRO FROM bhocwgxnnjmfqcmhrc1i.USUARIOS WHERE EMAIL=%s AND CONTRASEÑA=%s", (email, contraseña))
        usuario = cursor.fetchall()
        cantRegistros = cursor.rowcount
        conn.commit()

        if(cantRegistros > 0):
            errorLogIn = ""
            nombreApellidoUsuarioLogueado = usuario[0][1] + " " + usuario[0][2]
            return render_template('menu.html', nombreApellidoUsuarioLogueado = nombreApellidoUsuarioLogueado)
        else:
            errorLogIn = "Email y/o Contraseña incorrectos."
        
    return render_template('index.html', error = errorLogIn)


@app.route('/usuarios', methods=["GET", "POST"])
def usuarios():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT EMAIL, NOMBRE, APELLIDO, CONTRASEÑA, TELEFONO, ROL FROM bhocwgxnnjmfqcmhrc1i.USUARIOS ORDER BY APELLIDO")
    usuarios = cursor.fetchall()
    cursor.execute("SELECT DISTINCT ROL FROM bhocwgxnnjmfqcmhrc1i.PERMISOS ORDER BY ROL")
    roles = cursor.fetchall()
    conn.commit()

    return render_template('usuarios.html', nombreApellidoUsuarioLogueado = nombreApellidoUsuarioLogueado, usuarios = usuarios, roles = roles)


@app.route('/clientes', methods=["GET", "POST"])
def clientes():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT EMAIL, NOMBRE, APELLIDO, TELEFONO FROM bhocwgxnnjmfqcmhrc1i.CLIENTES ORDER BY APELLIDO")
    clientes = cursor.fetchall()
    conn.commit()

    return render_template('clientes.html', clientes = clientes, nombreApellidoUsuarioLogueado = nombreApellidoUsuarioLogueado)


@app.route('/trabajos', methods=["GET", "POST"])
def trabajos():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bhocwgxnnjmfqcmhrc1i.APP_TRABAJOS_EN_PROCESO")
    trabajosEnProceso = cursor.fetchall()
    conn.commit()

    return render_template('trabajos.html', trabajosEnProceso = trabajosEnProceso, nombreApellidoUsuarioLogueado = nombreApellidoUsuarioLogueado)


@app.route('/turnos')
def turnos():

    return render_template('turnos.html', nombreApellidoUsuarioLogueado = nombreApellidoUsuarioLogueado)



# #--------------------------------------------------------------------
# #--------------------------------------------------------------------
# FUNCIONALIDAD
# #--------------------------------------------------------------------
# #--------------------------------------------------------------------


# #--------------------------------------------------------------------
# CARGA DE USUARIOS
@app.route('/cargaUsuarios', methods=["GET", "POST"])
def cargaUsuarios():

    email = str(request.form.get("formUsuarioEmail"))
    contraseña = request.form.get("formUsuarioContraseña")
    rol = request.form.get("formUsuarioRol")
    nombre = request.form.get("formUsuarioNombre")
    apellido = request.form.get("formUsuarioApellido")
    celular = request.form.get("formUsuarioCelular")

    if email.find('@') == -1:
        flash(u'Debe ingresar una dirección de mail correcta.', 'error')
    elif contraseña.__len__ > 10 or contraseña.__len__ < 6:
        flash(u'La contraseña debe tener entre 6 y 10 caracteres.', 'error')
    else:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM bhocwgxnnjmfqcmhrc1i.USUARIOS WHERE EMAIL=%s", email)
        cursor.fetchall()
        cantRegistros = cursor.rowcount
        
        if cantRegistros > 0:
            flash(u'Ya existe un usuario con la dirección de email indicada.', 'error')
        else:
            cursor.execute("INSERT INTO bhocwgxnnjmfqcmhrc1i.USUARIOS VALUES(%s, %s, %s, %s, %s, %d, %s", nombre, apellido, email, contraseña, celular, datetime.date, rol)
            flash(u'Usuario creado exitosamente!', 'info')

        conn.commit()
    
    return redirect('/usuarios')






# #--------------------------------------------------------------------
# # Función para eliminar un registro
# @app.route('/destroy/<int:id>')
# def destroy(id):
#     conn = mysql.connect()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM `sistema`.`empleados` WHERE id=%s", (id))
#     conn.commit()
#     return redirect('/')

# #--------------------------------------------------------------------
# # Función para editar un registro
# @app.route('/edit/<int:id>')
# def edit(id):
#     conn = mysql.connect()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM `sistema`.`empleados` WHERE id=%s", (id))
#     empleados=cursor.fetchall()
#     conn.commit()
#     return render_template('empleados/edit.html', empleados=empleados)

# #--------------------------------------------------------------------
# # Función para actualizar los datos de un registro
# @app.route('/update', methods=['POST'])
# def update():
#     # Recibimos los valores del formulario y los pasamos a variables locales:
#     _nombre = request.form['txtNombre']
#     _correo = request.form['txtCorreo']
#     _foto = request.files['txtFoto']    
#     id = request.form['txtID']
    
#     # Armamos la sentencia SQL que va a actualizar los datos en la DB:
#     sql = "UPDATE `sistema`.`empleados` SET `nombre`=%s, `correo`=%s WHERE id=%s;"
#     # Y la tupa correspondiente
#     datos = (_nombre,_correo,id)
    
#     conn = mysql.connect()
#     cursor = conn.cursor()
    
#     # Guardamos en now los datos de fecha y hora
#     now = datetime.now()
    
#     # Y en tiempo almacenamos una cadena con esos datos
#     tiempo= now.strftime("%Y%H%M%S")

#     #Si el nombre de la foto ha sido proporcionado en el form...
#     if _foto.filename != '':
#         # Creamos el nombre de la foto y la guardamos.
#         nuevoNombreFoto = tiempo + _foto.filename
#         _foto.save("uploads/" + nuevoNombreFoto)
        
#         # Buscamos el registro y buscamos el nombre de la foto vieja:
#         cursor.execute("SELECT foto FROM `sistema`.`empleados` WHERE id=%s", id)
#         fila= cursor.fetchall()
        
#         # Y la borramos de la carpeta:
#         os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        
#         # Finalmente, actualizamos la DB con el nuevo nombre del archivo:
#         cursor.execute("UPDATE `sistema`.`empleados` SET foto=%s WHERE id=%s;", (nuevoNombreFoto, id))
#         conn.commit()
        
#     cursor.execute(sql, datos)
#     conn.commit()
#     return redirect('/')





# #--------------------------------------------------------------------
# # Función para crear un registro nuevo.
# @app.route('/create')
# def create():
#     return render_template('empleados/create.html')

# #--------------------------------------------------------------------
# #Función para almacenar los datos de un usuario.
# @app.route('/store', methods=['POST'])
# def storage():
#     # Recibimos los valores del formulario y los pasamos a variables locales:
#     _nombre = request.form['txtNombre']
#     _correo = request.form['txtCorreo']
#     _foto = request.files['txtFoto']
    
#     # Guardamos en now los datos de fecha y hora
#     now = datetime.now()
    
#     # Y en tiempo almacenamos una cadena con esos datos
#     tiempo = now.strftime("%Y%H%M%S") 
    
#     #Si el nombre de la foto ha sido proporcionado en el form...
#     if _foto.filename!='':
#         #...le cambiamos el nombre.
#         nuevoNombreFoto=tiempo+_foto.filename 
#         # Guardamos la foto en la carpeta uploads.
#         _foto.save("uploads/"+nuevoNombreFoto)
    
#     # Y armamos una tupla con esos valores:
#     datos = (_nombre,_correo, nuevoNombreFoto)
        
#     # Armamos la sentencia SQL que va a almacenar estos datos en la DB:
#     sql = "INSERT INTO `sistema`.`empleados` \
#           (`id`, `nombre`, `correo`, `foto`) \
#           VALUES (NULL, %s, %s, %s);"

#     conn = mysql.connect()     # Nos conectamos a la base de datos 
#     cursor = conn.cursor()     # En cursor vamos a realizar las operaciones
#     cursor.execute(sql, datos) # Ejecutamos la sentencia SQL en el cursor
#     conn.commit()              # Hacemos el commit
#     return redirect('/')       # Volvemos a index.html




#--------------------------------------------------------------------
# Estas líneas de código las requiere python para que 
# se pueda empezar a trabajar con la aplicación
if __name__=='__main__':
    #Corremos la aplicación en modo debug
    app.run(debug=True) 
#--------------------------------------------------------------------