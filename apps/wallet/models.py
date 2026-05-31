from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.user.email} - {self.balance}'

    def clean(self):
        if self.balance < 0:
            raise ValidationError({'balance': 'Wallet balance cannot be negative.'})

    def deposit(self, amount):
        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValidationError('Deposit amount must be positive.')
        self.balance += amount
        self.full_clean()
        self.save(update_fields=['balance', 'updated_at'])

    def withdraw(self, amount):
        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValidationError('Withdrawal amount must be positive.')
        if self.balance < amount:
            raise ValidationError('Insufficient wallet balance.')
        self.balance -= amount
        self.full_clean()
        self.save(update_fields=['balance', 'updated_at'])


class Transaction(models.Model):
    DEPOSIT = 'deposit'
    PURCHASE = 'purchase'
    REFUND = 'refund'

    TRANSACTION_TYPES = [
        (DEPOSIT, 'Deposit'),
        (PURCHASE, 'Purchase'),
        (REFUND, 'Refund'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.wallet.user.email} - {self.transaction_type} - {self.amount}'

    def clean(self):
        if self.amount <= 0:
            raise ValidationError({'amount': 'Transaction amount must be positive.'})
