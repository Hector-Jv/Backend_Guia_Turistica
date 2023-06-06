from app import db

class FotoComentario(db.Model):
    cve_foto_comentario = db.Column(db.Integer, autoincrement=True, nullable=False)
    nombre_imagen = db.Column(db.String(100), nullable=True)
    link_imagen = db.Column(db.String(200), nullable=False)
    nombre_autor = db.Column(db.String(200), nullable=True)
    cve_comentario = db.Column(db.Integer, db.ForeignKey('comentario.cve_comentario'), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('cve_foto_comentario', 'cve_comentario'),
    )
    
    def __init__(self, nombre_imagen: str, link_imagen: str, nombre_autor: str, cve_comentario: int):
        """Constructor de FotoComentario"""
        self.nombre_imagen = nombre_imagen
        self.link_imagen = link_imagen
        self.nombre_autor = nombre_autor
        self.cve_comentario = cve_comentario