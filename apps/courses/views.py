from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Avg
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from .models import Course, Category, Lesson, Enrollment, LessonProgress, LiveLesson, LiveLessonParticipant, EducationalCenter
from apps.accounts.models import Wallet, Transaction, User


def home_view(request):
    """
    Home page view
    """
    featured_courses = Course.objects.filter(is_published=True, is_featured=True)[:6]
    latest_courses = Course.objects.filter(is_published=True).order_by('-created_at')[:6]
    categories = Category.objects.all()
    
    context = {
        'featured_courses': featured_courses,
        'latest_courses': latest_courses,
        'categories': categories,
    }
    return render(request, 'home.html', context)


def courses_list_view(request):
    """
    Courses list view with search and filters
    """
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    level = request.GET.get('level', '')
    sort_by = request.GET.get('sort', 'latest')
    
    courses = Course.objects.filter(is_published=True)
    
    # Search
    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(mentor__first_name__icontains=query) |
            Q(mentor__last_name__icontains=query)
        )
    
    # Category filter
    if category_slug:
        courses = courses.filter(category__slug=category_slug)
    
    # Level filter
    if level:
        courses = courses.filter(level=level)
    
    # Sorting
    if sort_by == 'price_low':
        courses = courses.order_by('price')
    elif sort_by == 'price_high':
        courses = courses.order_by('-price')
    elif sort_by == 'popular':
        courses = courses.order_by('-students_count')
    elif sort_by == 'rating':
        courses = courses.order_by('-rating')
    else:  # latest
        courses = courses.order_by('-created_at')
    
    categories = Category.objects.all()
    
    context = {
        'courses': courses,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
        'selected_level': level,
        'sort_by': sort_by,
    }
    return render(request, 'courses/course_list.html', context)


def course_detail_view(request, slug):
    """
    Course detail view
    """
    course = get_object_or_404(Course, slug=slug, is_published=True)
    lessons = course.lessons.all()
    
    # Check if user is enrolled
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
    
    # Get related courses
    related_courses = Course.objects.filter(
        category=course.category,
        is_published=True
    ).exclude(id=course.id)[:4]
    
    context = {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled,
        'related_courses': related_courses,
    }
    return render(request, 'courses/course_detail.html', context)


def category_view(request, slug):
    """
    Category detail view
    """
    category = get_object_or_404(Category, slug=slug)
    courses = Course.objects.filter(category=category, is_published=True)
    
    context = {
        'category': category,
        'courses': courses,
    }
    return render(request, 'courses/category.html', context)


def lesson_view(request, course_slug, lesson_id):
    """
    Lesson view with progress tracking
    """
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    lesson = get_object_or_404(Lesson, course=course, id=lesson_id)
    
    enrollment = None
    lesson_progress = None
    
    # Check enrollment
    if not lesson.is_free:
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        if not enrollment:
            return redirect('courses:detail', slug=course.slug)
        
        # Get or create lesson progress
        lesson_progress, created = enrollment.lesson_progress.get_or_create(lesson=lesson)
    else:
        if request.user.is_authenticated:
            enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
            if enrollment:
                lesson_progress, created = enrollment.lesson_progress.get_or_create(lesson=lesson)
    
    # Get all lessons for navigation
    lessons = course.lessons.all()
    
    context = {
        'course': course,
        'lesson': lesson,
        'lessons': lessons,
        'enrollment': enrollment,
        'lesson_progress': lesson_progress,
    }
    return render(request, 'courses/lesson.html', context)


