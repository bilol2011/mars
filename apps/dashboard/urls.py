from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home_view, name='home'),
    path('my-courses/', views.my_courses_view, name='my_courses'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<slug:course_slug>/', views.add_to_wishlist_view, name='add_wishlist'),
    path('wishlist/remove/<slug:course_slug>/', views.remove_from_wishlist_view, name='remove_wishlist'),
    path('certificates/', views.certificates_view, name='certificates'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('settings/', views.settings_view, name='settings'),
    path('admin/analytics/', views.admin_analytics_view, name='admin_analytics'),
    
    # Admin Management URLs
    path('admin/users/', views.admin_users_view, name='admin_users'),
    path('admin/users/<int:user_id>/', views.admin_user_detail_view, name='admin_user_detail'),
    path('admin/users/<int:user_id>/block/', views.admin_block_user_view, name='admin_block_user'),
    path('admin/users/<int:user_id>/delete/', views.admin_delete_user_view, name='admin_delete_user'),
    path('admin/courses/', views.admin_courses_view, name='admin_courses'),
    path('admin/courses/<int:course_id>/', views.admin_course_detail_view, name='admin_course_detail'),
    path('admin/courses/<int:course_id>/toggle-featured/', views.admin_toggle_featured_view, name='admin_toggle_featured'),
    path('admin/payments/', views.admin_payments_view, name='admin_payments'),
    path('admin/wallets/', views.admin_wallets_view, name='admin_wallets'),
    path('admin/wallets/<int:wallet_id>/adjust/', views.admin_adjust_wallet_view, name='admin_adjust_wallet'),
    path('admin/reviews/', views.admin_reviews_view, name='admin_reviews'),
    path('admin/reviews/<int:review_id>/delete/', views.admin_delete_review_view, name='admin_delete_review'),
    path('admin/promocodes/', views.admin_promocodes_view, name='admin_promocodes'),
    path('admin/promocodes/create/', views.admin_create_promocode_view, name='admin_create_promocode'),
    path('admin/promocodes/<int:promocode_id>/toggle/', views.admin_toggle_promocode_view, name='admin_toggle_promocode'),
    path('admin/announcements/', views.admin_announcements_view, name='admin_announcements'),
    path('admin/announcements/create/', views.admin_create_announcement_view, name='admin_create_announcement'),
    path('admin/announcements/<int:announcement_id>/toggle/', views.admin_toggle_announcement_view, name='admin_toggle_announcement'),
]
