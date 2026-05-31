from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.courses.models import Course

from .models import Lesson, LessonProgress, Module
from .services import calculate_course_progress, can_access_lesson, complete_lesson, get_first_incomplete_lesson, get_first_lesson, user_has_course_access


def learning_page(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_published=True)
    has_access = user_has_course_access(request.user, course)
    modules = Module.objects.filter(course=course).prefetch_related('lessons')
    current_lesson = get_first_incomplete_lesson(request.user, course) if has_access else get_first_lesson(course)

    if current_lesson and not can_access_lesson(request.user, current_lesson):
        current_lesson = Lesson.objects.filter(module__course=course, is_preview=True).select_related('module').first()

    completed_ids = set()
    progress_percentage = 0
    if request.user.is_authenticated:
        completed_ids = set(LessonProgress.objects.filter(
            user=request.user,
            lesson__module__course=course,
            completed=True,
        ).values_list('lesson_id', flat=True))
        if has_access:
            progress_percentage = calculate_course_progress(request.user, course)

    return render(request, 'lms/learning.html', {
        'course': course,
        'modules': modules,
        'current_lesson': current_lesson,
        'completed_ids': completed_ids,
        'has_access': has_access,
        'progress_percentage': progress_percentage,
    })


def lesson_page(request, lesson_id):
    lesson = get_object_or_404(Lesson.objects.select_related('module__course'), id=lesson_id)
    if not can_access_lesson(request.user, lesson):
        messages.error(request, 'Please purchase this course to access the lesson.')
        return redirect('courses:detail', slug=lesson.course.slug)

    course = lesson.course
    has_access = user_has_course_access(request.user, course)
    modules = Module.objects.filter(course=course).prefetch_related('lessons')
    completed_ids = set()
    progress_percentage = 0

    if request.user.is_authenticated and has_access:
        completed_ids = set(LessonProgress.objects.filter(
            user=request.user,
            lesson__module__course=course,
            completed=True,
        ).values_list('lesson_id', flat=True))
        progress_percentage = calculate_course_progress(request.user, course)

    return render(request, 'lms/learning.html', {
        'course': course,
        'modules': modules,
        'current_lesson': lesson,
        'completed_ids': completed_ids,
        'has_access': has_access,
        'progress_percentage': progress_percentage,
    })


@login_required
def mark_complete_view(request, lesson_id):
    lesson = get_object_or_404(Lesson.objects.select_related('module__course'), id=lesson_id)
    if request.method != 'POST':
        return redirect('lms:lesson', lesson_id=lesson.id)
    if not user_has_course_access(request.user, lesson.course):
        messages.error(request, 'Please purchase this course to complete lessons.')
        return redirect('courses:detail', slug=lesson.course.slug)

    _, percentage = complete_lesson(request.user, lesson)
    messages.success(request, 'Lesson marked complete.')
    if percentage == 100:
        messages.success(request, 'Course completed. Your certificate is ready.')
    return redirect('lms:lesson', lesson_id=lesson.id)


@login_required
def continue_learning_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_published=True)
    if not user_has_course_access(request.user, course):
        messages.error(request, 'Please purchase this course to continue learning.')
        return redirect('courses:detail', slug=course.slug)
    lesson = get_first_incomplete_lesson(request.user, course)
    if not lesson:
        messages.info(request, 'No lessons are available yet.')
        return redirect('courses:detail', slug=course.slug)
    return redirect('lms:lesson', lesson_id=lesson.id)
