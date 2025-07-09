from rest_framework import serializers
from constade.models import ConstaDe

class ConstaDeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstaDe
        fields = ['id', 'categoria', 'programa_academico']
        extra_kwargs = {
            'categoria': {'required': True},
            'programa_academico': {'required': True}
        }

    def validate(self, data):
        # Validación para evitar duplicados
        if ConstaDe.objects.filter(
            categoria=data['categoria'],
            programa_academico=data['programa_academico']
        ).exists():
            raise serializers.ValidationError("Esta relación ya existe.")
        return data