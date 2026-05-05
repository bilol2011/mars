from django.db import models
from django.conf import settings
from apps.courses.models import Course


class Wishlist(models.Model):
    """
    Wishlist model for saved courses
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'
        unique_together = ('user', 'course')
    
    def __str__(self):
        return f"{self.user.email} - {self.course.title}"


class Certificate(models.Model):
    """
    Certificate model for completed courses
    """
    enrollment = models.OneToOneField('courses.Enrollment', on_delete=models.CASCADE, related_name='certificate')
    certificate_id = models.CharField(max_length=100, unique=True)
    issued_date = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'
    
    def __str__(self):
        return f"Certificate {self.certificate_id}"
    
    def save(self, *args, **kwargs):
        if not self.certificate_id:
            import uuid
            self.certificate_id = f"BIL-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)


class Notification(models.Model):
    """
    Notification model for user notifications
    """
    TYPE_CHOICES = [
        ('payment', 'To\'lov'),
        ('course', 'Kurs'),
        ('lesson', 'Dars'),
        ('system', 'Tizim'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"


class CourseRecommendation(models.Model):
    """
    AI Course recommendation for users
    """
    REASON_CHOICES = [
        ('category', 'Category Interest'),
        ('trending', 'Trending'),
        ('popular', 'Popular'),
        ('similar', 'Similar Courses'),
        ('completed', 'Based on Completed'),
        ('wishlist', 'Based on Wishlist'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendations')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='recommended_for')
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # AI confidence score
    is_clicked = models.BooleanField(default=False)
    is_enrolled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Course Recommendation'
        verbose_name_plural = 'Course Recommendations'
        unique_together = ('user', 'course')
        ordering = ['-score', '-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.course.title}"


class DailyAnalytics(models.Model):
    """
    Daily analytics for admin dashboard
    """
    date = models.DateField(unique=True)
    total_users = models.PositiveIntegerField(default=0)
    active_users = models.PositiveIntegerField(default=0)
    total_courses = models.PositiveIntegerField(default=0)
    total_enrollments = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    new_users = models.PositiveIntegerField(default=0)
    new_enrollments = models.PositiveIntegerField(default=0)
    completed_courses = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = 'Daily Analytics'
        verbose_name_plural = 'Daily Analytics'
        ordering = ['-date']
    
    def __str__(self):
        return f"Analytics for {self.date}"


class CourseAnalytics(models.Model):
    """
    Per-course analytics
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='analytics')
    date = models.DateField()
    views = models.PositiveIntegerField(default=0)
    enrollments = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    completions = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = 'Course Analytics'
        verbose_name_plural = 'Course Analytics'
        unique_together = ('course', 'date')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.course.title} - {self.date}"


class PromoCode(models.Model):
    """
    Promo code for discounts
    """
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Foiz'),
        ('fixed', 'Aniq summa'),
    ]
    
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, default='percentage')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)  # Percentage or fixed amount
    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    usage_limit = models.PositiveIntegerField(blank=True, null=True)  # null = unlimited
    used_count = models.PositiveIntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Promo Code'
        verbose_name_plural = 'Promo Codes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} - {self.discount_value}%"
    
    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        if not self.is_active:
            return False
        if now < self.valid_from or now > self.valid_until:
            return False
        if self.usage_limit and self.used_count >= self.usage_limit:
            return False
        return True
    
    def apply_discount(self, amount):
        """Apply discount to amount"""
        if self.discount_type == 'percentage':
            discount = amount * (self.discount_value / 100)
            if self.max_discount:
                discount = min(discount, self.max_discount)
            return discount
        else:
            return min(self.discount_value, amount)


class Announcement(models.Model):
    """
    Admin announcements for all users
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Past'),
        ('medium', 'O\'rtacha'),
        ('high', 'Yuqori'),
    ], default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
