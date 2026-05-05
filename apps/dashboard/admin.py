from django.contrib import admin
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.urls import path
from django.shortcuts import render
from django.http import JsonResponse
from .models import Wishlist, Certificate, Notification, CourseRecommendation, DailyAnalytics, CourseAnalytics
from apps.accounts.models import User, Transaction, Wallet, UserLevel, Badge, UserBadge, PaymentCard
from apps.courses.models import Course, Enrollment, EducationalCenter, Category, Lesson, LessonProgress, LiveLesson, LiveLessonParticipant


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'course__title')


class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_id', 'enrollment', 'issued_date')
    list_filter = ('issued_date',)
    search_fields = ('certificate_id', 'enrollment__user__email', 'enrollment__course__title')
    readonly_fields = ('certificate_id', 'issued_date')


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__email', 'title', 'message')


class CourseRecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'reason', 'score', 'is_clicked', 'is_enrolled', 'created_at')
    list_filter = ('reason', 'is_clicked', 'is_enrolled', 'created_at')
    search_fields = ('user__email', 'course__title')
    readonly_fields = ('created_at',)


class DailyAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_users', 'active_users', 'total_courses', 'total_enrollments', 'total_revenue', 'new_users')
    list_filter = ('date',)
    readonly_fields = ('date',)


class CourseAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('course', 'date', 'views', 'enrollments', 'revenue', 'completions')
    list_filter = ('date', 'course')
    search_fields = ['course__title']
    readonly_fields = ('date',)


# Register models with standard admin
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(CourseRecommendation, CourseRecommendationAdmin)
admin.site.register(DailyAnalytics, DailyAnalyticsAdmin)
admin.site.register(CourseAnalytics, CourseAnalyticsAdmin)


