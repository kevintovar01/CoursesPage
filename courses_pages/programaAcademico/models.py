# api/models.py
from django.db import models

class programaAcademico(models.Model):
    nombreprogramaAcademico = models.CharField(max_length=100, unique=True)
    
    class Meta:
        db_table = 'programaAcademico'  # Esto mantendrá el nombre exacto de tu tabla
    
    def __str__(self):
        return self.nombreprogramaAcademico
