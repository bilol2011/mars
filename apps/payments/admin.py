from django.contrib import admin
from .models import PaymentPlan, Payment, InstallmentPayment


@admin.register(PaymentPlan)
class PaymentPlanAdmin(admin.ModelAdmin):
    list_display = ('course', 'months', 'interest_rate', 'is_active', 'get_monthly_payment')
    list_filter = ('months', 'is_active')
    search_fields = ('course__title',)


class InstallmentPaymentInline(admin.TabularInline):
    model = InstallmentPayment
    extra = 0
    readonly_fields = ('installment_number', 'amount', 'due_date', 'status')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'amount', 'status', 'payment_method', 'payment_date', 'due_date')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('user__email', 'course__title', 'transaction_id')
    readonly_fields = ('transaction_id', 'created_at', 'updated_at')
    inlines = [InstallmentPaymentInline]


@admin.register(InstallmentPayment)
class InstallmentPaymentAdmin(admin.ModelAdmin):
    list_display = ('payment', 'installment_number', 'amount', 'due_date', 'status', 'paid_date')
    list_filter = ('status', 'due_date')
    search_fields = ('payment__user__email', 'payment__course__title')
