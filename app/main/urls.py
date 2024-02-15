from django.urls import path
from .views import TransactionView, BalanceView, DepositView, GetAllUsers, TransactionHistoryView, SendMoneyView


urlpatterns = [
    path('transactions/', TransactionView.as_view(), name='transaction'),#транзакция с указанием отправителя и получателя
    path('sendamount/', SendMoneyView.as_view(),name = 'send_money'),#транзакция от текущего пользователя к указаному 
    path('history/', TransactionHistoryView.as_view(), name='transactions_history'),#история транзакций
    path('balance/', BalanceView.as_view(), name='balance'),#баланс текущего пользователя
    path('deposit/', DepositView.as_view(), name='deposit'),#внесения депозита на баланс текущего пользователя
    path('users/', GetAllUsers.as_view(), name='users'), #вывод списка пользователей
]
