# api/models.py
from django.db import models

class Categoria(models.Model):
    nombreCategoria = models.CharField(max_length=100, unique=True)
    
    class Meta:
        db_table = 'Categoria'  # Esto mantendrá el nombre exacto de tu tabla
    
    def __str__(self):
        return self.nombreCategoria
