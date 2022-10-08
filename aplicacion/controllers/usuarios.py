from aplicacion import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from aplicacion.models.usuario import Usuario
bycrypt =Bcrypt(app)

@app.route('/')
def inicio():
    session['login']==False
    return render_template("inicio.html")

@app.route('/bienvenido/<int:id>')
def bienvenido_segun_id(id):
    print(id)
    if session['login']==True:
        return render_template("welcome.html")
    else:
        return redirect ('/') 

#RUTA FORMULARIO DE REGISTRO
@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    # aca va la validacion:
    if not Usuario.validacion_registro(request.form):
        return redirect("/")
    #contraena hash:
    pw_hash=bycrypt.generate_password_hash(request.form["contrasena"])
    print(pw_hash)
    data={
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'correo': request.form['correo'],
        'contrasena': pw_hash
    }
    usuario_id=Usuario.registrar_usuario(data) 
    #traquear al usuario
    session['usuario_id']= usuario_id
    session['usuario_nombre']= data['nombre']
    #esta es para saber que si session login es true ya se inicio la sesion de algun registrado
    session['login']=True
    return redirect (f"/bienvenido/{usuario_id}")

#RUTA INICIO DE SESION
@app.route('/login', methods=['POST'])
def iniciar_usuario():
    # pw_hash=bycrypt.generate_password_hash(request.form["contrasena"])
    # print(pw_hash)
    data ={
        'correo': request.form['correo'],
        'contrasena': request.form['contrasena']
    }
    print(data, " DATA DEL ROUTE")
    if not Usuario.validacion_login(data):
        return redirect("/")
    else:
        usuario_existente=Usuario.revisar_correo_existente(data)
        # print(usuario_existente, "ESTO TENGO QUE LEER")
        # print(usuario_existente[0]['id'], "ESTE ES EL ID")
        session['usuario_id']= usuario_existente.id
        session['usuario_nombre']= usuario_existente.nombre
        #esta es para saber que si session login es true ya se inicio la sesion de algun registrado
        session['login']=True
        return redirect (f"/bienvenido/{usuario_existente.id}")

#RUTA CERRAR SESION
@app.route("/cerrar_sesión")
def cerrar_sesión():
    session.clear()
    session['login']=False
    return redirect ("/")