# Custom views for standard admin
class DashboardAdminMixin:
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
            path('analytics/revenue/', self.admin_view(self.revenue_analytics), name='revenue_analytics'),
            path('analytics/users/', self.admin_view(self.user_analytics), name='user_analytics'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        """Main dashboard view with overview statistics"""
        today = timezone.now().date()
        
        # Get statistics
        total_users = User.objects.count()
        total_courses = Course.objects.filter(is_published=True).count()
        total_centers = EducationalCenter.objects.filter(is_active=True).count()
        total_revenue = Transaction.objects.filter(
            transaction_type='purchase',
            status='success'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Today's statistics
        today_revenue = Transaction.objects.filter(
            transaction_type='purchase',
            status='success',
            created_at__date=today
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        today_enrollments = Enrollment.objects.filter(enrolled_at__date=today).count()
        today_users = User.objects.filter(date_joined__date=today).count()
        
        # This month's revenue
        this_month = timezone.now().replace(day=1)
        monthly_revenue = Transaction.objects.filter(
            transaction_type='purchase',
            status='success',
            created_at__date__gte=this_month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # This year's revenue
        this_year = timezone.now().replace(month=1, day=1)
        yearly_revenue = Transaction.objects.filter(
            transaction_type='purchase',
            status='success',
            created_at__date__gte=this_year
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Recent transactions
        recent_transactions = Transaction.objects.select_related('user').order_by('-created_at')[:10]
        
        # Top courses
        top_courses = Course.objects.annotate(
            enrollment_count=Count('enrollments')
        ).order_by('-enrollment_count')[:5]
        
        # Top users by spending
        top_spenders = User.objects.annotate(
            total_spent=Sum('wallet__transactions__amount', filter=Q(wallet__transactions__transaction_type='purchase'))
        ).order_by('-total_spent')[:5]
        
        context = {
            'total_users': total_users,
            'total_courses': total_courses,
            'total_centers': total_centers,
            'total_revenue': total_revenue,
            'today_revenue': today_revenue,
            'today_enrollments': today_enrollments,
            'today_users': today_users,
            'monthly_revenue': monthly_revenue,
            'yearly_revenue': yearly_revenue,
            'recent_transactions': recent_transactions,
            'top_courses': top_courses,
            'top_spenders': top_spenders,
            **self.each_context(request),
        }
        return render(request, 'admin/dashboard.html', context)

    def revenue_analytics(self, request):
        """Revenue analytics view"""
        from django.db.models.functions import TruncDate, TruncMonth, TruncYear
        
        # Daily revenue for last 30 days
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        daily_revenue = Transaction.objects.filter(
            transaction_type='purchase',
            status='success',
            created_at__gte=thirty_days_ago
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            total=Sum('amount')
        ).order_by('date')
        
        # Monthly revenue for this year
        this_year = timezone.now().replace(month=1, day=1)
        monthly_revenue = Transaction.objects.filter(
            transaction_type='purchase',
            status='success',
            created_at__date__gte=this_year
        ).annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(
            total=Sum('amount')
        ).order_by('month')
        
        # Yearly revenue
        yearly_revenue = Transaction.objects.filter(
            transaction_type='purchase',
            status='success'
        ).annotate(
            year=TruncYear('created_at')
        ).values('year').annotate(
            total=Sum('amount')
        ).order_by('year')
        
        context = {
            'daily_revenue': daily_revenue,
            'monthly_revenue': monthly_revenue,
            'yearly_revenue': yearly_revenue,
            **self.each_context(request),
        }
        return render(request, 'admin/revenue_analytics.html', context)

    def user_analytics(self, request):
        """User analytics and purchase tracking"""
        
        # Recent user registrations
        recent_users = User.objects.order_by('-date_joined')[:20]
        
        # Users with most purchases
        top_buyers = User.objects.annotate(
            purchase_count=Count('enrollments'),
            total_spent=Sum('wallet__transactions__amount', filter=Q(wallet__transactions__transaction_type='purchase'))
        ).order_by('-total_spent')[:20]
        
        # Recent purchases
        recent_purchases = Transaction.objects.filter(
            transaction_type='purchase',
            status='success'
        ).select_related('user').order_by('-created_at')[:20]
        
        # User activity (last 7 days)
        seven_days_ago = timezone.now() - timezone.timedelta(days=7)
        active_users = User.objects.filter(
            Q(enrollments__enrolled_at__gte=seven_days_ago) |
            Q(wallet__transactions__created_at__gte=seven_days_ago)
        ).distinct().count()
        
        context = {
            'recent_users': recent_users,
            'top_buyers': top_buyers,
            'recent_purchases': recent_purchases,
            'active_users': active_users,
            **self.each_context(request),
        }
        return render(request, 'admin/user_analytics.html', context)


# Create custom admin site with dashboard functionality
class DashboardAdminSite(admin.AdminSite):
    site_header = 'BILOL Admin'
    site_title = 'BILOL Administration'
    index_title = 'Boshqaruv Paneli'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
            path('analytics/revenue/', self.admin_view(self.revenue_analytics), name='revenue_analytics'),
            path('analytics/users/', self.admin_view(self.user_analytics), name='user_analytics'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        """Main dashboard view with overview statistics"""
        today = timezone.now().date()
        
        # Get statistics
        total_users = User.objects.count()
        total_courses = Course.objects.filter(is_published=True).count()
        total_centers = EducationalCenter.objects.filter(is_active=True).count()
        total_revenue = Transaction.objects.filter(
            transaction_type='purchase',
            status='success'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Today's statistics
        today_revenue = Transaction.objects.filter(
            transaction_type='purchase',
            status='success',
            created_at__date=today
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        today_enrollments = Enrollment.objects.filter(enrolled_at__date=today).count()
        today_users = User.objects.filter(date_joined__date=today).count()
        
        # This month's revenue
        this_month = timezone.now().replace(day=1)
        monthly_revenue = Transaction.objects.filter(
            transaction_type='purchase',
            status='success',
            created_at__date__gte=this_month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # This year's revenue
        this_year = timezone.now().replace(month=1, day=1)
        yearly_revenue = Transaction.objects.filter(
            transaction_type='purchase',
            status='success',
            created_at__date__gte=this_year
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Recent transactions
        recent_transactions = Transaction.objects.select_related('user').order_by('-created_at')[:10]
        
        # Top courses
        top_courses = Course.objects.annotate(
            enrollment_count=Count('enrollments')
        ).order_by('-enrollment_count')[:5]
        
        # Top users by spending
        top_spenders = User.objects.annotate(
            total_spent=Sum('wallet__transactions__amount', filter=Q(wallet__transactions__transaction_type='purchase'))
        ).order_by('-total_spent')[:5]
        
        context = {
            'total_users': total_users,
            'total_courses': total_courses,
            'total_centers': total_centers,
            'total_revenue': total_revenue,
            'today_revenue': today_revenue,
            'today_enrollments': today_enrollments,
            'today_users': today_users,
            'monthly_revenue': monthly_revenue,
            'yearly_revenue': yearly_revenue,
            'recent_transactions': recent_transactions,
            'top_courses': top_courses,
            'top_spenders': top_spenders,
            **self.each_context(request),
        }
        return render(request, 'admin/dashboard.html', context)

    def revenue_analytics(self, request):
        """Revenue analytics view"""
        from django.db.models.functions import TruncDate, TruncMonth, TruncYear
        
        # Daily revenue for last 30 days
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        daily_revenue = Transaction.objects.filter(
            transaction_type='purchase',
            status='success',
            created_at__gte=thirty_days_ago
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            total=Sum('amount')
        ).order_by('date')
        
        # Monthly revenue for this year
        this_year = timezone.now().replace(month=1, day=1)
        monthly_revenue = Transaction.objects.filter(
            transaction_type='purchase',
            status='success',
            created_at__date__gte=this_year
        ).annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(
            total=Sum('amount')
        ).order_by('month')
        
        # Yearly revenue
        yearly_revenue = Transaction.objects.filter(
            transaction_type='purchase',
            status='success'
        ).annotate(
            year=TruncYear('created_at')
        ).values('year').annotate(
            total=Sum('amount')
        ).order_by('year')
        
        context = {
            'daily_revenue': daily_revenue,
            'monthly_revenue': monthly_revenue,
            'yearly_revenue': yearly_revenue,
            **self.each_context(request),
        }
        return render(request, 'admin/revenue_analytics.html', context)

    def user_analytics(self, request):
        """User analytics and purchase tracking"""
        
        # Recent user registrations
        recent_users = User.objects.order_by('-date_joined')[:20]
        
        # Users with most purchases
        top_buyers = User.objects.annotate(
            purchase_count=Count('enrollments'),
            total_spent=Sum('wallet__transactions__amount', filter=Q(wallet__transactions__transaction_type='purchase'))
        ).order_by('-total_spent')[:20]
        
        # Recent purchases
        recent_purchases = Transaction.objects.filter(
            transaction_type='purchase',
            status='success'
        ).select_related('user').order_by('-created_at')[:20]
        
        # User activity (last 7 days)
        seven_days_ago = timezone.now() - timezone.timedelta(days=7)
        active_users = User.objects.filter(
            Q(enrollments__enrolled_at__gte=seven_days_ago) |
            Q(wallet__transactions__created_at__gte=seven_days_ago)
        ).distinct().count()
        
        context = {
            'recent_users': recent_users,
            'top_buyers': top_buyers,
            'recent_purchases': recent_purchases,
            'active_users': active_users,
            **self.each_context(request),
        }
        return render(request, 'admin/user_analytics.html', context)


# Create the custom admin site instance
dashboard_admin = DashboardAdminSite(name='dashboard_admin')

# Register all models with the custom admin site
from apps.accounts.admin import UserAdmin, WalletAdmin, TransactionAdmin, UserLevelAdmin, BadgeAdmin, UserBadgeAdmin, PaymentCardAdmin
from apps.courses.admin import CategoryAdmin, CourseAdmin, LessonAdmin, EnrollmentAdmin, LessonProgressAdmin, LiveLessonAdmin, LiveLessonParticipantAdmin, EducationalCenterAdmin

dashboard_admin.register(User, UserAdmin)
dashboard_admin.register(Wallet, WalletAdmin)
dashboard_admin.register(Transaction, TransactionAdmin)
dashboard_admin.register(UserLevel, UserLevelAdmin)
dashboard_admin.register(Badge, BadgeAdmin)
dashboard_admin.register(UserBadge, UserBadgeAdmin)
dashboard_admin.register(PaymentCard, PaymentCardAdmin)
dashboard_admin.register(Category, CategoryAdmin)
dashboard_admin.register(Course, CourseAdmin)
dashboard_admin.register(Lesson, LessonAdmin)
dashboard_admin.register(Enrollment, EnrollmentAdmin)
dashboard_admin.register(LessonProgress, LessonProgressAdmin)
dashboard_admin.register(LiveLesson, LiveLessonAdmin)
dashboard_admin.register(LiveLessonParticipant, LiveLessonParticipantAdmin)
dashboard_admin.register(EducationalCenter, EducationalCenterAdmin)
dashboard_admin.register(Wishlist, WishlistAdmin)
dashboard_admin.register(Certificate, CertificateAdmin)
dashboard_admin.register(Notification, NotificationAdmin)
dashboard_admin.register(CourseRecommendation, CourseRecommendationAdmin)
dashboard_admin.register(DailyAnalytics, DailyAnalyticsAdmin)
dashboard_admin.register(CourseAnalytics, CourseAnalyticsAdmin)
