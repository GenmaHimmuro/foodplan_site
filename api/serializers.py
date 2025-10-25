from typing import Any

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from foodplan_site.models import Allergen
from foodplan_site.choices import MENU_TYPES, DURATION_CHOICES
from subscription.models import Subscription, Promotion


def _choices_values(choices):
    return {c[0] for c in choices}


class OrderSerializer(serializers.Serializer):
    duration = serializers.IntegerField()
    diet_type = serializers.ChoiceField(choices=[c[0] for c in MENU_TYPES])

    is_breakfast = serializers.BooleanField(default=False)
    is_lunch = serializers.BooleanField(default=False)
    is_dinner = serializers.BooleanField(default=False)
    is_dessert = serializers.BooleanField(default=False)

    excluded_allergens = serializers.ListField(
        child=serializers.IntegerField(), required=False, allow_empty=True
    )
    promo_code = serializers.CharField(required=False, allow_blank=True)

    def validate_duration(self, value: int) -> int:
        allowed = _choices_values(DURATION_CHOICES)
        if value not in allowed:
            raise serializers.ValidationError(_('Недопустимый срок подписки'))
        return value

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        if not (
            attrs.get('is_breakfast')
            or attrs.get('is_lunch')
            or attrs.get('is_dinner')
            or attrs.get('is_dessert')
        ):
            raise serializers.ValidationError(_('Выберите хотя бы один приём пищи'))
        return attrs

    def _get_promotion(self, code: str | None) -> Promotion | None:
        if not code:
            return None
        return Promotion.objects.filter(discount_code=code.strip(), is_active=True).first()

    def create(self, validated_data):
        request = self.context['request']
        promo = self._get_promotion(validated_data.get('promo_code'))
        allergens_ids = validated_data.pop('excluded_allergens', [])
        validated_data.pop('promo_code', None)

        sub = Subscription(
            user=request.user,
            promotion=promo,
            **validated_data,
        )
        sub.save()
        if allergens_ids:
            allergens = Allergen.objects.filter(id__in=allergens_ids)
            sub.excluded_allergens.set(allergens)
        return sub


class PromoCheckSerializer(OrderSerializer):
    def create(self, validated_data):  # not used
        raise NotImplementedError

    def compute_price(self):
        promo = self._get_promotion(self.validated_data.get('promo_code'))
        sub = Subscription(
            user=self.context['request'].user,
            duration=self.validated_data['duration'],
            diet_type=self.validated_data['diet_type'],
            is_breakfast=self.validated_data.get('is_breakfast', False),
            is_lunch=self.validated_data.get('is_lunch', False),
            is_dinner=self.validated_data.get('is_dinner', False),
            is_dessert=self.validated_data.get('is_dessert', False),
            promotion=promo,
        )
        price = sub.calculate_price()
        return price, bool(promo)

