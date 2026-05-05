import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bilol_project.settings')
django.setup()

from apps.courses.models import Course, Lesson

courses = Course.objects.all()
print(f'Total courses: {courses.count()}')

for course in courses:
    lessons = course.lessons.all()
    print(f'\n{course.title}: {lessons.count()} lessons')
    for lesson in lessons:
        has_video = bool(lesson.video_url)
        print(f'  - {lesson.title}: video={has_video}')
        if not has_video:
            print(f'    MISSING VIDEO!')
