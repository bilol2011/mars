from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('course/<slug:course_slug>/', views.payment_view, name='payment'),
    path('process/<slug:course_slug>/', views.process_payment_view, name='process'),
    path('success/<int:payment_id>/', views.payment_success_view, name='success'),
    path('cancel/<int:payment_id>/', views.payment_cancel_view, name='cancel'),
    path('history/', views.payment_history_view, name='history'),
    path('installment/<int:payment_id>/', views.installment_detail_view, name='installment_detail'),
    path('webhook/payme/', views.payme_webhook_view, name='payme_webhook'),
    path('webhook/click/', views.click_webhook_view, name='click_webhook'),
]
