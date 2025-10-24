from django.db import models

from foodplan_site.choices import ALLERGENS, MENU_TYPES, DISH_TYPES


class Allergen(models.Model):
    code = models.CharField(max_length=50, choices=ALLERGENS, unique=True)

    def __str__(self):
        return self.get_code_display()

    class Meta:
        verbose_name = 'Аллерген'
        verbose_name_plural = 'Аллергены'


class Ingredient(models.Model):
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
    allergen = models.ForeignKey(
        Allergen,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ingredients',
        verbose_name='Аллерген'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название блюда',
        max_length=150,
        help_text='Название рецепта, например: Овсянка с ягодами'
    )
    image = models.ImageField(
        verbose_name='Фото блюда',
        upload_to='dishes/',
        blank=True
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
        related_name='in_recipes',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Рецепт'
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
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f'{self.recipe.name}: {self.ingredient.name}'