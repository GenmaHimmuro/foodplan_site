from django.contrib import admin
from foodplan_site.models import RecipeIngredient, Recipe, Ingredient, DietInfo
from subscription.models import Subscription, Promotion


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    fields = ('ingredient', 'quantity', 'unit')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'diet_type', 'dish_type', 'description')
    inlines = [RecipeIngredientInline]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'allergen')


@admin.register(DietInfo)
class DietInfoAdmin(admin.ModelAdmin):
    list_display = ('code', 'title')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'diet_type', 'start_date', 'expiring_date', 'price', 'is_active')
    readonly_fields = ('price', 'expiring_date')


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_code', 'discount_percent', 'is_active')
