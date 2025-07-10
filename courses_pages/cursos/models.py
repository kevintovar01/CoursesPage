from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Curso(models.Model):
    """Modelo de Curso"""
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cursos_creados'
    )
    nombreCurso = models.CharField(max_length=150)
    precioCurso = models.DecimalField(max_digits=10, decimal_places=2)
    descripcionCurso = models.TextField(blank=True, null=True)
    nivelCurso = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombreCurso

class Modulo(models.Model):
    """Modelo de Módulo"""
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='modulos')
    nombreModulo = models.CharField(max_length=150)
    totalLecciones = models.IntegerField()

    def __str__(self):
        return f"{self.nombreModulo} ({self.curso.nombreCurso})"

class Material(models.Model):
    """Modelo de Material"""
    tipo = models.CharField(max_length=50)
    tipoDeArchivo = models.CharField(max_length=50)
    urlArchivo = models.URLField()
    modulos = models.ManyToManyField(Modulo, related_name='materiales')

    def __str__(self):
        return f"{self.tipo} - {self.tipoDeArchivo}"

class Realiza(models.Model):
    """Modelo para la solicitud de realización de un curso por parte de un usuario."""
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    fechaRealizacion = models.DateField()
    estado = models.CharField(max_length=50)

    class Meta:
        unique_together = ('curso', 'usuario')

    def __str__(self):
        return f"{self.usuario} solicita realizar {self.curso}"

class Adquiere(models.Model):
    """Modelo para la adquisición de un curso por parte de un usuario."""
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='adquiere')
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cursos_adquiridos'
    )
    fechaInicio = models.DateField()
    fechaFinalizacion = models.DateField()
    porcAvance = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        unique_together = ('curso', 'usuario')
        constraints = [
            models.CheckConstraint(
                check=models.Q(fechaInicio__lte=models.F('fechaFinalizacion')),
                name='fechaInicio_lte_fechaFinalizacion'
            )
        ]

    def __str__(self):
        return f"{self.usuario} adquiere {self.curso}"
