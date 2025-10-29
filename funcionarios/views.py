from rest_framework.views import APIView
from .models import Funcionario
from rest_framework.response import Response
from .serializers import FuncionarioSerializer
from rest_framework import status

class FuncionarioCreateView(APIView):
    def post(self, request):
        serializer = FuncionarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FuncionarioListView(APIView):
    def get(self, request):
        queryset = Funcionario.objects.all()
        serializer = FuncionarioSerializer(queryset, many=True)
        return Response({ "results": serializer.data }, status=status.HTTP_200_OK)
    
class FuncionarioUpdateView(APIView):
    def put(self, request, pk):
        queryset = Funcionario.objects.get(pk=pk)
        serializer = FuncionarioSerializer(instance=queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class FuncionarioDeleteView(APIView):
    def delete(self, request, pk):
        queryset = Funcionario.objects.get(pk=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
