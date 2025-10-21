from django.db import models


class Ingredient(models.Model):
    ALLERGENS = [
        ('seafood', 'Рыба и морепродукты'),
        ('meat', 'Мясо'),
        ('grains', 'Зерновые'),
        ('bee_products', 'Продукты пчеловодства'),
        ('nuts', 'Орехи и бобовые'),
        ('milk', 'Молочные продукты'),
    ]

    name = models.CharField(
        verbose_name='Название продукта',
        max_length=100,
        unique=True,
        help_text='Например: Курица'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        help_text='Краткое описание продукта или способа приготовления'
    )
    allergen = models.CharField(
        verbose_name='Аллерген',
        max_length=50,
        choices=ALLERGENS,
        blank=True,
        null=True,
        default=None
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    MENU_TYPES = [
        ('classic', 'Классическое'),
        ('low_carb', 'Низкоуглеводное'),
        ('vegetarian', 'Вегетарианское'),
        ('keto', 'Кето'),
    ]
    DISH_TYPES = [
        ('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('dinner', 'Ужин'),
        ('dessert', 'Десерт'),
    ]

    name = models.CharField(
        verbose_name='Название блюда',
        max_length=150,
        help_text='Название рецепта, например: Овсянка с ягодами'
    )
    diet_type = models.CharField(
        verbose_name='Тип меню',
        max_length=50,
        choices=MENU_TYPES,
        blank=True,
        null=True
    )
    dish_type = models.CharField(
        verbose_name='Тип блюда',
        max_length=50,
        choices=DISH_TYPES,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ['name']


class RecipeIngredient(models.Model):
    UNITS = [
        ('g', 'г'),
        ('ml', 'мл'),
        ('pcs', 'шт.'),
    ]
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='in_recipes'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    quantity = models.DecimalField(
        verbose_name='Количество продукта',
        max_digits=10,
        decimal_places=2,
        help_text='Сколько нужно этого продукта'
    )
    unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=50,
        choices=UNITS,
        help_text='Единица измерения ингредиента'
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
