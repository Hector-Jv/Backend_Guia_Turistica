from app import db

class Horario(db.Model):
    cve_horario = db.Column(db.Integer, autoincrement=True, nullable=False)
    dia = db.Column(db.String(100), nullable=False)
    horario_apertura = db.Column(db.Time, nullable=False)
    horario_cierre = db.Column(db.Time, nullable=False)
    cve_sitio = db.Column(db.Integer, db.ForeignKey('sitio.cve_sitio'), nullable=False)
    
    __table_args__ = (
        db.PrimaryKeyConstraint('cve_horario', 'cve_sitio'),
    )

    def __init__(self, dia: str, horario_apertura: str, horario_cierre: str, cve_sitio: int):
        """Constructor de Horario"""
        self.dia = dia
        self.horario_apertura = horario_apertura
        self.horario_cierre = horario_cierre
        self.cve_sitio = cve_sitio
