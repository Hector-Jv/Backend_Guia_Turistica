import re
from flask import request
from flask_jwt_extended import create_access_token
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import fields, Schema
from app import db
from app.models import Usuario, TipoUsuario
import cloudinary.uploader

class RegistroUsuarioSchema(Schema):
    correo = fields.String(required=True, description="Correo del usuario.")
    usuario = fields.String(required=True, description="Nombre del usuario.")
    contrasena = fields.String(required=True, description="Contraseña del usuario.")
    foto_usuario = fields.String(required=False, description="Fotografía de usuario. (multipart/form-data)")

class RegistroUsuarioResponseSchema(Schema):
    access_token = fields.String(description="Token de acceso.")
    usuario = fields.String(description="Nombre del usuario.")
    tipo_usuario = fields.String(description="Tipo de usuario.")
    link_imagen = fields.String(description="Link de la foto del usuario.")


registrar_usuario_bp = Blueprint('Registrar usuario', __name__, description="""Registro de usuario. 

                                 Esta ruta acepta una petición POST multipart/form-data.
                                 """)


@registrar_usuario_bp.route('/registro')
class Registro(MethodView):
    
    @registrar_usuario_bp.arguments(RegistroUsuarioSchema, location='form')
    @registrar_usuario_bp.response(200, RegistroUsuarioResponseSchema)
    @registrar_usuario_bp.response(400, description="Sintaxis inválida.")
    def post(self):
        ## DATOS ##
        correo = request.form['correo']
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        
        ## VALIDACIONES ##
        
        if not correo or not usuario or not contrasena:
            abort(400, message="Hacen falta datos.")
            
        formato_correo = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(formato_correo, correo):
            abort(400, message="El correo ingresado no es válido.")
            
        formato_contrasena = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$'
        if not re.match(formato_contrasena, contrasena):
            abort(400, message="La contraseña debe contener al menos 8 caracteres, una letra mayúscula, un número y un carácter especial.")
            
        if Usuario.query.get(correo):
            abort(400, message="Ya existe el correo ingresado.")
        
        if Usuario.query.filter_by(usuario=usuario).first():
            abort(400, message="Ya existe el usuario ingresado.")
            
        ## MANEJO DE IMAGEN ##
        link_foto = None
        if 'foto_usuario' in request.files:
            foto = request.files['foto_usuario']
            if foto.filename != '':
                # VALIDACIONES #
                extensiones_validas = {'png', 'jpg', 'jpeg', 'gif'}
                if not '.' in foto.filename and not foto.filename.rsplit('.', 1)[1].lower() in extensiones_validas:
                    abort(400, message="La imagen no tiene una extensión válida.")
                
                # SE SUBE LA IMAGEN #
                upload_result = cloudinary.uploader.upload(foto)
                link_foto = upload_result['secure_url']
                
        try:
            nuevo_usuario = Usuario(
                correo_usuario = correo,
                usuario = usuario,
                contrasena = contrasena,
                link_imagen = link_foto
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
        except Exception as e:
            abort(400, message="Error al crear al usuario.")
                   
        ## Se obtienen los datos del usuario ##
        access_token = create_access_token(identity=nuevo_usuario.correo_usuario)
        print(access_token)
        tipo_usuario: TipoUsuario = TipoUsuario.query.get(nuevo_usuario.cve_tipo_usuario)
        
        return {
            "access_token": access_token, 
            "usuario": nuevo_usuario.usuario, 
            "tipo_usuario": tipo_usuario.tipo_usuario, 
            "link_imagen": link_foto
        }