from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.courses.models import Enrollment
from apps.payments.models import Payment

from .models import Transaction, Wallet


def get_wallet_for_user(user):
    wallet, _ = Wallet.objects.get_or_create(user=user)
    return wallet


@transaction.atomic
def add_balance(user, amount):
    wallet = Wallet.objects.select_for_update().get(user=user)
    wallet.deposit(amount)
    Transaction.objects.create(
        wallet=wallet,
        amount=amount,
        transaction_type=Transaction.DEPOSIT,
        description='Wallet balance top-up',
    )
    return wallet


@transaction.atomic
def purchase_course(user, course):
    if Enrollment.objects.filter(user=user, course=course).exists():
        raise ValidationError('You have already purchased this course.')

    wallet = Wallet.objects.select_for_update().get(user=user)
    amount = course.get_discounted_price()

    if wallet.balance < amount:
        raise ValidationError('Insufficient wallet balance.')

    wallet.withdraw(amount)
    Transaction.objects.create(
        wallet=wallet,
        amount=amount,
        transaction_type=Transaction.PURCHASE,
        description=f'Course purchase: {course.title}',
    )
    enrollment = Enrollment.objects.create(user=user, course=course, progress=0)
    payment = Payment.objects.create(
        user=user,
        course=course,
        amount=amount,
        status='success',
        payment_method='wallet',
        payment_date=timezone.now(),
    )
    course.students_count = course.enrollments.count()
    course.save(update_fields=['students_count'])
    return enrollment, payment
