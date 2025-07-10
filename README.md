
{
    "id": 1,
    "usuario": 1,
    "programa_academico": 1
}

CREATE TABLE IF NOT EXISTS Reseña (
    idReseña        SERIAL     PRIMARY KEY,
    idUsuario       INT        NOT NULL
        REFERENCES Usuario(idUsuario),
    idCurso         INT        NOT NULL
        REFERENCES Curso(idCurso),
    valorCalificacion SMALLINT NOT NULL
        CHECK (valorCalificacion BETWEEN 0 AND 5),
    fecha           DATE       NOT NULL
); 
ahora para este crea un mode views urls serializers no olvides poner metodos get post y delete cursos esta en una app llamada cursos
que tiene el siguiente models:
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
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
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
serialisers:
from rest_framework import serializers
from ..models import Curso, Modulo, Material, Realiza, Adquiere

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class RealizaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Realiza
        fields = '__all__'

class AdquiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adquiere
        fields = '__all__'
urls: 
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CursoViewSet, 
    ModuloViewSet, MaterialViewSet, RealizaViewSet
)

router = DefaultRouter()
router.register(r'cursos', CursoViewSet)
router.register(r'modulos', ModuloViewSet)
router.register(r'materiales', MaterialViewSet)
router.register(r'realiza', RealizaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
views:
from django.shortcuts import render
from django.db.models import Count, Avg
from django.db import connection
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Curso, Modulo, Material, Realiza, Adquiere
from .serializers import CursoSerializer, ModuloSerializer, MaterialSerializer, RealizaSerializer, AdquiereSerializer

# Create your views here.

class IsEstudiante(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a usuarios con rol 'Estudiante'.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'rol') and request.user.rol == 'Estudiante'

# Usando APIView para control total sobre el modelo Curso
class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    @action(detail=False, methods=['get'])
    def estudiantes_matriculados(self, request):
        """
        2. Estudiantes matriculados por curso
        """
        cursos = Curso.objects.annotate(
            estudiantesMatriculados=Count('adquiere'),
            progresoPromedio=Avg('adquiere__porcAvance')
        ).order_by('-estudiantesMatriculados')
        
        data = [{
            'nombreCurso': curso.nombreCurso,
            'nivelCurso': curso.nivelCurso,
            'estudiantesMatriculados': curso.estudiantesMatriculados,
            'progresoPromedio': round(curso.progresoPromedio, 2) if curso.progresoPromedio else 0
        } for curso in cursos]
        
        return Response(data)

    @action(detail=True, methods=['get'])
    def recursos(self, request, pk=None):
        """
        3. Uso de recursos por curso
        """
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT mo.nombreModulo, COUNT(ma.idMaterial) AS totalMateriales, STRING_AGG(ma.tipo, ', ') AS tiposMateriales
                FROM cursos_modulo mo
                INNER JOIN cursos_contiene co ON mo.idModulo = co.idModulo
                INNER JOIN cursos_material ma ON co.idMaterial = ma.idMaterial
                WHERE mo.idCurso_id = %s
                GROUP BY mo.idModulo, mo.nombreModulo
                ORDER BY mo.nombreModulo;
            """, [pk])
            rows = cursor.fetchall()

        data = [{
            'nombreModulo': row[0],
            'totalMateriales': row[1],
            'tiposMateriales': row[2]
        } for row in rows]
        
        return Response(data)

    @action(detail=False, methods=['get'], permission_classes=[IsEstudiante])
    def cursos_no_adquiridos(self, request):
        """
        12. Cursos disponibles para inscribirse (que no he adquirido)
        """
        cursos = Curso.objects.exclude(adquiere__usuario=request.user).annotate(
            calificacionPromedio=Avg('reseña__valorCalificacion')
        ).order_by('-calificacionPromedio')

        serializer = self.get_serializer(cursos, many=True)
        return Response(serializer.data)


class ModuloViewSet(viewsets.ModelViewSet):
    queryset = Modulo.objects.all()
    serializer_class = ModuloSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class RealizaViewSet(viewsets.ModelViewSet):
    queryset = Realiza.objects.all()
    serializer_class = RealizaSerializer

class AdquiereViewSet(viewsets.ModelViewSet):
    queryset = Adquiere.objects.all()
    serializer_class = AdquiereSerializer
    permission_classes = [IsEstudiante]

