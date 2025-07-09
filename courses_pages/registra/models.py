from django.db import models
from django.conf import settings

class Registra(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='idUsuario'  # Nombre exacto de columna en BD
    )
    
    programa_academico = models.ForeignKey(
        'programaAcademico.ProgramaAcademico',  # Referencia entre apps
        on_delete=models.CASCADE,
        db_column='idProgramaAcademico'  # Nombre exacto de columna
    )

    class Meta:
        db_table = 'Registra'
        unique_together = (('usuario', 'programa_academico'),)