from django.urls import path

from . import views

app_name = 'lms'

urlpatterns = [
    path('learn/<int:course_id>/', views.learning_page, name='learn'),
    path('lesson/<int:lesson_id>/', views.lesson_page, name='lesson'),
    path('lesson/<int:lesson_id>/complete/', views.mark_complete_view, name='mark_complete'),
    path('learn/<int:course_id>/continue/', views.continue_learning_view, name='continue'),
]
