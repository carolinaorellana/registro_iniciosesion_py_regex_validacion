from aplicacion.config.mysqlconnection import connectToMySQL #siempre importar la conección con la base de datos
from flask import flash
from flask_bcrypt import Bcrypt
from aplicacion import app
import re

bycrypt =Bcrypt(app)

patron_nombreyapellido=re.compile(r'[a-zA-Z]+')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z._-]+\.[a-zA-Z]+$')

class Usuario:

    base_datos="esquema_login_y_registro"

    def __init__(self, data):
        self.id=data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.correo = data['correo']
        self.contrasena = data['contrasena']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    #CREAR USUARIO EN LA BASE DE DATOS
    @classmethod
    def registrar_usuario(cls,data):
        consulta= """INSERT INTO usuarios (nombre, apellido, correo, contrasena, created_at, updated_at) VALUES (%(nombre)s, %(apellido)s,%(correo)s,%(contrasena)s, NOW(), NOW())"""
        resultado= connectToMySQL(cls.base_datos).query_db(consulta,data)
        return resultado
    
    @classmethod
    def revisar_correo_existente(cls, data):
        consulta = "SELECT * FROM usuarios WHERE correo = %(correo)s"
        resultado= connectToMySQL (cls.base_datos).query_db(consulta,data)
        # print(resultado, "ESTO IMPRIM EL CLASSMETHOD")
        if len(resultado) <1:
            return False
        #return resultado
        return cls(resultado[0])

    @staticmethod
    def validacion_registro(formulario_registro):
        is_valid = True # asumimos que esto es true
        if len(formulario_registro['nombre']) < 2:
            flash("Tu Nombre debe contar con al menos 2 caracteres", 'registro')
            is_valid = False
        #validando que los caracteres utilizados sean acorde al patron definido:
        if not re.fullmatch(patron_nombreyapellido, formulario_registro['nombre']):
            flash("Tu Nombre sólo debe contar letras (en mayusculas y/o minisculas)", 'registro')
            is_valid = False
        if len(formulario_registro['apellido']) < 2:
            flash("Tu Apellido debe contar con al menos 2 caracteres.", 'registro')
            is_valid = False
        #validando que los caracteres utilizados sean acorde al patron definido:
        if not re.fullmatch(patron_nombreyapellido, formulario_registro['apellido']):
            flash("Tu Apellido sólo debe contar letras (en mayusculas y/o minisculas)", 'registro')
        # ACA EL DEL CORREO
        if not EMAIL_REGEX.match(formulario_registro['correo']): 
            flash("Correo ingresado invalido", 'registro')
            is_valid = False
        if Usuario.revisar_correo_existente(formulario_registro):
            flash("Correo ya registrado, inicia sesion", 'registro')
            is_valid = False
        #contrasena
        if len(formulario_registro['contrasena']) < 8:
            flash("Tu contraseña debe contar con al menos 8 caracteres.", 'registro')
            is_valid = False
        if not re.search(r'[0-9]', formulario_registro['contrasena']):
            flash("Tu contraseña debe contar con al menos 1 numero (0-9)", 'registro')
            is_valid = False
        if not re.search(r'[A-Z]', formulario_registro['contrasena']):
            flash("Tu contraseña debe contar con al menos una letra en mayusculas", 'registro')
            is_valid = False

        #confirmar contraseña igual a la anterior:
        if formulario_registro['contrasena'] != formulario_registro['confirmar']:
            flash("Las contraseñas no coinciden!!", "registro")
            is_valid = False
        return is_valid

    @staticmethod
    def validacion_login(formulario_login):
        is_valid = True 
        if not EMAIL_REGEX.match(formulario_login['correo']): 
            flash("Correo ingresado invalido", 'login')
            is_valid = False
        
        if not Usuario.revisar_correo_existente(formulario_login):
            flash("Correo no registrado, registrate", 'login')
            is_valid = False
        
        elif not bycrypt.check_password_hash( Usuario.revisar_correo_existente(formulario_login).contrasena, formulario_login['contrasena']):
        # si obtenemos False después de verificar la contraseña
            flash("contraseña invalida", "login")
            is_valid=False
        return is_valid
