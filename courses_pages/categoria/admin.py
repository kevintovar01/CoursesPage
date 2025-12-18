
from django.contrib import admin
from .models import Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombreCategoria")
    search_fields = ("nombreCategoria",)

# Register your models here.
