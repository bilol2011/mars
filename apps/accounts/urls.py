from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/<str:username>/', views.profile_detail_view, name='profile_detail'),
    path('wallet/', views.wallet_view, name='wallet'),
    path('wallet/add/', views.add_balance_view, name='add_balance'),
    path('wallet/card/add/', views.add_card_view, name='add_card'),
    path('wallet/card/<int:card_id>/set-default/', views.set_default_card_view, name='set_default_card'),
    path('wallet/card/<int:card_id>/delete/', views.delete_card_view, name='delete_card'),
    path('shop/', views.shop_view, name='shop'),
    path('shop/purchase/<slug:item_slug>/', views.purchase_item_view, name='purchase_item'),
    path('shop/my-purchases/', views.my_purchases_view, name='my_purchases'),
]
