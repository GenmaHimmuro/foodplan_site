from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from datetime import date

from .models import Subscription, Promotion, PriceRule


for model in (Subscription, Promotion):
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass


class ActiveSubscriptionFilter(admin.SimpleListFilter):
    title = _('Активность подписки')
    parameter_name = 'active'

    def lookups(self, request, model_admin):
        return (
            ('1', _('Активные')),
            ('0', _('Неактивные')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == '1':
            return queryset.filter(expiring_date__gte=date.today())
        if value == '0':
            return queryset.filter(expiring_date__lt=date.today())
        return queryset


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'diet_type', 'duration', 'start_date', 'expiring_date',
        'is_breakfast', 'is_lunch', 'is_dinner', 'is_dessert', 'price', 'promotion', 'is_active_display',
    )
    list_filter = (
        'diet_type', 'duration', 'is_breakfast', 'is_lunch', 'is_dinner', 'is_dessert',
        'start_date', 'expiring_date', ActiveSubscriptionFilter,
    )
    search_fields = ('user__email', 'user__username', 'user__name')
    readonly_fields = ('price',)
    filter_horizontal = ('excluded_allergens',)
    autocomplete_fields = ('user', 'promotion')

    @admin.display(boolean=True, description=_('Активна'))
    def is_active_display(self, obj: Subscription):
        return obj.is_active()


@admin.register(PriceRule)
class PriceRuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'dish_type', 'duration', 'price')
    list_filter = ('dish_type', 'duration')


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'discount_code', 'discount_percent', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'discount_code')
