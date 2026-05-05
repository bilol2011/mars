from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('add/<slug:course_slug>/', views.add_review_view, name='add'),
    path('update/<int:review_id>/', views.update_review_view, name='update'),
    path('delete/<int:review_id>/', views.delete_review_view, name='delete'),
    path('course/<slug:course_slug>/', views.course_reviews_view, name='course_reviews'),
]
