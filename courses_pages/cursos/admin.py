from django.contrib import admin
from .models import Curso, Modulo, Material, Realiza, Adquiere

# Register your models here.

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombreCurso', 'usuario', 'precioCurso', 'nivelCurso')
    list_filter = ('nivelCurso', 'usuario')
    search_fields = ('nombreCurso', 'descripcionCurso')
    ordering = ('nombreCurso',)

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('nombreModulo', 'curso', 'totalLecciones')
    list_filter = ('curso',)
    search_fields = ('nombreModulo', 'curso__nombreCurso')
    ordering = ('curso', 'nombreModulo')

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'tipoDeArchivo', 'urlArchivo')
    list_filter = ('tipo', 'tipoDeArchivo')
    search_fields = ('tipo', 'tipoDeArchivo')
    filter_horizontal = ('modulos',)

@admin.register(Realiza)
class RealizaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'curso', 'fechaRealizacion', 'estado')
    list_filter = ('estado', 'fechaRealizacion', 'curso')
    search_fields = ('usuario__email', 'curso__nombreCurso')
    date_hierarchy = 'fechaRealizacion'
    ordering = ('-fechaRealizacion',)

@admin.register(Adquiere)
class AdquiereAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'curso', 'fechaInicio', 'fechaFinalizacion', 'porcAvance')
    list_filter = ('fechaInicio', 'fechaFinalizacion', 'curso')
    search_fields = ('usuario__email', 'curso__nombreCurso')
    date_hierarchy = 'fechaInicio'
    ordering = ('-fechaInicio',)
    readonly_fields = ('fechaInicio',)
