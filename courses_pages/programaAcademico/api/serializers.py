# api/serializers.py
from rest_framework import serializers
from programaAcademico.models import programaAcademico

class programaAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = programaAcademico
        fields = ['id', 'nombreprogramaAcademico']  # Django automáticamente añade 'id' aunque en tu tabla es idprogramaAcademico
        # Si necesitas mapear exactamente id a idprogramaAcademico:
        # fields = ['idprogramaAcademico', 'nombreCategoria']
        # Pero necesitarías cambiar el nombre del campo en el modelo