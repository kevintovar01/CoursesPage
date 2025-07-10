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
