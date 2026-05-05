from django.db import models
from django.conf import settings
from apps.courses.models import Course


class PaymentPlan(models.Model):
    """
    Payment plan for installment payments
    """
    MONTH_CHOICES = [
        (3, '3 oy'),
        (6, '6 oy'),
        (12, '12 oy'),
        (18, '18 oy'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payment_plans')
    months = models.IntegerField(choices=MONTH_CHOICES)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # in percentage
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Payment Plan'
        verbose_name_plural = 'Payment Plans'
        unique_together = ('course', 'months')
    
    def __str__(self):
        return f"{self.course.title} - {self.months} oy"
    
    def get_monthly_payment(self):
        total_amount = self.course.get_discounted_price()
        total_with_interest = total_amount * (1 + self.interest_rate / 100)
        return round(total_with_interest / self.months, 2)
    
    def get_total_amount(self):
        return round(self.get_monthly_payment() * self.months, 2)


class Payment(models.Model):
    """
    Payment model
    """
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('paid', 'To\'landi'),
        ('failed', 'Xatolik'),
        ('cancelled', 'Bekor qilindi'),
        ('overdue', 'Muddati o\'tdi'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('click', 'Click'),
        ('payme', 'Payme'),
        ('uzcard', 'Uzcard'),
        ('humo', 'Humo'),
        ('cash', 'Naqd'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments')
    payment_plan = models.ForeignKey(PaymentPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    
    transaction_id = models.CharField(max_length=200, blank=True, null=True, unique=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.course.title} - {self.amount}"
    
    def is_overdue(self):
        if self.due_date and self.status == 'pending':
            from django.utils import timezone
            return timezone.now().date() > self.due_date
        return False


class InstallmentPayment(models.Model):
    """
    Individual installment payment
    """
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('paid', 'To\'landi'),
        ('overdue', 'Muddati o\'tdi'),
    ]
    
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='installments')
    installment_number = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    transaction_id = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Installment Payment'
        verbose_name_plural = 'Installment Payments'
        ordering = ['installment_number']
        unique_together = ('payment', 'installment_number')
    
    def __str__(self):
        return f"{self.payment.course.title} - {self.installment_number}-tolov"
    
    def is_overdue(self):
        if self.status == 'pending':
            from django.utils import timezone
            return timezone.now().date() > self.due_date
        return False
