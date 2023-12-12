from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование продукта', 
        help_text='Введите название продукта')
    
    price = models.FloatField(verbose_name='Цена', 
        help_text='Введите цену продукта')
    
    stock = models.IntegerField(verbose_name='Остаток', 
        help_text='Введите количество продукта на складе')
    
    description = models.TextField(verbose_name='Описание', 
        help_text='Введите описание продукта', blank=True)
    
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория', 
        help_text='Выберите категорию продукта')
    
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления', 
        help_text='Дата и время добавления продукта')
    
    is_active = models.BooleanField(default=True, verbose_name='Активен', 
        help_text='Флаг активности продукта')
    
    @property
    def full_info(self):
        return f"{self.name}: {self.description}"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование категории', 
        help_text='Введите название категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
