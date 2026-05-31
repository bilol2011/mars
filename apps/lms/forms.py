from django import forms

from .models import Lesson, Module


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ('course', 'title', 'description', 'order')


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('module', 'title', 'description', 'video_url', 'duration_minutes', 'order', 'is_preview')
