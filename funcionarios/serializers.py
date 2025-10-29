from rest_framework import serializers


#definindo o apontamento do modelo
from .models import Funcionario

#Verificando os campos recebidos 
class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        # Ordem final: Matricula, Nome, Idade, Cargo
        fields = '__all__'