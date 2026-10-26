from django.contrib import admin
from .models import Category, Brand, BrandProfile, Size, Product
from .forms import CategoryForm, BrandForm, BrandProfileForm, SizeForm, ProductForm

admin.site.site_header = 'WEARHOUSE — управление магазином'
admin.site.site_title = 'Админ-панель WEARHOUSE'
admin.site.index_title = 'Управление каталогом одежды'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    list_display = ('id', 'name', 'description')
    list_filter = ('name',)
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    form = BrandForm
    list_display = ('id', 'name', 'country')
    list_filter = ('country',)
    search_fields = ('name', 'country')
    ordering = ('name',)

@admin.register(BrandProfile)
class BrandProfileAdmin(admin.ModelAdmin):
    form = BrandProfileForm
    list_display = ('id', 'brand', 'website', 'description')
    list_filter = ('brand__country', 'brand')
    search_fields = ('brand__name', 'website', 'description')
    list_select_related = ('brand',)

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    form = SizeForm
    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('id', 'name', 'category', 'brand', 'price', 'stock', 'color', 'available_sizes')
    list_filter = ('category', 'brand', 'sizes', 'kind', 'tone')
    search_fields = ('name', 'color', 'category__name', 'brand__name')
    list_select_related = ('category', 'brand')
    list_per_page = 25
    ordering = ('id',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('sizes')

    @admin.display(description='Размеры')
    def available_sizes(self, obj):
        return ', '.join(size.name for size in obj.sizes.all())
