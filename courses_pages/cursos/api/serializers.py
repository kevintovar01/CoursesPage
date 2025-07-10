from time import timezone
from rest_framework import serializers
from django.utils.timezone import now
from ..models import Curso, Modulo, Material, Realiza, Adquiere

class CursoSerializer(serializers.ModelSerializer):
    usuario = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Curso
        fields = ('id', 'nombreCurso', 'descripcionCurso', 'nivelCurso', 'precioCurso', 'usuario')

class ModuloSerializer(serializers.ModelSerializer):
    # this avoid selecting all cursos of the application
    curso = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.none())
    class Meta:
        model = Modulo
        fields = ("id", "curso", "nombreModulo", "totalLecciones")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # accede al user desde el contexto y filtra sólo sus cursos
        user = self.context['request'].user
        self.fields['curso'].queryset = Curso.objects.filter(usuario=user)

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class RealizaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Realiza
        fields = '__all__'

class AdquiereSerializer(serializers.ModelSerializer):

    usuario = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Adquiere
        fields = ("id","curso","usuario", "fechaInicio",)
    

