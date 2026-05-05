from django.contrib import admin
from .models import Category, Course, Lesson, Enrollment, LessonProgress, LiveLesson, LiveLessonParticipant, EducationalCenter


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('title', 'order', 'duration', 'is_free')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'mentor', 'price', 'level', 'is_published', 'is_featured', 'students_count', 'rating')
    list_filter = ('category', 'level', 'is_published', 'is_featured', 'created_at')
    search_fields = ('title', 'description', 'mentor__email')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonInline]
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug', 'category', 'mentor', 'short_description', 'description')
        }),
        ('Media', {
            'fields': ('thumbnail', 'video_preview')
        }),
        ('Narx va daraja', {
            'fields': ('price', 'discount_price', 'level', 'duration', 'total_hours')
        }),
        ('Qo\'shimcha', {
            'fields': ('language', 'is_published', 'is_featured')
        }),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'duration', 'is_free', 'created_at')
    list_filter = ('is_free', 'course', 'created_at')
    search_fields = ('title', 'course__title')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at', 'progress', 'is_completed')
    list_filter = ('is_completed', 'enrolled_at')
    search_fields = ('user__email', 'course__title')


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'lesson', 'is_completed', 'completed_at', 'watch_time')
    list_filter = ('is_completed', 'completed_at', 'created_at')
    search_fields = ('enrollment__user__email', 'lesson__title')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(LiveLesson)
class LiveLessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'mentor', 'scheduled_time', 'status', 'max_participants')
    list_filter = ('status', 'scheduled_time', 'course')
    search_fields = ('title', 'description', 'mentor__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(LiveLessonParticipant)
class LiveLessonParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'live_lesson', 'joined_at', 'left_at')
    list_filter = ('joined_at', 'live_lesson')
    search_fields = ('user__email', 'live_lesson__title')
    readonly_fields = ('joined_at',)


@admin.register(EducationalCenter)
class EducationalCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'phone', 'rating', 'students_count', 'courses_count', 'is_featured', 'is_active', 'created_at')
    list_filter = ('is_featured', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'phone', 'email')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'city')
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('name', 'slug', 'short_description', 'description')
        }),
        ('Media', {
            'fields': ('logo', 'cover_image')
        }),
        ('Aloqa ma\'lumotlari', {
            'fields': ('phone', 'email', 'address', 'city')
        }),
        ('Ijtimoiy tarmoqlar', {
            'fields': ('website', 'telegram', 'instagram', 'facebook')
        }),
        ('Statistika', {
            'fields': ('rating', 'reviews_count', 'students_count', 'courses_count')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active')
        }),
    )
    
    def get_queryset(self, request):
        """Only show Tashkent centers"""
        qs = super().get_queryset(request)
        return qs.filter(city='Toshkent')
