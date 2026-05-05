from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('courses/', views.courses_list_view, name='list'),
    path('course/<slug:slug>/', views.course_detail_view, name='detail'),
    path('course/<slug:slug>/purchase/', views.purchase_course, name='purchase'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('lesson/<slug:course_slug>/<int:lesson_id>/', views.lesson_view, name='lesson'),
    path('lesson/<slug:course_slug>/<int:lesson_id>/complete/', views.mark_lesson_complete, name='mark_complete'),
    path('continue/<slug:course_slug>/', views.continue_learning, name='continue'),
    path('search/', views.search_courses, name='search'),
    path('recommendations/', views.get_recommendations, name='recommendations'),
    path('live-lessons/', views.live_lessons_list, name='live_lessons'),
    path('live-lesson/<int:lesson_id>/', views.live_lesson_detail, name='live_lesson_detail'),
    path('live-lesson/<int:lesson_id>/join/', views.live_lesson_join, name='live_lesson_join'),
    path('live-lesson/<int:lesson_id>/video/', views.live_lesson_video, name='live_lesson_video'),
    path('centers/', views.centers_list_view, name='centers_list'),
    path('center/<slug:slug>/', views.center_detail_view, name='center_detail'),
]
