from django.db import models
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    """
    Course category model
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Course(models.Model):
    """
    Course model
    """
    LEVEL_CHOICES = [
        ('beginner', 'Boshlang\'ich'),
        ('intermediate', 'O\'rtacha'),
        ('advanced', 'Yuqori'),
    ]
    
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500)
    thumbnail = models.ImageField(upload_to='courses/thumbnails/')
    video_preview = models.FileField(upload_to='courses/previews/', blank=True, null=True)
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    duration = models.CharField(max_length=100)  # e.g., "4 weeks", "2 months"
    total_hours = models.PositiveIntegerField(default=0)
    
    language = models.CharField(max_length=50, default='Uzbek')
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    students_count = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    reviews_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_discounted_price(self):
        return self.discount_price if self.discount_price else self.price
    
    def get_installment_price(self, months):
        return self.get_discounted_price() / months


class Lesson(models.Model):
    """
    Lesson model
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to='courses/lessons/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    duration = models.PositiveIntegerField(default=0)  # in minutes
    order = models.PositiveIntegerField(default=0)
    is_free = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def get_embed_url(self):
        """Convert YouTube URL to embed format"""
        if not self.video_url:
            return None
        
        if 'youtube.com/watch?v=' in self.video_url:
            video_id = self.video_url.split('v=')[1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        elif 'youtu.be/' in self.video_url:
            video_id = self.video_url.split('youtu.be/')[1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        elif 'youtube.com/embed/' in self.video_url:
            return self.video_url
        else:
            return self.video_url


class Enrollment(models.Model):
    """
    Enrollment model
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    progress = models.PositiveIntegerField(default=0)  # percentage
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'
        unique_together = ('user', 'course')
    
    def __str__(self):
        return f"{self.user.email} - {self.course.title}"
    
    def update_progress(self):
        """Update enrollment progress based on completed lessons"""
        total_lessons = self.course.lessons.count()
        if total_lessons > 0:
            completed_lessons = self.lesson_progress.filter(is_completed=True).count()
            self.progress = int((completed_lessons / total_lessons) * 100)
            
            if self.progress == 100 and not self.is_completed:
                self.is_completed = True
                self.completed_at = timezone.now()
            
            self.save()


class LessonProgress(models.Model):
    """
    Track user progress for each lesson
    """
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    watch_time = models.IntegerField(default=0)  # in seconds
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Lesson Progress'
        verbose_name_plural = 'Lesson Progress'
        unique_together = ('enrollment', 'lesson')
        ordering = ['lesson__order']
    
    def __str__(self):
        return f"{self.enrollment.user.email} - {self.lesson.title}"
    
    def mark_completed(self):
        """Mark lesson as completed and update enrollment progress"""
        if not self.is_completed:
            self.is_completed = True
            self.completed_at = timezone.now()
            self.save()
            self.enrollment.update_progress()


class LiveLesson(models.Model):
    """
    Live video lesson with mentor
    """
    STATUS_CHOICES = [
        ('scheduled', 'Rejalashtirilgan'),
        ('live', 'Jonli'),
        ('ended', 'Tugagan'),
        ('cancelled', 'Bekor qilingan'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='live_lessons')
    mentor = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='hosted_live_lessons', limit_choices_to={'role': 'mentor'})
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    scheduled_time = models.DateTimeField()
    duration = models.IntegerField(help_text='Davomiyligi (daqiqa)', default=60)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    meeting_link = models.URLField(blank=True, help_text='Zoom/Google Meet link')
    max_participants = models.IntegerField(default=50)
    is_recorded = models.BooleanField(default=False)
    recording_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Live Lesson'
        verbose_name_plural = 'Live Lessons'
        ordering = ['scheduled_time']
    
    def __str__(self):
        return f"{self.title} - {self.scheduled_time}"
    
    def is_live_now(self):
        """Check if lesson is currently live"""
        from django.utils import timezone
        if self.status != 'live':
            return False
        now = timezone.now()
        start_time = self.scheduled_time
        end_time = start_time + timezone.timedelta(minutes=self.duration)
        return start_time <= now <= end_time


class LiveLessonParticipant(models.Model):
    """
    Track participants in live lessons
    """
    live_lesson = models.ForeignKey(LiveLesson, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='live_lesson_participations')
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Live Lesson Participant'
        verbose_name_plural = 'Live Lesson Participants'
        unique_together = ('live_lesson', 'user')
    
    def __str__(self):
        return f"{self.user.email} - {self.live_lesson.title}"
    
    def mark_completed(self):
        """Mark lesson as completed and award points"""
        from apps.accounts.models import UserLevel
        user_level, created = UserLevel.objects.get_or_create(user=self.user)
        
        # Award points for attending live lesson
        user_level.add_points(15)
        user_level.update_streak()


class EducationalCenter(models.Model):
    """
    Educational center model
    """
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500)
    logo = models.ImageField(upload_to='centers/logos/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='centers/covers/', blank=True, null=True)
    
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=100, default='Toshkent')
    
    website = models.URLField(blank=True, null=True)
    telegram = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    reviews_count = models.PositiveIntegerField(default=0)
    students_count = models.PositiveIntegerField(default=0)
    courses_count = models.PositiveIntegerField(default=0)
    
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Educational Center'
        verbose_name_plural = 'Educational Centers'
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return self.name
    
    def clean(self):
        """Validate that city is always Tashkent"""
        from django.core.exceptions import ValidationError
        if self.city.lower() != 'toshkent':
            raise ValidationError({'city': 'Faqat Toshkent shahridagi o\'quv markazlari qabul qilinadi.'})
    
    def save(self, *args, **kwargs):
        """Force city to be Tashkent"""
        self.city = 'Toshkent'
        super().save(*args, **kwargs)
