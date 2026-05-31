from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.courses.models import Category, Course, Enrollment
from apps.payments.models import Payment

from .models import Transaction, Wallet
from .services import purchase_course


class WalletSystemTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='StrongPass123',
        )
        self.mentor = User.objects.create_user(
            username='mentor',
            email='mentor@example.com',
            password='StrongPass123',
            role='mentor',
        )
        self.category = Category.objects.create(name='Programming', slug='programming')
        self.course = Course.objects.create(
            title='Python Basics',
            slug='python-basics',
            description='Learn Python',
            short_description='Python intro',
            category=self.category,
            mentor=self.mentor,
            price=Decimal('200000.00'),
            level='beginner',
            duration='4 weeks',
            total_hours=10,
        )

    def test_wallet_created_for_new_user(self):
        self.assertTrue(Wallet.objects.filter(user=self.user).exists())
        self.assertEqual(self.user.wallet.balance, Decimal('0.00'))

    def test_balance_top_up(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('wallet:add_balance'), {'preset_amount': '200000'})
        self.assertRedirects(response, reverse('wallet:dashboard'))
        self.user.wallet.refresh_from_db()
        self.assertEqual(self.user.wallet.balance, Decimal('200000.00'))
        self.assertTrue(Transaction.objects.filter(wallet=self.user.wallet, transaction_type=Transaction.DEPOSIT).exists())

    def test_successful_purchase(self):
        self.user.wallet.deposit(Decimal('250000.00'))
        enrollment, payment = purchase_course(self.user, self.course)
        self.user.wallet.refresh_from_db()
        self.assertEqual(self.user.wallet.balance, Decimal('50000.00'))
        self.assertEqual(enrollment.course, self.course)
        self.assertEqual(payment.status, 'success')
        self.assertTrue(Payment.objects.filter(user=self.user, course=self.course).exists())

    def test_insufficient_balance(self):
        with self.assertRaisesMessage(Exception, 'Insufficient wallet balance.'):
            purchase_course(self.user, self.course)
        self.assertFalse(Enrollment.objects.filter(user=self.user, course=self.course).exists())

    def test_duplicate_purchase_prevention(self):
        self.user.wallet.deposit(Decimal('500000.00'))
        purchase_course(self.user, self.course)
        with self.assertRaisesMessage(Exception, 'You have already purchased this course.'):
            purchase_course(self.user, self.course)
        self.assertEqual(Enrollment.objects.filter(user=self.user, course=self.course).count(), 1)
