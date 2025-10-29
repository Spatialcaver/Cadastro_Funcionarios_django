from django.contrib import admin
from .models import Funcionario

# Register your models here.

@admin.register(Funcionario)
class AdminFuncionario(admin.ModelAdmin):
    list_display = ('matricula', 'nome', 'cpf', 'cargo')
    search_fields = ('nome', 'cpf', 'cargo')