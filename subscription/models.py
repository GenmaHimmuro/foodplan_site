from datetime import date
from decimal import Decimal

from dateutil.relativedelta import relativedelta

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from accounts.models import CustomUser
from foodplan_site.choices import DISH_TYPES, DURATION_CHOICES, MENU_TYPES
from foodplan_site.models import Allergen


class Subscription(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь'
    )
    duration = models.PositiveIntegerField(
        choices=DURATION_CHOICES,
        default=1,
        verbose_name='Срок подписки (в месяцах)'
    )
    start_date = models.DateField(
        default=date.today,
        verbose_name='Дата начала'
    )
    expiring_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата окончания'
    )

    diet_type = models.CharField(
        verbose_name='Тип меню',
        max_length=50,
        choices=MENU_TYPES,
        blank=True,
        null=True
    )

    is_breakfast = models.BooleanField(
        default=False,
        verbose_name='Завтрак включён'
    )
    is_lunch = models.BooleanField(
        default=False,
        verbose_name='Обед включён'
    )
    is_dinner = models.BooleanField(
        default=False,
        verbose_name='Ужин включён'
    )
    is_dessert = models.BooleanField(
        default=False,
        verbose_name='Десерт включён'
    )

    excluded_allergens = models.ManyToManyField(
        Allergen,
        blank=True,
        related_name='subscriptions',
        verbose_name='Исключаемые аллергены'
    )

    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Итоговая стоимость подписки'
    )
    promotion = models.ForeignKey(
        'Promotion',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='subscriptions',
        verbose_name='Использованный промо-код'
    )
    persons = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name='Количество персон')

    def save(self, *args, **kwargs):
        if not self.expiring_date:
            self.expiring_date = self.start_date + relativedelta(months=self.duration)
        if self.price is None:
            self.price = self.calculate_price()
        super().save(*args, **kwargs)

    def is_active(self):
        return self.expiring_date >= date.today()

    def calculate_price(self):
        total = 0
        included_dishes = []

        if self.is_breakfast:
            included_dishes.append('breakfast')
        if self.is_lunch:
            included_dishes.append('lunch')
        if self.is_dinner:
            included_dishes.append('dinner')
        if self.is_dessert:
            included_dishes.append('dessert')

        for dish_type in included_dishes:
            try:
                price_rule = PriceRule.objects.get(dish_type=dish_type, duration=self.duration)
                total += price_rule.price
            except PriceRule.DoesNotExist:
                continue

        if self.promotion and self.promotion.is_active and self.promotion.discount_percent:
            discount = Decimal('1') - (self.promotion.discount_percent / Decimal('100'))
            total = total * discount
        return total

    def __str__(self):
        return f'Подписка пользователя {self.user}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        indexes = [
            models.Index(fields=['user', 'expiring_date']),
            models.Index(fields=['start_date']),
        ]


class PriceRule(models.Model):
    dish_type = models.CharField(
        max_length=50,
        choices=DISH_TYPES,
        verbose_name='Тип блюда'
    )
    duration = models.PositiveIntegerField(
        choices=DURATION_CHOICES,
        default=1,
        verbose_name='Продолжительность подписки'
    )
    price = models.DecimalField(
        verbose_name='Стоимость за позицию в подписке',
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        unique_together = ('dish_type', 'duration')
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self):
        return f'{self.get_dish_type_display()} — {self.get_duration_display()} — {self.price}₽'


class Promotion(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название акции'
    )
    discount_code = models.CharField(
        max_length=50,
        verbose_name='Код для получения скидки',
        unique=True
    )

    discount_percent = models.DecimalField(
        verbose_name='Размер скидки в процентах',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    is_active = models.BooleanField(default=False, verbose_name='Активна')

    class Meta:
        verbose_name = 'Промо-код'
        verbose_name_plural = 'Промо-коды'

    def __str__(self):
        return self.name
