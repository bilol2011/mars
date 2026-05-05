from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import Review, MentorReview
from apps.courses.models import Course, Enrollment


@login_required
def add_review_view(request, course_slug):
    """
    Add a review for a course
    """
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    
    # Check if user has enrolled
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    if not enrollment:
        messages.warning(request, 'Faqat kursga yozilgan foydalanuvchilar sharh qoldirishi mumkin.')
        return redirect('courses:detail', slug=course.slug)
    
    # Check if already reviewed
    if Review.objects.filter(user=request.user, course=course).exists():
        messages.warning(request, 'Siz allaqachon sharh qoldirgansiz.')
        return redirect('courses:detail', slug=course.slug)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating and comment:
            review = Review.objects.create(
                course=course,
                user=request.user,
                rating=int(rating),
                comment=comment,
                is_verified_purchase=True
            )
            
            # Update course rating
            reviews = Review.objects.filter(course=course)
            avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
            course.rating = round(avg_rating, 2)
            course.reviews_count = reviews.count()
            course.save()
            
            messages.success(request, 'Sharh muvaffaqiyatli qo\'shildi.')
            return redirect('courses:detail', slug=course.slug)
        else:
            messages.error(request, 'Iltimos, barcha maydonlarni to\'ldiring.')
    
    return render(request, 'reviews/add_review.html', {'course': course})


@login_required
def update_review_view(request, review_id):
    """
    Update an existing review
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating and comment:
            review.rating = int(rating)
            review.comment = comment
            review.save()
            
            # Update course rating
            course = review.course
            reviews = Review.objects.filter(course=course)
            avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
            course.rating = round(avg_rating, 2)
            course.save()
            
            messages.success(request, 'Sharh yangilandi.')
            return redirect('courses:detail', slug=course.slug)
    
    return render(request, 'reviews/update_review.html', {'review': review})


@login_required
def delete_review_view(request, review_id):
    """
    Delete a review
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)
    course = review.course
    review.delete()
    
    # Update course rating
    reviews = Review.objects.filter(course=course)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    course.rating = round(avg_rating, 2)
    course.reviews_count = reviews.count()
    course.save()
    
    messages.success(request, 'Sharh o\'chirildi.')
    return redirect('courses:detail', slug=course.slug)


def course_reviews_view(request, course_slug):
    """
    View all reviews for a course
    """
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    reviews = course.reviews.all()
    
    context = {
        'course': course,
        'reviews': reviews,
    }
    return render(request, 'reviews/course_reviews.html', context)
