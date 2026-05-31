from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.certificates.models import Certificate
from apps.courses.models import Category, Course, Enrollment

from .models import Lesson, LessonProgress, Module
from .services import calculate_course_progress, complete_lesson


class LmsPhaseThreeTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='student', email='student@example.com', password='Pass12345')
        self.other_user = User.objects.create_user(username='guest', email='guest@example.com', password='Pass12345')
        self.mentor = User.objects.create_user(username='mentor', email='mentor@example.com', password='Pass12345')
        self.category = Category.objects.create(name='Backend', slug='backend')
        self.course = Course.objects.create(
            title='Django LMS',
            slug='django-lms',
            description='Build LMS',
            short_description='LMS',
            category=self.category,
            mentor=self.mentor,
            price=Decimal('100000.00'),
            duration='2 weeks',
            total_hours=5,
        )
        self.module = Module.objects.create(course=self.course, title='Start', description='Intro', order=1)
        self.preview_lesson = Lesson.objects.create(
            module=self.module,
            title='Preview',
            video_url='https://youtu.be/demo',
            duration_minutes=5,
            order=1,
            is_preview=True,
        )
        self.paid_lesson = Lesson.objects.create(
            module=self.module,
            title='Paid lesson',
            video_url='https://youtu.be/paid',
            duration_minutes=10,
            order=2,
        )

    def test_preview_access_without_purchase(self):
        response = self.client.get(reverse('lms:lesson', args=[self.preview_lesson.id]))
        self.assertEqual(response.status_code, 200)

    def test_paid_lesson_blocked_without_purchase(self):
        self.client.force_login(self.other_user)
        response = self.client.get(reverse('lms:lesson', args=[self.paid_lesson.id]))
        self.assertRedirects(response, reverse('courses:detail', args=[self.course.slug]))

    def test_lesson_completion_and_progress(self):
        Enrollment.objects.create(user=self.user, course=self.course)
        progress, percentage = complete_lesson(self.user, self.preview_lesson)
        self.assertTrue(progress.completed)
        self.assertEqual(percentage, 50)
        self.assertEqual(calculate_course_progress(self.user, self.course), 50)

    def test_certificate_generation_when_course_complete(self):
        Enrollment.objects.create(user=self.user, course=self.course)
        complete_lesson(self.user, self.preview_lesson)
        complete_lesson(self.user, self.paid_lesson)
        self.assertTrue(Certificate.objects.filter(user=self.user, course=self.course).exists())
        self.assertEqual(calculate_course_progress(self.user, self.course), 100)

    def test_certificate_verification(self):
        certificate = Certificate.objects.create(user=self.user, course=self.course)
        response = self.client.get(reverse('certificates:verify', args=[certificate.certificate_id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Valid Certificate')
