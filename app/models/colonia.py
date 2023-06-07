from app import db

class Colonia(db.Model):
    cve_colonia = db.Column(db.Integer, primary_key=True)
    nombre_colonia = db.Column(db.String(100), nullable=False)
    cve_delegacion = db.Column(db.Integer, nullable=False)
    
    def __init__ (self, nombre_colonia: str, cve_delegacion: int):
        """Constructor de Colonia"""
        self.nombre_colonia = nombre_colonia
        self.cve_delegacion = cve_delegacion
        