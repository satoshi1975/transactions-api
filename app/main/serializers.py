from rest_framework import serializers
from .models import Profile, Transaction
from django.contrib.auth.models import User


class TransactionSerializer(serializers.ModelSerializer):
    """сериалайзер транзакции"""
    class Meta:
        model = Transaction
        fields = ['id','sender','receiver','amount','created_at', 'updated_at']

class SendMoneySerializer(serializers.Serializer):
    """сериалайзер транзакции от текущего пользователя"""
    receiver_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_receiver_id(self, value):
        try:
            User.objects.get(pk=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с указанным ID не найден.")
        return value

class BalanceSerializer(serializers.ModelSerializer):
    """сериалайзер вывода баланса текущего пользователя"""
    class Meta:
        model = Profile
        fields = ['balance']

class ProfileSerializer(serializers.ModelSerializer):
    """сериалайзер вывода Пользователя"""
    class Meta:
        model = User
        fields = '__all__'


class DepositSerializer(serializers.Serializer):
    """сериалайзер внесения депозита"""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

