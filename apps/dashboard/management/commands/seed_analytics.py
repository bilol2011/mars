from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import models
from datetime import timedelta, date
from apps.dashboard.models import DailyAnalytics, CourseAnalytics
from apps.courses.models import Course, Enrollment
from apps.accounts.models import UserLevel, Transaction


class Command(BaseCommand):
    help = 'Seed analytics data for the dashboard'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding analytics data...')
        
        # Seed daily analytics for the last 30 days
        today = timezone.now().date()
        
        for i in range(30):
            day = today - timedelta(days=i)
            
            daily_analytics, created = DailyAnalytics.objects.get_or_create(
                date=day,
                defaults={
                    'total_users': UserLevel.objects.count(),
                    'active_users': Enrollment.objects.filter(
                        enrolled_at__date=day
                    ).values('user').distinct().count(),
                    'total_courses': Course.objects.filter(is_published=True).count(),
                    'total_enrollments': Enrollment.objects.count(),
                    'total_revenue': Transaction.objects.filter(
                        transaction_type='purchase',
                        created_at__date=day
                    ).aggregate(total=models.Sum('amount'))['total'] or 0,
                    'new_users': UserLevel.objects.filter(
                        created_at__date=day
                    ).count(),
                    'new_enrollments': Enrollment.objects.filter(
                        enrolled_at__date=day
                    ).count(),
                    'completed_courses': Enrollment.objects.filter(
                        completed_at__date=day
                    ).count(),
                }
            )
            
            if created:
                self.stdout.write(f'Created daily analytics for {day}')
        
        # Seed course analytics for the last 30 days
        courses = Course.objects.filter(is_published=True)
        
        for course in courses:
            for i in range(30):
                day = today - timedelta(days=i)
                
                course_analytics, created = CourseAnalytics.objects.get_or_create(
                    course=course,
                    date=day,
                    defaults={
                        'views': 0,
                        'enrollments': Enrollment.objects.filter(
                            course=course,
                            enrolled_at__date=day
                        ).count(),
                        'revenue': Transaction.objects.filter(
                            transaction_type='purchase',
                            created_at__date=day,
                            description__icontains=course.title
                        ).aggregate(total=models.Sum('amount'))['total'] or 0,
                        'completions': Enrollment.objects.filter(
                            course=course,
                            completed_at__date=day
                        ).count(),
                    }
                )
                
                if created:
                    self.stdout.write(f'Created course analytics for {course.title} on {day}')
        
        self.stdout.write(self.style.SUCCESS('Analytics data seeded successfully!'))
