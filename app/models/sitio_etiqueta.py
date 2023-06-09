from app import db

class SitioEtiqueta(db.Model):
    cve_sitio = db.Column(db.Integer, primary_key=True)
    cve_etiqueta = db.Column(db.Integer, primary_key=True)
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['cve_sitio'],
            ['sitio.cve_sitio'],
        ),
        db.ForeignKeyConstraint(
            ['cve_etiqueta'],
            ['etiqueta.cve_etiqueta'],
        ),
    )
    
    def __init__(self, cve_sitio:  int, cve_etiqueta: int):
        """Constructor de SitioEtiqueta"""
        self.cve_sitio = cve_sitio
        self.cve_etiqueta = cve_etiqueta