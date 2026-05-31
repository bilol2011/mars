from django.urls import path

from . import views

app_name = 'wallet'

urlpatterns = [
    path('', views.wallet_dashboard, name='dashboard'),
    path('add/', views.add_balance_view, name='add_balance'),
    path('purchase/<slug:slug>/', views.purchase_course_view, name='purchase_course'),
]
