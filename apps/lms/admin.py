from django.contrib import admin

from .models import Lesson, LessonProgress, Module


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('title', 'order', 'duration_minutes', 'is_preview')


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'description', 'course__title')
    ordering = ('course', 'order')
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'course_title', 'order', 'duration_minutes', 'is_preview', 'created_at')
    list_filter = ('is_preview', 'module__course', 'created_at')
    search_fields = ('title', 'description', 'module__title', 'module__course__title')
    ordering = ('module__course', 'module__order', 'order')

    def course_title(self, obj):
        return obj.module.course.title


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'completed_at')
    list_filter = ('completed', 'completed_at')
    search_fields = ('user__email', 'lesson__title', 'lesson__module__course__title')
    ordering = ('-completed_at',)