def purchase_course(request, slug):
    """
    Purchase course using wallet balance
    """
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    course = get_object_or_404(Course, slug=slug, is_published=True)
    
    # Check if already enrolled
    if Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.warning(request, 'Siz allaqachon bu kursga yozilgansiz.')
        return redirect('courses:detail', slug=course.slug)
    
    # Get or create wallet
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    
    # Check balance
    course_price = course.get_discounted_price()
    if wallet.balance < course_price:
        messages.error(request, f"Hisobingizda yetarli mablag' yo'q. Kerak: {course_price} so'm, Sizda: {wallet.balance} so'm")
        return redirect('accounts:wallet')
    
    # Process purchase
    with transaction.atomic():
        # Deduct from wallet
        wallet.deduct_balance(course_price)
        
        # Create enrollment
        Enrollment.objects.create(
            user=request.user,
            course=course,
            progress=0
        )
        
        # Create transaction record
        Transaction.objects.create(
            user=request.user,
            transaction_type='purchase',
            amount=course_price,
            status='success',
            description=f'Kurs sotib olish: {course.title}'
        )
        
        # Update course students count
        course.students_count += 1
        course.save()
    
    messages.success(request, 'Kurs muvaffaqiyatli sotib olindi!')
    return redirect('dashboard:my_courses')


def search_courses(request):
    """
    AJAX search for courses
    """
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    courses = Course.objects.filter(
        is_published=True
    ).filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(category__name__icontains=query)
    )[:10]
    
    results = []
    for course in courses:
        results.append({
            'id': course.id,
            'title': course.title,
            'slug': course.slug,
            'price': str(course.get_discounted_price()),
            'category': course.category.name,
            'thumbnail': course.thumbnail.url if course.thumbnail else None,
        })
    
    return JsonResponse({'results': results})


@login_required
def mark_lesson_complete(request, course_slug, lesson_id):
    """
    Mark lesson as complete and award 20 coins
    """
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    lesson = get_object_or_404(Lesson, course=course, id=lesson_id)
    
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    lesson_progress, created = enrollment.lesson_progress.get_or_create(lesson=lesson)
    
    if not lesson_progress.is_completed:
        lesson_progress.mark_completed()
        
        # Award 20 coins for completing a video lesson
        if lesson.video or lesson.video_url:
            request.user.add_coins(20)
            messages.success(request, f'{lesson.title} darsi tugatildi! +20 coin berildi!')
        else:
            messages.success(request, f'{lesson.title} darsi tugatildi!')
    
    # Get next lesson
    lessons = course.lessons.filter(order__gt=lesson.order).first()
    if lessons:
        return redirect('courses:lesson', course_slug=course.slug, lesson_id=lessons.id)
    else:
        return redirect('dashboard:my_courses')


@login_required
def continue_learning(request, course_slug):
    """
    Continue learning from last position
    """
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    
    # Find first incomplete lesson
    incomplete_lesson = enrollment.lesson_progress.filter(is_completed=False).first()
    if incomplete_lesson:
        return redirect('courses:lesson', course_slug=course.slug, lesson_id=incomplete_lesson.lesson.id)
    
    # If all completed, go to last lesson for review
    last_lesson = course.lessons.last()
    if last_lesson:
        return redirect('courses:lesson', course_slug=course.slug, lesson_id=last_lesson.id)
    
    # If no lessons, go to course detail
    return redirect('courses:detail', slug=course.slug)


def get_recommendations(request):
    """
    AI-based course recommendations
    """
    if not request.user.is_authenticated:
        courses = Course.objects.filter(is_published=True, is_featured=True)[:6]
        return render(request, 'courses/recommendations.html', {'courses': courses, 'reason': 'featured'})
    
    user = request.user
    
    # Get user's enrolled courses
    enrolled_categories = Enrollment.objects.filter(user=user).values_list('course__category', flat=True)
    
    # Get courses from enrolled categories
    recommended_courses = Course.objects.filter(
        category__in=enrolled_categories,
        is_published=True
    ).exclude(
        id__in=Enrollment.objects.filter(user=user).values_list('course__id', flat=True)
    )[:6]
    
    if not recommended_courses.exists():
        # Fallback to trending courses
        recommended_courses = Course.objects.filter(
            is_published=True
        ).order_by('-students_count')[:6]
    
    return render(request, 'courses/recommendations.html', {
        'courses': recommended_courses,
        'reason': 'personalized'
    })


