from rest_framework import serializers
from registra.models import Registra

class RegistraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registra
        fields = ['id', 'usuario', 'programa_academico']
        extra_kwargs = {
            'usuario': {'required': True},
            'programa_academico': {'required': True}
        }

    def validate(self, data):
        # Validación personalizada para evitar duplicados
        if Registra.objects.filter(
            usuario=data['usuario'],
            programa_academico=data['programa_academico']
        ).exists():
            raise serializers.ValidationError("Este registro ya existe.")
        return data