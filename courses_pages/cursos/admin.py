
from django.contrib import admin
from .models import Curso, Modulo, Material, Realiza, Adquiere

class ModuloInline(admin.TabularInline):
    model = Modulo
    extra = 1

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombreCurso", "precioCurso", "nivelCurso", "usuario")
    search_fields = ("nombreCurso", "descripcionCurso", "usuario__username")
    list_filter = ("nivelCurso",)
    inlines = [ModuloInline]

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ("id", "nombreModulo", "curso", "totalLecciones")
    search_fields = ("nombreModulo", "curso__nombreCurso")
    list_filter = ("curso",)

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("id", "tipo", "tipoDeArchivo", "urlArchivo")
    search_fields = ("tipo", "tipoDeArchivo")
    list_filter = ("tipo", "tipoDeArchivo")
    filter_horizontal = ("modulos",)

@admin.register(Realiza)
class RealizaAdmin(admin.ModelAdmin):
    list_display = ("id", "curso", "usuario", "fechaRealizacion", "estado")
    search_fields = ("curso__nombreCurso", "usuario__username")
    list_filter = ("estado", "fechaRealizacion")

@admin.register(Adquiere)
class AdquiereAdmin(admin.ModelAdmin):
    list_display = ("id", "curso", "usuario", "fechaInicio", "fechaFinalizacion", "porcAvance")
    search_fields = ("curso__nombreCurso", "usuario__username")
    list_filter = ("fechaInicio",)

# Register your models here.
