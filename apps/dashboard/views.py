from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from apps.courses.models import Enrollment, Course, Lesson
from apps.payments.models import Payment
from apps.accounts.models import Wallet, Transaction, UserLevel, Badge, UserBadge, User
from apps.reviews.models import Review
from .models import Wishlist, Certificate, Notification, CourseRecommendation, DailyAnalytics, PromoCode, Announcement


def is_admin(user):
    """Check if user is admin"""
    return user.is_staff or user.is_superuser


@login_required
def dashboard_home_view(request):
    """
    Dashboard home view
    """
    user = request.user
    
    # Get or create wallet
    wallet, created = Wallet.objects.get_or_create(user=user)
    
    # Get or create user level
    user_level, created = UserLevel.objects.get_or_create(user=user)
    
    # Get user's badges
    user_badges = UserBadge.objects.filter(user=user).select_related('badge')
    
    # Get available badges not earned
    earned_badge_ids = user_badges.values_list('badge_id', flat=True)
    available_badges = Badge.objects.filter(is_active=True).exclude(id__in=earned_badge_ids)
    
    # Get user's enrollments
    enrollments = Enrollment.objects.filter(user=user).order_by('-enrolled_at')
    
    # Get completed courses
    completed_enrollments = enrollments.filter(is_completed=True)
    
    # Get in-progress courses
    in_progress_enrollments = enrollments.filter(is_completed=False)
    
    # Get wishlist
    wishlist = Wishlist.objects.filter(user=user)
    
    # Get recent transactions
    recent_transactions = Transaction.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Get unread notifications
    unread_notifications = Notification.objects.filter(user=user, is_read=False)[:5]
    
    # Get recommended courses
    recommendations = CourseRecommendation.objects.filter(user=user).select_related('course')[:6]
    
    context = {
        'wallet': wallet,
        'user_level': user_level,
        'user_badges': user_badges,
        'available_badges': available_badges,
        'enrollments': enrollments,
        'completed_enrollments': completed_enrollments,
        'in_progress_enrollments': in_progress_enrollments,
        'wishlist': wishlist,
        'recent_transactions': recent_transactions,
        'unread_notifications': unread_notifications,
        'recommendations': recommendations,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def my_courses_view(request):
    """
    My courses view
    """
    enrollments = Enrollment.objects.filter(user=request.user).order_by('-enrolled_at')
    
    context = {
        'enrollments': enrollments,
    }
    return render(request, 'dashboard/my_courses.html', context)


@login_required
def wishlist_view(request):
    """
    Wishlist view
    """
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('course')
    
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'dashboard/wishlist.html', context)


@login_required
def add_to_wishlist_view(request, course_slug):
    """
    Add course to wishlist
    """
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        course=course
    )
    
    if created:
        messages.success(request, 'Kurs saqlanganlarga qo\'shildi.')
    else:
        messages.info(request, 'Kurs allaqachon saqlanganlarda bor.')
    
    return redirect('courses:detail', slug=course.slug)


@login_required
def remove_from_wishlist_view(request, course_slug):
    """
    Remove course from wishlist
    """
    course = get_object_or_404(Course, slug=course_slug)
    
    try:
        wishlist_item = Wishlist.objects.get(user=request.user, course=course)
        wishlist_item.delete()
        messages.success(request, 'Kurs saqlanganlardan olib tashlandi.')
    except Wishlist.DoesNotExist:
        messages.warning(request, 'Kurs saqlanganlarda topilmadi.')
    
    return redirect('dashboard:wishlist')


@login_required
def certificates_view(request):
    """
    Certificates view
    """
    certificates = Certificate.objects.filter(
        enrollment__user=request.user
    ).select_related('enrollment__course')
    
    context = {
        'certificates': certificates,
    }
    return render(request, 'dashboard/certificates.html', context)


@login_required
def notifications_view(request):
    """
    Notifications view
    """
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Mark all as read
    notifications.update(is_read=True)
    
    context = {
        'notifications': notifications,
    }
    return render(request, 'dashboard/notifications.html', context)


@login_required
def settings_view(request):
    """
    User settings view
    """
    return render(request, 'dashboard/settings.html')


