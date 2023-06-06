import datetime
from app import db

class Comentario(db.Model):
    cve_comentario = db.Column(db.Integer, autoincrement=True, nullable=False)
    comentario = db.Column(db.String(400), nullable=False)
    fecha_comentario = db.Column(db.DateTime, nullable=False)
    cve_historial = db.Column(db.Integer, db.ForeignKey('historial.cve_historial'), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('cve_comentario', 'cve_historial'),
    )

    def __init__(self, comentario: str, cve_historial: int):
        """Constructor de Comentario"""
        self.comentario = comentario
        self.fecha_comentario = datetime.now()
        self.cve_historial = cve_historial
        