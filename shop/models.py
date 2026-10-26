from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, RegexValidator
from decimal import Decimal

class Category(models.Model):
    name = models.CharField('Название', max_length=80, unique=True, validators=[MinLengthValidator(2)])
    description = models.TextField('Описание', max_length=500, blank=True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField('Название бренда', max_length=80, unique=True, validators=[MinLengthValidator(2)])
    country = models.CharField('Страна', max_length=80, validators=[MinLengthValidator(2)])
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

class BrandProfile(models.Model):
    brand = models.OneToOneField(Brand, verbose_name='Бренд', on_delete=models.CASCADE, related_name='profile')
    website = models.URLField('Сайт бренда', max_length=200)
    description = models.TextField('Описание бренда', max_length=1000, validators=[MinLengthValidator(10)])
    class Meta:
        ordering = ['brand__name']
    def __str__(self):
        return f'Профиль {self.brand}'

class Size(models.Model):
    name = models.CharField('Размер', max_length=4, unique=True, validators=[RegexValidator(r'^(XXS|XS|S|M|L|XL|XXL|XXXL)$', 'Выберите размер XXS, XS, S, M, L, XL, XXL или XXXL.')])
    class Meta:
        ordering = ['id']
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField('Название товара', max_length=120, unique=True, validators=[MinLengthValidator(2)])
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.PROTECT, related_name='products')
    brand = models.ForeignKey(Brand, verbose_name='Бренд', on_delete=models.PROTECT, related_name='products')
    sizes = models.ManyToManyField(Size, verbose_name='Доступные размеры', related_name='products')
    price = models.DecimalField('Цена, ₽', max_digits=9, decimal_places=2, validators=[MinValueValidator(Decimal('0.01')), MaxValueValidator(Decimal('1000000'))])
    stock = models.PositiveIntegerField('Остаток, шт.', default=0, validators=[MaxValueValidator(1000000)])
    color = models.CharField('Цвет', max_length=60, validators=[MinLengthValidator(2)])
    kind = models.CharField('Силуэт', max_length=10, choices=[('tee', 'Футболка'), ('hoodie', 'Худи'), ('pants', 'Брюки')])
    tone = models.CharField('Палитра', max_length=10, choices=[('cream', 'Молочный'), ('sage', 'Шалфей'), ('charcoal', 'Графит'), ('clay', 'Терракота'), ('sand', 'Песочный'), ('olive', 'Оливковый')])
    class Meta:
        ordering = ['id']
        constraints = [models.CheckConstraint(condition=models.Q(price__gte=Decimal('0.01'), price__lte=1000000), name='product_price_range')]
    def __str__(self):
        return self.name
