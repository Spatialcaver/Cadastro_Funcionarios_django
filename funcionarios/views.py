from datetime import timedelta
from django.utils import timezone
from funcionarios.models import Funcionario, Jornada
from funcionarios.serializers import FuncionarioSerializer, FuncionarioSerializerControle, JornadaSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Value, DecimalField, FloatField, ExpressionWrapper # Importar Value e DecimalField
from django.db.models.functions import Coalesce # Importar a função Coalesce
from django.shortcuts import get_object_or_404
from django.db.models import Sum , Q, F


class FuncionarioListCreateView(generics.ListCreateAPIView):
 
    queryset = Funcionario.objects.all()
    
    # Define qual Serializer será usado para a entrada/saída de dados.
    serializer_class = FuncionarioSerializer
    
    # Prioridade P2: Garante que apenas usuários autenticados possam listar/criar.
    permission_classes = [permissions.IsAuthenticated] 


    


class FuncionarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Permite visualizar os detalhes, atualizar ou deletar um funcionário específico.
    Requer autenticação (JWT Token).
    """
    # Define todos os objetos que a View deve operar.
    queryset = Funcionario.objects.all()
    
    # Define qual Serializer será usado.
    serializer_class = FuncionarioSerializer
    
    # Prioridade P2: Garante que apenas usuários autenticados possam modificar/deletar.
    permission_classes = [permissions.IsAuthenticated]
    
    
class BaterPontoAPIView( APIView):
    """
    Endpoint para registrar entrada (Clock-in) ou saída (Clock-out).
    Identifica o funcionário logado via Token JWT.
    """
    permission_classes = [permissions.IsAuthenticated] 

    def post(self, request, *args, **kwargs):
        # O usuário Funcionario é identificado pelo JWT
        user = request.user 
        
        # O objeto Funcionario é a FK do objeto User
        try:
            funcionario = Funcionario.objects.get(usuario=user)
        except Funcionario.DoesNotExist:
            return Response({"error": "Perfil de funcionário não encontrado ou não associado."}, 
                            status=status.HTTP_404_NOT_FOUND)

        # 1. Tenta encontrar a jornada aberta (hora_saida é NULA)
        try:
            jornada_aberta = Jornada.objects.filter(
                funcionario=funcionario, 
                hora_saida__isnull=True
            ).latest('hora_entrada')
            
            # --- LÓGICA DE SAÍDA (CLOCK-OUT) ---
            jornada_aberta.hora_saida = timezone.now()
            jornada_aberta.save() # O save() calcula as horas_trabalhadas
            
            serializer = JornadaSerializer(jornada_aberta)
            return Response({
                "message": "Saída registrada com sucesso!",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Jornada.DoesNotExist:
            # --- LÓGICA DE ENTRADA (CLOCK-IN) ---
            nova_jornada = Jornada.objects.create(
                funcionario=funcionario,
                hora_entrada=timezone.now()
            )
            serializer = JornadaSerializer(nova_jornada)
            return Response({
                "message": "Entrada registrada com sucesso!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
            
            
            
            
META_HORAS_SEMANAIS = 14.0 

class ProgressoMetaView(APIView):
    """
    Endpoint para o Colaborador ver seu progresso semanal em tempo real.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Identifica o funcionário logado
        funcionario = get_object_or_404(Funcionario, usuario=request.user)

        # 1. Define o ciclo semanal (Segunda a Domingo)
        hoje = timezone.localdate()
        # Calcula a data da última segunda-feira
        inicio_semana = hoje - timedelta(days=hoje.weekday()) 
        # Calcula a data do próximo domingo
        fim_semana = inicio_semana + timedelta(days=6) 

        # 2. Agrega horas trabalhadas NA SEMANA ATUAL
        horas_trabalhadas = Jornada.objects.filter(
            funcionario=funcionario,
            hora_entrada__date__range=[inicio_semana, fim_semana]
        ).aggregate(total_horas=Sum('horas_trabalhadas'))['total_horas'] or 0.00
        
        # 3. Calcula o progresso
        horas_atuais = float(horas_trabalhadas)
        percentual = round((horas_atuais / META_HORAS_SEMANAIS) * 100, 2)
        
        return Response({
            "colaborador": funcionario.usuario.name,
            "matricula": funcionario.matricula,
            "meta_semanal_horas": META_HORAS_SEMANAIS,
            "horas_trabalhadas_atuais": horas_atuais,
            "horas_restantes": max(0, META_HORAS_SEMANAIS - horas_atuais),
            "progresso_percentual": percentual
        })
        
        
