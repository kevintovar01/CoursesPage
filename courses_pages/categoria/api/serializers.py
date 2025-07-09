# api/serializers.py
from rest_framework import serializers
from categoria.models import Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombreCategoria']  # Django automáticamente añade 'id' aunque en tu tabla es idCategoria
        # Si necesitas mapear exactamente id a idCategoria:
        # fields = ['idCategoria', 'nombreCategoria']
        # Pero necesitarías cambiar el nombre del campo en el modelo