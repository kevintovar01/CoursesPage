
from django.contrib import admin
from .models import Registra

@admin.register(Registra)
class RegistraAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "programa_academico")
    search_fields = ("usuario__username", "programa_academico__nombreprogramaAcademico")
    list_filter = ("programa_academico",)

# Register your models here.
