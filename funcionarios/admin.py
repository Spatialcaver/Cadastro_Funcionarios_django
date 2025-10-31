from django.contrib import admin
from .models import Funcionario

class AdminFuncionario(admin.ModelAdmin):
    list_display = ('matricula', 'usuario', 'cpf', 'cargo', 'empresa')
    search_fields = ('usuario__name', 'usuario__email', 'cpf', 'cargo', 'empresa__razao_social', 'empresa__cnpj')
    
    
admin.site.register(Funcionario, AdminFuncionario)