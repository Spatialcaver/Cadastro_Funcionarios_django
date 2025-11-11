from rest_framework import serializers

from contas.models import User
from .models import Funcionario, Jornada


class FuncionarioSerializer(serializers.ModelSerializer):
    
    nome = serializers.CharField(source='usuario.name', read_only=True)
    empresa = serializers.StringRelatedField(read_only=True)
    email = serializers.EmailField(source='usuario.email', read_only=True)
    
    class Meta:
        model = Funcionario
        fields = ['id', 'usuario', 'nome', 'email', 'cpf', 'matricula', 
                  'cargo', 'idade', 'empresa']
        
        extra_kwargs = {
            'usuario': {'write_only': True}
        }
        
    def validate_cpf(self, value):
        cpf = value.strip().lower().replace('.', '').replace('-', '')
        if len(cpf) != 11:
            raise serializers.ValidationError("CPF inválido")
        return cpf

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'is_staff']

class JornadaSerializer(serializers.ModelSerializer):
    nome_funcionario = serializers.CharField(source='funcionario.usuario.name', read_only=True)
    
    class Meta:
        model = Jornada
        fields = ['id', 'nome_funcionario', 'funcionario', 'hora_entrada', 'hora_saida', 'horas_trabalhadas']
        read_only_fields = ['hora_entrada', 'hora_saida', 'horas_trabalhadas', 'funcionario']