from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from registra.models import Registra
from .serializers import RegistraSerializer

class RegistraList(APIView):
    """Maneja GET (todos) y POST (crear)"""
    def get(self, request):
        registros = Registra.objects.all()
        serializer = RegistraSerializer(registros, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RegistraSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistraDetail(APIView):
    """Maneja GET (uno), PUT (actualizar) y DELETE"""
    def get_object(self, pk):
        try:
            return Registra.objects.get(pk=pk)
        except Registra.DoesNotExist:
            return None

    def get(self, request, pk):
        registro = self.get_object(pk)
        if registro:
            serializer = RegistraSerializer(registro)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        registro = self.get_object(pk)
        if registro:
            serializer = RegistraSerializer(registro, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        registro = self.get_object(pk)
        if registro:
            registro.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    