@login_required
def live_lessons_list(request):
    """
    List all live lessons for enrolled courses
    """
    enrolled_courses = Enrollment.objects.filter(user=request.user).values_list('course', flat=True)
    live_lessons = LiveLesson.objects.filter(
        course__in=enrolled_courses,
        scheduled_time__gte=timezone.now()
    ).order_by('scheduled_time')
    
    return render(request, 'courses/live_lessons.html', {'live_lessons': live_lessons})


@login_required
def live_lesson_detail(request, lesson_id):
    """
    Live lesson detail and join page
    """
    live_lesson = get_object_or_404(LiveLesson, id=lesson_id)
    
    # Check if user is enrolled in the course
    if not Enrollment.objects.filter(user=request.user, course=live_lesson.course).exists():
        messages.error(request, 'Siz bu kursga yozilmagansiz.')
        return redirect('courses:detail', slug=live_lesson.course.slug)
    
    # Check if lesson is full
    if live_lesson.participants.count() >= live_lesson.max_participants:
        messages.error(request, 'Dars to\'la qatnashchilar bilan band.')
        return redirect('courses:live_lessons')
    
    # Check if user already joined
    participant, created = LiveLessonParticipant.objects.get_or_create(
        live_lesson=live_lesson,
        user=request.user
    )
    
    if created:
        participant.mark_completed()
        messages.success(request, 'Darsga qo\'shildingiz!')
    
    return render(request, 'courses/live_lesson_detail.html', {
        'live_lesson': live_lesson,
        'participant': participant
    })


@login_required
def live_lesson_join(request, lesson_id):
    """
    Join live lesson and redirect to meeting link
    """
    live_lesson = get_object_or_404(LiveLesson, id=lesson_id)
    
    # Check if user is enrolled
    if not Enrollment.objects.filter(user=request.user, course=live_lesson.course).exists():
        messages.error(request, 'Siz bu kursga yozilmagansiz.')
        return redirect('courses:detail', slug=live_lesson.course.slug)
    
    # Check if lesson is live
    if not live_lesson.is_live_now():
        messages.error(request, 'Dars hozir jonli emas.')
        return redirect('courses:live_lesson_detail', lesson_id=lesson_id)
    
    # Create participant record
    participant, created = LiveLessonParticipant.objects.get_or_create(
        live_lesson=live_lesson,
        user=request.user
    )
    
    if live_lesson.meeting_link:
        return redirect(live_lesson.meeting_link)
    else:
        # Redirect to built-in video chat
        return redirect('courses:live_lesson_video', lesson_id=lesson_id)


@login_required
def live_lesson_video(request, lesson_id):
    """
    Built-in WebRTC video chat for live lessons
    """
    live_lesson = get_object_or_404(LiveLesson, id=lesson_id)
    
    # Check if user is enrolled
    if not Enrollment.objects.filter(user=request.user, course=live_lesson.course).exists():
        messages.error(request, 'Siz bu kursga yozilmagansiz.')
        return redirect('courses:detail', slug=live_lesson.course.slug)
    
    # Check if user is a participant
    if not LiveLessonParticipant.objects.filter(live_lesson=live_lesson, user=request.user).exists():
        messages.error(request, 'Avval darsga qo\'shiling.')
        return redirect('courses:live_lesson_detail', lesson_id=lesson_id)
    
    return render(request, 'courses/live_lesson_video.html', {
        'live_lesson': live_lesson,
        'is_mentor': request.user == live_lesson.mentor
    })


def centers_list_view(request):
    """
    Educational centers list view
    """
    centers = EducationalCenter.objects.filter(is_active=True)
    
    context = {
        'centers': centers,
    }
    return render(request, 'courses/centers_list.html', context)


def center_detail_view(request, slug):
    """
    Educational center detail view
    """
    center = get_object_or_404(EducationalCenter, slug=slug, is_active=True)
    
    context = {
        'center': center,
    }
    return render(request, 'courses/center_detail.html', context)
