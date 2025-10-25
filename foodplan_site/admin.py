from django.contrib import admin

from foodplan_site.models import RecipeIngredient, Recipe, Ingredient, Allergen, DietInfo
from subscription.models import Subscription, Promotion


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    fields = ('ingredient', 'quantity', 'unit')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    pass


@admin.register(DietInfo)
class DietInfoAdmin(admin.ModelAdmin):
    list_display = ('code', 'title')
