from django.db import transaction
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import JSONParser
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework import status, views, permissions
from rest_framework.response import Response
from .models import Transaction
from django_ratelimit.decorators import ratelimit
from .serializers import (TransactionSerializer, BalanceSerializer,
                           DepositSerializer, ProfileSerializer, SendMoneySerializer)


class DepositView(views.APIView):
    """внесение депозита на баланс текущего пользователя"""
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (JSONParser,)
    
    @swagger_auto_schema(request_body=DepositSerializer)
    @method_decorator(ratelimit(key='user', rate='5/m', method='POST', block=True))
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            profile = request.user.profile
            profile.balance += amount
            profile.save()
            return Response({'message':'Бланс успешно пополнен','new_balance': profile.balance},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class TransactionHistoryView(views.APIView):
    """вывод истории транзакций"""
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (JSONParser,)
    
    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        serializer = TransactionSerializer(transactions, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetAllUsers(views.APIView):
    """Вывод всех пользователей"""
    def get(self, request):
        profiles = User.objects.all()
        serializer = ProfileSerializer(profiles, many = True)
        return Response(serializer.data)


class BalanceView(views.APIView):
    """вывод баланса текущего пользователя"""
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (JSONParser,)

    
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        serializer = BalanceSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SendMoneyView(views.APIView):
    """отправка средств пользователю со счета текущего пользователя"""
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=SendMoneySerializer)
    @method_decorator(ratelimit(key='user', rate='5/m', method='POST', block=True))
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = SendMoneySerializer(data=request.data)
        if serializer.is_valid():
            receiver_id = serializer.validated_data['receiver_id']
            amount = serializer.validated_data['amount']
            sender = request.user
            receiver = User.objects.get(pk=receiver_id)

            if sender.profile.balance < amount:
                return Response({"error": "Недостаточно средств на балансе"}, status=status.HTTP_400_BAD_REQUEST)

            sender.profile.balance -= amount
            receiver.profile.balance += amount
            sender.profile.save()
            receiver.profile.save()

            
            Transaction.objects.create(sender=sender, receiver=receiver, amount=amount)

            return Response({"message": "Средства успешно отправлены"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionView(views.APIView):
    """Отправка средств с указанием получателя и отправителя"""
    parser_classes = (JSONParser,)
    

    @swagger_auto_schema(request_body=TransactionSerializer)
    @method_decorator(ratelimit(key='user', rate='5/m', method='POST', block=True))
    @transaction.atomic
    def post(self, request, *args, **kwargs) -> Response:
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            sender = serializer.validated_data['sender']
            receiver = serializer.validated_data['receiver']
            amount = serializer.validated_data['amount']

            if sender.profile.balance < amount:
                return Response({"error": "Недостаточно средств на балансе отправителя"},
                                status=status.HTTP_400_BAD_REQUEST)
            sender.profile.balance -= amount
            receiver.profile.balance += amount
            sender.profile.save()
            receiver.profile.save()

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
