# api/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from programaAcademico.models import programaAcademico
from .serializers import programaAcademicoSerializer

# Opción 1: Usando APIView para control total
class programaAcademicoList(APIView):
    def get(self, request):
        programaAcademicos = programaAcademico.objects.all()
        serializer = programaAcademicoSerializer(programaAcademicos, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = programaAcademicoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class programaAcademicoDetail(APIView):
    def get_object(self, pk):
        try:
            return programaAcademico.objects.get(pk=pk)
        except programaAcademico.DoesNotExist:
            return None
    
    def get(self, request, pk):
        programaAcademico = self.get_object(pk)
        if programaAcademico is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = programaAcademicoSerializer(programaAcademico)
        return Response(serializer.data)
    
    def put(self, request, pk):
        programaAcademico = self.get_object(pk)
        if programaAcademico is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = programaAcademicoSerializer(programaAcademico, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        programaAcademico = self.get_object(pk)
        if programaAcademico is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        programaAcademico.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Opción 2: Usando vistas genéricas (más conciso)
class programaAcademicoListCreate(ListCreateAPIView):
    queryset = programaAcademico.objects.all()
    serializer_class = programaAcademicoSerializer

class programaAcademicoRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = programaAcademico.objects.all()
    serializer_class = programaAcademicoSerializer