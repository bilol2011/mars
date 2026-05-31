from django.contrib import admin

from apps.courses.models import Enrollment
from apps.payments.models import Payment

from .models import Transaction, Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'created_at', 'updated_at')
    search_fields = ('user__email', 'user__username', 'user__first_name', 'user__last_name')
    ordering = ('-updated_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'transaction_type', 'amount', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('wallet__user__email', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


class EnrollmentWalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at')
    search_fields = ('user__email', 'course__title')
    list_filter = ('enrolled_at',)
    ordering = ('-enrolled_at',)


class PaymentWalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'amount', 'status', 'created_at')
    search_fields = ('user__email', 'course__title')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
