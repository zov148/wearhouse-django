from django.contrib import admin
from .models import Category, Brand, BrandProfile, Size, Product

admin.site.register([Category, Brand, BrandProfile, Size, Product])
