from rest_framework import serializers


#definindo o apontamento do modelo
from .models import Funcionario

#Verificando os campos recebidos 
class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = ['nome', 'cpf', 'matricula', 'cargo', 'idade']
        
    def validate_cpf(self, value):

        cpf = value.strip().lower().replace('.', '').replace('-', '')
        if len(cpf) != 11:
            # 2. Se for diferente de 11, levanta a exceção de validação
            raise serializers.ValidationError("CPF inválido")