from django.urls import path
from . import views

app_name = 'marche_smart'

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('customer/login/', views.customer_login, name='customer_login'),
    path('customer/signup/', views.customer_signup, name='customer_signup'),
    path('owner/login/', views.owner_login, name='owner_login'),
    path('owner/', views.owner_dashboard, name='owner_dashboard'),
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<str:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
]
