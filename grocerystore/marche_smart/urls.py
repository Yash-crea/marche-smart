from django.urls import path
from . import views

app_name = 'marche_smart'

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('customer/login/', views.customer_login, name='customer_login'),
    path('owner/login/', views.owner_login, name='owner_login'),
    path('owner/', views.owner_dashboard, name='owner_dashboard'),
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
]
