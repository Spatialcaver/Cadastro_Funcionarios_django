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
        
        
class FuncionarioSerializerControle(serializers.ModelSerializer):
    # Campos do modelo User (via FK)
    nome = serializers.CharField(source='usuario.name', read_only=True)
    
    # Campos calculados na View (GestaoRankingView)
    horas_atuais = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    progresso_percentual = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    meta_atingida = serializers.SerializerMethodField()

    class Meta:
        model = Funcionario
        # Campos requeridos pelo seu frontend
        fields = ['nome', 'matricula', 'cargo', 'horas_atuais', 'progresso_percentual', 'meta_atingida']
    
    def get_meta_atingida(self, obj):
        # A constante de meta é definida na View. Vamos assumir 14h como padrão aqui
        META_HORAS_SEMANAIS = 14.0 
        
        # O campo 'horas_atuais' é anotado na queryset.
        horas_atuais = getattr(obj, 'horas_atuais', 0)
        return float(horas_atuais or 0) >= META_HORAS_SEMANAIS