@login_required
def admin_analytics_view(request):
    """
    Admin analytics dashboard view
    """
    if not request.user.is_staff:
        messages.error(request, 'Sizga bu sahifaga kirish ruxsati yo\'q.')
        return redirect('dashboard:home')
    
    # Get overall statistics
    total_users = UserLevel.objects.count()
    total_courses = Course.objects.count()
    total_enrollments = Enrollment.objects.count()
    total_revenue = Transaction.objects.filter(transaction_type='purchase').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # Get active users (users with enrollments in last 30 days)
    from django.utils import timezone
    from datetime import timedelta
    thirty_days_ago = timezone.now() - timedelta(days=30)
    active_users = Enrollment.objects.filter(enrolled_at__gte=thirty_days_ago).values('user').distinct().count()
    
    # Get top courses
    top_courses = Course.objects.annotate(
        enrollment_count=Count('enrollments')
    ).order_by('-enrollment_count')[:10]
    
    # Get daily analytics for chart
    daily_analytics = DailyAnalytics.objects.all().order_by('-date')[:30]
    
    # Get recent payments
    recent_payments = Payment.objects.select_related('user', 'course').order_by('-created_at')[:10]
    
    # Get wallet balances summary
    wallet_count = Wallet.objects.count()
    if wallet_count > 0:
        total_balance = Wallet.objects.aggregate(total=Sum('balance'))['total'] or 0
        avg_balance = total_balance / wallet_count
    else:
        total_balance = 0
        avg_balance = 0
    
    wallet_summary = {
        'total_balance': total_balance,
        'avg_balance': avg_balance
    }
    
    context = {
        'total_users': total_users,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'total_revenue': total_revenue,
        'active_users': active_users,
        'top_courses': top_courses,
        'daily_analytics': daily_analytics,
        'recent_payments': recent_payments,
        'wallet_summary': wallet_summary,
    }
    return render(request, 'dashboard/admin_analytics.html', context)


# ==================== ADMIN MANAGEMENT VIEWS ====================

@user_passes_test(is_admin)
@login_required
def admin_users_view(request):
    """Admin user management"""
    search_query = request.GET.get('search', '')
    
    users = User.objects.all()
    
    if search_query:
        users = users.filter(
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(username__icontains=search_query)
        )
    
    users = users.order_by('-created_at')
    
    context = {
        'users': users,
        'search_query': search_query,
    }
    return render(request, 'dashboard/admin/users.html', context)


@user_passes_test(is_admin)
@login_required
def admin_user_detail_view(request, user_id):
    """Admin user detail view"""
    user = get_object_or_404(User, id=user_id)
    enrollments = Enrollment.objects.filter(user=user).select_related('course')
    transactions = Transaction.objects.filter(user=user).order_by('-created_at')
    wallet = Wallet.objects.filter(user=user).first()
    
    context = {
        'target_user': user,
        'enrollments': enrollments,
        'transactions': transactions,
        'wallet': wallet,
    }
    return render(request, 'dashboard/admin/user_detail.html', context)


@user_passes_test(is_admin)
@login_required
def admin_block_user_view(request, user_id):
    """Block/unblock user"""
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    
    status = 'bloklandi' if not user.is_active else 'blokdan olindi'
    messages.success(request, f'Foydalanuvchi {status}.')
    return redirect('dashboard:admin_users')


@user_passes_test(is_admin)
@login_required
def admin_delete_user_view(request, user_id):
    """Delete user"""
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        messages.error(request, 'O\'zingizni o\'chira olmaysiz.')
        return redirect('dashboard:admin_users')
    
    user.delete()
    messages.success(request, 'Foydalanuvchi o\'chirildi.')
    return redirect('dashboard:admin_users')


@user_passes_test(is_admin)
@login_required
def admin_courses_view(request):
    """Admin course management"""
    courses = Course.objects.all().order_by('-created_at')
    
    context = {
        'courses': courses,
    }
    return render(request, 'dashboard/admin/courses.html', context)


@user_passes_test(is_admin)
@login_required
def admin_course_detail_view(request, course_id):
    """Admin course detail view"""
    course = get_object_or_404(Course, id=course_id)
    enrollments = Enrollment.objects.filter(course=course).select_related('user')
    lessons = Lesson.objects.filter(course=course)
    
    context = {
        'course': course,
        'enrollments': enrollments,
        'lessons': lessons,
    }
    return render(request, 'dashboard/admin/course_detail.html', context)


@user_passes_test(is_admin)
@login_required
def admin_toggle_featured_view(request, course_id):
    """Toggle course featured status"""
    course = get_object_or_404(Course, id=course_id)
    course.is_featured = not course.is_featured
    course.save()
    
    messages.success(request, f'Kurs {"top" if course.is_featured else "oddiy"} qilib belgilandi.')
    return redirect('dashboard:admin_courses')


@user_passes_test(is_admin)
@login_required
def admin_payments_view(request):
    """Admin payment management"""
    payments = Payment.objects.select_related('user', 'course').order_by('-created_at')
    
    # Filter by date
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if date_from:
        payments = payments.filter(created_at__gte=date_from)
    if date_to:
        payments = payments.filter(created_at__lte=date_to)
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        payments = payments.filter(status=status)
    
    context = {
        'payments': payments,
        'date_from': date_from,
        'date_to': date_to,
        'status': status,
    }
    return render(request, 'dashboard/admin/payments.html', context)


@user_passes_test(is_admin)
@login_required
def admin_wallets_view(request):
    """Admin wallet management"""
    wallets = Wallet.objects.select_related('user').order_by('-updated_at')
    
    context = {
        'wallets': wallets,
    }
    return render(request, 'dashboard/admin/wallets.html', context)


