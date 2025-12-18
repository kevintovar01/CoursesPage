
from django.contrib import admin
from .models import programaAcademico

@admin.register(programaAcademico)
class ProgramaAcademicoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombreprogramaAcademico")
    search_fields = ("nombreprogramaAcademico",)

# Register your models here.