class MinhasJornadasView(generics.ListAPIView):
    """
    Endpoint dedicado para o colaborador visualizar todas as suas jornadas de trabalho.
    Requer autenticação JWT. (GET /funcionarios/jornadas/me/)
    """
    serializer_class = JornadaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 1. Encontra o Funcionario associado ao usuário logado via Token
        try:
            funcionario = Funcionario.objects.get(usuario=self.request.user)
        except Funcionario.DoesNotExist:
            # Retorna um conjunto vazio se o perfil de funcionário não for encontrado
            return Jornada.objects.none() 

        # 2. Retorna todas as jornadas desse funcionário, da mais recente para a mais antiga.
        return Jornada.objects.filter(funcionario=funcionario).order_by('-hora_entrada')
    
    
class GestaoRankingView(generics.ListAPIView):
    """
    Endpoint para o Gestor visualizar o ranking de progresso de toda a equipe na semana.
    """
    # 🛑 1. Restrição de Permissão: Apenas Staff/Admin pode acessar
    # permissions.IsAdminUser verifica is_staff e is_superuser (se IS_STAFF_VIEW is True no settings, senão só is_superuser)
    # Recomendado: Crie uma permissão customizada se quiser só Staff, mas IsAdminUser funciona bem.
    permission_classes = [permissions.IsAdminUser] 
    
    # Vamos usar um serializer customizado para incluir nome, matricula, cargo e meta.
    serializer_class = FuncionarioSerializerControle # Vamos criar este Serializer no 1.2

    # A lógica de get_queryset está excelente para calcular horas e percentual.
    # Apenas vamos garantir que os campos estejam disponíveis para o serializer.
    META_HORAS_SEMANAIS = 14.0 # Garanta que esta constante esteja acessível
    
    def get_queryset(self):
        hoje = timezone.localdate()
        inicio_semana = hoje - timedelta(days=hoje.weekday()) 
        fim_semana = inicio_semana + timedelta(days=6) 
        
        queryset = Funcionario.objects.annotate(
            horas_atuais=Sum(
                'jornadas__horas_trabalhadas',
                filter= Q(jornadas__hora_entrada__date__range=[inicio_semana, fim_semana])
            )
        ).annotate(
            # 1. Coalesce para garantir 0.00 se for NULL
            horas_atuais_num=Coalesce(F('horas_atuais'), Value(0.00, output_field=DecimalField())),
        ).annotate(
            # 🛑 2. CORREÇÃO FINAL AQUI: 
            # O output_field deve ser anexado à expressão de cálculo, não como argumento extra.
            progresso_percentual=F('horas_atuais_num') / self.META_HORAS_SEMANAIS * 100,
            # Se a anotação for complexa, como a nossa, o jeito mais limpo é o ExpressionWrapper, 
            # mas vamos tentar a forma mais simples que geralmente funciona para divisões:
            
        )
        
        # 💡 Tenta a forma simples com output_field na expressão:
        queryset = queryset.annotate(
            progresso_percentual=ExpressionWrapper(
                F('horas_atuais_num') / self.META_HORAS_SEMANAIS * 100,
                output_field=FloatField()
            )
        ).order_by('-horas_atuais_num')
        
        return queryset