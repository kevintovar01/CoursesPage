
from django.contrib import admin
from .models import Reseña

@admin.register(Reseña)
class ReseñaAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "curso", "valorCalificacion", "fecha")
    search_fields = ("usuario__username", "curso__nombreCurso", "comentario")
    list_filter = ("valorCalificacion", "fecha")
    readonly_fields = ("fecha",)

# Register your models here.
