from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.courses.models import Course


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lms_modules')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']
        unique_together = ('course', 'order')

    def __str__(self):
        return f'{self.course.title} - {self.title}'


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)
    is_preview = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['module__order', 'order', 'id']
        unique_together = ('module', 'order')

    def __str__(self):
        return f'{self.module.title} - {self.title}'

    @property
    def course(self):
        return self.module.course

    def get_embed_url(self):
        if 'youtube.com/watch?v=' in self.video_url:
            video_id = self.video_url.split('v=')[1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        if 'youtu.be/' in self.video_url:
            video_id = self.video_url.split('youtu.be/')[1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        return self.video_url


class LessonProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lms_lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress_records')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['lesson__module__order', 'lesson__order']
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f'{self.user.email} - {self.lesson.title}'

    def mark_complete(self):
        self.completed = True
        self.completed_at = self.completed_at or timezone.now()
        self.save(update_fields=['completed', 'completed_at'])
