# reseñas/serializers.py
from rest_framework import serializers
from reseña.models import Reseña

class ReseñaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reseña
        fields = ['id', 'usuario', 'curso', 'valorCalificacion', 'comentario', 'fecha']
        read_only_fields = ['usuario', 'fecha']
        extra_kwargs = {
            'valorCalificacion': {'min_value': 0, 'max_value': 5}
        }

    def validate(self, data):
        if Reseña.objects.filter(usuario=self.context['request'].user, curso=data['curso']).exists():
            raise serializers.ValidationError("Ya has reseñado este curso")
        return data