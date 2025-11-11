from django.contrib import admin
from .models import Funcionario, Jornada

class AdminFuncionario(admin.ModelAdmin):
    list_display = ('matricula', 'usuario', 'cpf', 'cargo', 'empresa')
    search_fields = ('usuario__name', 'usuario__email', 'cpf', 'cargo', 'empresa__razao_social', 'empresa__cnpj')
    
    
    
class JornadaTrabalhoAdmin(admin.ModelAdmin):
    # Exibe os campos importantes na lista
    list_display = ('funcionario', 'hora_entrada', 'hora_saida', 'horas_trabalhadas')
    # Filtro para ver jornadas abertas (hora_saida é nula)
    list_filter = ('funcionario', 'hora_saida') 
    search_fields = ('funcionario__usuario__name',)


    
    
admin.site.register(Funcionario, AdminFuncionario)
admin.site.register(Jornada, JornadaTrabalhoAdmin)