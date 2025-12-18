
from django.contrib import admin
from .models import ConstaDe

@admin.register(ConstaDe)
class ConstaDeAdmin(admin.ModelAdmin):
    list_display = ("id", "categoria", "programa_academico")
    search_fields = ("categoria__nombreCategoria", "programa_academico__nombreprogramaAcademico")
    list_filter = ("categoria", "programa_academico")

# Register your models here.