@user_passes_test(is_admin)
@login_required
def admin_adjust_wallet_view(request, wallet_id):
    """Manually adjust wallet balance"""
    wallet = get_object_or_404(Wallet, id=wallet_id)
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        action = request.POST.get('action')  # 'add' or 'deduct'
        
        try:
            amount = float(amount)
            if action == 'add':
                wallet.add_balance(amount)
                messages.success(request, f'{amount} so\'m qo\'shildi.')
            elif action == 'deduct':
                if wallet.deduct_balance(amount):
                    messages.success(request, f'{amount} so\'m yechildi.')
                else:
                    messages.error(request, 'Hisobda yetarli mablag\' yo\'q.')
        except ValueError:
            messages.error(request, 'Noto\'g\'ri summa.')
        
        return redirect('dashboard:admin_wallets')
    
    context = {
        'wallet': wallet,
    }
    return render(request, 'dashboard/admin/adjust_wallet.html', context)


@user_passes_test(is_admin)
@login_required
def admin_reviews_view(request):
    """Admin review management"""
    reviews = Review.objects.select_related('user', 'course').order_by('-created_at')
    
    context = {
        'reviews': reviews,
    }
    return render(request, 'dashboard/admin/reviews.html', context)


@user_passes_test(is_admin)
@login_required
def admin_delete_review_view(request, review_id):
    """Delete review"""
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    messages.success(request, 'Sharh o\'chirildi.')
    return redirect('dashboard:admin_reviews')


@user_passes_test(is_admin)
@login_required
def admin_promocodes_view(request):
    """Admin promo code management"""
    promocodes = PromoCode.objects.all().order_by('-created_at')
    
    context = {
        'promocodes': promocodes,
    }
    return render(request, 'dashboard/admin/promocodes.html', context)


@user_passes_test(is_admin)
@login_required
def admin_create_promocode_view(request):
    """Create promo code"""
    if request.method == 'POST':
        code = request.POST.get('code')
        discount_type = request.POST.get('discount_type')
        discount_value = request.POST.get('discount_value')
        min_purchase = request.POST.get('min_purchase', 0)
        max_discount = request.POST.get('max_discount')
        usage_limit = request.POST.get('usage_limit')
        valid_from = request.POST.get('valid_from')
        valid_until = request.POST.get('valid_until')
        description = request.POST.get('description')
        
        try:
            promocode = PromoCode.objects.create(
                code=code.upper(),
                discount_type=discount_type,
                discount_value=discount_value,
                min_purchase=min_purchase,
                max_discount=max_discount if max_discount else None,
                usage_limit=usage_limit if usage_limit else None,
                valid_from=valid_from,
                valid_until=valid_until,
                description=description
            )
            messages.success(request, 'Promo kod yaratildi.')
            return redirect('dashboard:admin_promocodes')
        except Exception as e:
            messages.error(request, f'Xatolik: {str(e)}')
    
    return render(request, 'dashboard/admin/create_promocode.html')


@user_passes_test(is_admin)
@login_required
def admin_toggle_promocode_view(request, promocode_id):
    """Toggle promo code active status"""
    promocode = get_object_or_404(PromoCode, id=promocode_id)
    promocode.is_active = not promocode.is_active
    promocode.save()
    
    messages.success(request, 'Promo kod holati o\'zgartirildi.')
    return redirect('dashboard:admin_promocodes')


@user_passes_test(is_admin)
@login_required
def admin_announcements_view(request):
    """Admin announcement management"""
    announcements = Announcement.objects.all().order_by('-created_at')
    
    context = {
        'announcements': announcements,
    }
    return render(request, 'dashboard/admin/announcements.html', context)


@user_passes_test(is_admin)
@login_required
def admin_create_announcement_view(request):
    """Create announcement"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        priority = request.POST.get('priority', 'medium')
        
        announcement = Announcement.objects.create(
            title=title,
            content=content,
            priority=priority
        )
        
        # Send notification to all users
        from apps.accounts.models import User
        users = User.objects.all()
        for user in users:
            Notification.objects.create(
                user=user,
                notification_type='system',
                title=title,
                message=content,
                link='/'
            )
        
        messages.success(request, 'E\'lon yaratildi va barcha foydalanuvchilarga yuborildi.')
        return redirect('dashboard:admin_announcements')
    
    return render(request, 'dashboard/admin/create_announcement.html')


@user_passes_test(is_admin)
@login_required
def admin_toggle_announcement_view(request, announcement_id):
    """Toggle announcement active status"""
    announcement = get_object_or_404(Announcement, id=announcement_id)
    announcement.is_active = not announcement.is_active
    announcement.save()
    
    messages.success(request, 'E\'lon holati o\'zgartirildi.')
    return redirect('dashboard:admin_announcements')
