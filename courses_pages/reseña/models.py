# reseñas/models.py
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Reseña(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='idUsuario',
        related_name='reseñas'
    )
    curso = models.ForeignKey(
        'cursos.Curso',  # Referencia a la app cursos
        on_delete=models.CASCADE,
        db_column='idCurso',
        related_name='reseñas'
    )
    valorCalificacion = models.SmallIntegerField(
        db_column='valorCalificacion',
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    fecha = models.DateField(db_column='fecha', auto_now_add=True)
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Reseña'
        unique_together = ('usuario', 'curso')  # Un usuario solo puede reseñar un curso una vez
        verbose_name = 'reseña'
        verbose_name_plural = 'reseñas'

    def __str__(self):
        return f"Reseña #{self.id} - {self.usuario} para {self.curso}"