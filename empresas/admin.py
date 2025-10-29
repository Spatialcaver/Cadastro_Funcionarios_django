from django.contrib import admin
from .models import Empresa

# Register your models here.
@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('razao_social', 'cnpj', 'segmento')
    search_fields = ('razao_social', 'cnpj', 'segmento')
