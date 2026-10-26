from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('about/', views.about, name='about'),
    path('database/categories/', views.database_table, {'table': 'categories'}, name='categories'),
    path('database/brands/', views.database_table, {'table': 'brands'}, name='brands'),
    path('database/profiles/', views.database_table, {'table': 'profiles'}, name='profiles'),
    path('database/sizes/', views.database_table, {'table': 'sizes'}, name='sizes'),
    path('database/products/', views.database_table, {'table': 'products'}, name='products'),
]
