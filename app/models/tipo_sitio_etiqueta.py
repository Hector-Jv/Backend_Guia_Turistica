from app import db

class TipoSitio_Etiqueta(db.Model):
    cve_tipo_sitio = db.Column(db.Integer, primary_key=True)
    cve_etiqueta = db.Column(db.Integer, primary_key=True)
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['cve_tipo_sitio'],
            ['tipo_sitio.cve_tipo_sitio'],
        ),
        db.ForeignKeyConstraint(
            ['cve_etiqueta'],
            ['etiqueta.cve_etiqueta'],
        ),
    )
    
    def __init__(self, cve_tipo_sitio: int, cve_etiqueta: int):
        """Constructor de TipoSitio_Etiqueta"""
        self.cve_tipo_sitio = cve_tipo_sitio
        self.cve_etiqueta = cve_etiqueta
        