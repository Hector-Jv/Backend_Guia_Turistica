from flask import Blueprint, jsonify, request
from app import db
from app.models import Sitio, Colonia, Horario, TipoSitio, SitioEtiqueta, FotoSitio
from flask.views import MethodView
from flask_smorest import Blueprint, abort, fields
from marshmallow import Schema, fields
import cloudinary.uploader

crear_sitio_bp = Blueprint('crear_sitio', __name__)

@crear_sitio_bp.route('/crear_sitio')
class AgregarSitio(MethodView):
    
    def post(self):
        
        print("A")
        
        # Datos ingresados #
        try:
            # Modelo Sitio
            nombre_sitio = request.form["nombre_sitio"]
            longitud = request.form["longitud"]
            latitud = request.form["latitud"]
            descripcion = request.form["descripcion"]
            correo = request.form["correo"]
            costo = request.form["costo"]
            pagina_web = request.form["pagina_web"]
            telefono = request.form["telefono"]
            print("B1")
            
            adscripcion = request.form["adscripcion"]
            print("B2")
            
            cve_tipo_sitio = int(request.form["cve_tipo_sitio"]) 
            print("B3")
            cve_delegacion = int(request.form["cve_delegacion"])
            print("B4")
            
            colonia = request.form["colonia"]
            # Modelo SitioEtiqueta #
            arreglo_etiquetas = request.form["etiquetas"] # arreglo diccionarios
            print("B5")
            
            # Modelo Horario
            # arr_horario = request.form["horarios"] # arreglo de diccionarios
            
        except Exception as e:
            abort(400, message="Hubo un error al recibir los datos.")
            
        # Conversiones #
        longitud = float(longitud)
        latitud = float(latitud)
        costo = float(costo) if costo else 0
        
        print("C")
        
        # Validaciones #
        if Sitio.query.filter_by(nombre_sitio=nombre_sitio, longitud=longitud, latitud=latitud).first():
            abort(400, message="Ya existe un sitio con ese nombre y con la misma dirección.")
        
        calificacion_sitio = {
            "promedio": 0
        }
        
        obtener_tipo_sitio = TipoSitio.query.get(cve_tipo_sitio)
        print("D")
        
        if obtener_tipo_sitio.tipo_sitio == "Hotel":
            calificacion_sitio["calificaciones_especificas"] = {
                "limpieza": 0,
                "atencion": 0,
                "instalaciones": 0
            }
        if obtener_tipo_sitio.tipo_sitio == "Restaurante":
            calificacion_sitio["calificaciones_especificas"] = {
                "limpieza": 0,
                "atencion": 0,
                "costo": 0,
                "sabor": 0
            }    
        
        obtener_colonia = Colonia.query.filter_by(nombre_colonia=colonia).first()
        print("E")
        
        try:
            # Insertar colonia
            if not obtener_colonia:
                crear_colonia = Colonia(
                    colonia, 
                    cve_delegacion
                )
                db.session.add(crear_colonia)
                db.session.flush()
                obtener_colonia = crear_colonia
            print("F")

            # Insertar sitio
            nuevo_sitio = Sitio(
                # Obligatorios #
                nombre_sitio, 
                longitud, 
                latitud,
                cve_tipo_sitio,
                obtener_colonia.cve_colonia,
                # Opcionales #
                descripcion,
                correo,
                costo,
                pagina_web,
                telefono,
                adscripcion,
                calificacion_sitio
            )
            db.session.add(nuevo_sitio)
            db.session.flush()
            print("G")

            """
            # Insertar horarios
            for horario in arr_horario:
                nuevo_horario = Horario(
                    horario["dia"],
                    horario["horario_apertura"],
                    horario["horario_cierre"],
                    horario["cve_sitio"]
                )
                db.session.add(nuevo_horario)
            """
            # Insertar etiquetas
            if obtener_tipo_sitio.tipo_sitio in ["Hotel", "Restaurante", "Museo"] and arreglo_etiquetas:
                for cve_etiqueta in arreglo_etiquetas:
                    nueva_relacion = SitioEtiqueta(
                        nuevo_sitio.cve_sitio,
                        cve_etiqueta
                    )
                    db.session.add(nueva_relacion)
            print("H")
            
            # Insertar imagenes
            fotos = request.files.getlist('fotos_sitio')
            links_imagenes = []
            for foto in fotos:
                if foto.filename != '':
                    # VALIDACIONES #
                    extensiones_validas = {'png', 'jpg', 'jpeg', 'gif'}
                    if '.' not in foto.filename and foto.filename.rsplit('.', 1)[1].lower() not in extensiones_validas:
                        abort(400, message="La imagen no tiene una extensión válida.")
                    
                    # SE SUBE LA IMAGEN #
                    result = cloudinary.uploader.upload(foto)
                    links_imagenes.append(result['secure_url'])
                    
                    foto_sitio = FotoSitio(
                        link_imagen = result['secure_url'],
                        cve_sitio = nuevo_sitio.cve_sitio,
                        nombre_imagen='x',
                        nombre_autor='x'
                    )
                    db.session.add(foto_sitio)
            print("I")

            # Si todo ha salido bien, confirmamos los cambios
            db.session.commit()
            print("J")

        except Exception as e:
            # Si ha habido algún error, deshacemos los cambios
            db.session.rollback()
            print("K")
            
            abort(400, message="Hubo un error: " + str(e))
        finally:
            print("L")
            
            return {"mensaje": "Sitio creado con éxito."}
