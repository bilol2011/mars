from django.contrib import admin
from .models import Review, MentorReview


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'rating', 'is_verified_purchase', 'created_at')
    list_filter = ('rating', 'is_verified_purchase', 'created_at')
    search_fields = ('course__title', 'user__email', 'comment')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(MentorReview)
class MentorReviewAdmin(admin.ModelAdmin):
    list_display = ('mentor', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('mentor__email', 'user__email', 'comment')
