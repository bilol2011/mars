from django.db import transaction

from apps.courses.models import Enrollment

from .models import Lesson, LessonProgress


def user_has_course_access(user, course):
    return user.is_authenticated and Enrollment.objects.filter(user=user, course=course).exists()


def can_access_lesson(user, lesson):
    if lesson.is_preview:
        return True
    return user_has_course_access(user, lesson.course)


def calculate_course_progress(user, course):
    total_lessons = Lesson.objects.filter(module__course=course).count()
    if total_lessons == 0:
        return 0
    completed_lessons = LessonProgress.objects.filter(
        user=user,
        lesson__module__course=course,
        completed=True,
    ).count()
    return int((completed_lessons / total_lessons) * 100)


def get_first_lesson(course):
    return Lesson.objects.filter(module__course=course).select_related('module').order_by('module__order', 'order', 'id').first()


def get_first_incomplete_lesson(user, course):
    lessons = Lesson.objects.filter(module__course=course).select_related('module').order_by('module__order', 'order', 'id')
    completed_ids = set(LessonProgress.objects.filter(
        user=user,
        lesson__module__course=course,
        completed=True,
    ).values_list('lesson_id', flat=True))
    for lesson in lessons:
        if lesson.id not in completed_ids:
            return lesson
    return lessons.last()


@transaction.atomic
def complete_lesson(user, lesson):
    progress, _ = LessonProgress.objects.select_for_update().get_or_create(user=user, lesson=lesson)
    progress.mark_complete()

    percentage = calculate_course_progress(user, lesson.course)
    Enrollment.objects.filter(user=user, course=lesson.course).update(
        progress=percentage,
        is_completed=percentage == 100,
    )

    if percentage == 100:
        from apps.certificates.services import issue_certificate
        issue_certificate(user, lesson.course)

    return progress, percentage
