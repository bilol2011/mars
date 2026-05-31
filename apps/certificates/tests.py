from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.courses.models import Category, Course

from .models import Certificate
from .services import build_certificate_pdf


class CertificateTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='student', email='student@example.com', password='Pass12345')
        self.mentor = User.objects.create_user(username='mentor', email='mentor@example.com', password='Pass12345')
        category = Category.objects.create(name='Design', slug='design')
        self.course = Course.objects.create(
            title='UI Design',
            slug='ui-design',
            description='Design course',
            short_description='UI',
            category=category,
            mentor=self.mentor,
            price=Decimal('100000.00'),
            duration='1 week',
            total_hours=3,
        )
        self.certificate = Certificate.objects.create(user=self.user, course=self.course)

    def test_pdf_generation(self):
        pdf = build_certificate_pdf(self.certificate)
        self.assertTrue(pdf.startswith(b'%PDF'))
        self.assertIn(self.certificate.certificate_id.encode('latin-1'), pdf)

    def test_download_requires_owner(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('certificates:download', args=[self.certificate.certificate_id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
