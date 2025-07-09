from django.db import models

class ConstaDe(models.Model):
    categoria = models.ForeignKey(
        'categoria.Categoria',  # Referencia a la app categoria
        on_delete=models.CASCADE,
        db_column='idCategoria'
    )
    
    programa_academico = models.ForeignKey(
        'programaAcademico.ProgramaAcademico',  # Referencia a la app programaAcademico
        on_delete=models.CASCADE,
        db_column='idProgramaAcademico'
    )

    class Meta:
        db_table = 'ConstaDe'
        unique_together = (('categoria', 'programa_academico'),)  # Clave primaria compuesta

    def __str__(self):
        return f"Categoría {self.categoria.id} → Programa {self.programa_academico.id}"