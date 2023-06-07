from flask import request
from flask_jwt_extended import create_access_token
from flask.views import MethodView
from flask_smorest import Blueprint, abort, fields
from marshmallow import Schema, fields
from app.models import Usuario, TipoUsuario

"""
class LoginSchema(Schema):
    correo = fields.String(required=True, description="Correo del usuario.")
    contrasena = fields.String(required=True, description="Contraseña del usuario.")
    
class LoginResponseSchema(Schema):
    access_token = fields.String(description="Token de acceso del usuario.")
    usuario = fields.String(description="Nombre del usuario.")
    tipo_usuario = fields.String(description="Tipo del usuario.")
    link_imagen = fields.String(description="Link de la imagen del usuario.")
"""

iniciar_sesion_bp = Blueprint('Iniciar sesion', __name__, description="Inicio de sesión de usuario registrado y administrador.")

@iniciar_sesion_bp.route('/login')
class Login(MethodView):
    
    """
    @iniciar_sesion_bp.arguments(LoginSchema, location='json')
    @iniciar_sesion_bp.response(200, LoginResponseSchema, description="Inicio de sesión exitoso.")
    @iniciar_sesion_bp.response(400, description="Correo y/o contraseña faltantes o acceso no autorizado.")
    @iniciar_sesion_bp.response(404, description="El correo no se encuentra registrado.")
    @iniciar_sesion_bp.response(401, description="Contraseña incorrecta.")
    """
    
    def post(self):
        
        ## Datos recibidos del usuario ##
        data = request.get_json()
        correo: str = data.get('correo')
        contrasena: str = data.get('contrasena')
        
        ## Validacion ##
        if not correo or not contrasena:
            abort(400, message="Correo y contraseña requeridos.")

        usuario_encontrado: Usuario = Usuario.query.get(correo)
        if usuario_encontrado is None:
            abort(404, message="El correo no se encuentra registrado.")
        if not usuario_encontrado.verificar_contrasena(contrasena):
            abort(401, message="Contraseña incorrecta.")
        
        ## Se obtienen los datos del usuario ##
        access_token = create_access_token(identity=usuario_encontrado.correo_usuario)
        tipo_usuario: TipoUsuario = TipoUsuario.query.get(usuario_encontrado.cve_tipo_usuario)
        
        if tipo_usuario.tipo_usuario == 'Administrador' or tipo_usuario.tipo_usuario == 'Usuario registrado':
            return {"access_token": access_token, "usuario": usuario_encontrado.usuario, "tipo_usuario": tipo_usuario.tipo_usuario, "link_imagen": usuario_encontrado.link_imagen}
        else:
            abort(400, mesaage="No se pudo acceder a la cuenta.")
            