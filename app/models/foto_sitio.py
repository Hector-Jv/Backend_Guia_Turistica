from app import db

class FotoSitio(db.Model):
    cve_foto_sitio = db.Column(db.Integer, autoincrement=True, nullable=False)
    nombre_imagen = db.Column(db.String(100), nullable=True)
    link_imagen = db.Column(db.String(200), nullable=False)
    nombre_autor = db.Column(db.String(200), nullable=True)
    cve_sitio = db.Column(db.Integer, db.ForeignKey('sitio.cve_sitio'), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('cve_foto_sitio', 'cve_sitio'),
    )
    
    def __init__(self, nombre_imagen: str, link_imagen: str, nombre_autor: str, cve_sitio: int):
        """Constructor de FotoSitio"""
        self.nombre_imagen = nombre_imagen
        self.link_imagen = link_imagen
        self.nombre_autor = nombre_autor
        self.cve_sitio = cve_sitio
