from django import forms

from foodplan_site.choices import DURATION_CHOICES, MENU_TYPES
from foodplan_site.models import Allergen


class OrderForm(forms.Form):
    duration = forms.ChoiceField(choices=DURATION_CHOICES)
    diet_type = forms.ChoiceField(choices=MENU_TYPES)

    is_breakfast = forms.BooleanField(required=False)
    is_lunch = forms.BooleanField(required=False)
    is_dinner = forms.BooleanField(required=False)
    is_dessert = forms.BooleanField(required=False)

    excluded_allergens = forms.ModelMultipleChoiceField(
        queryset=Allergen.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    promo_code = forms.CharField(required=False)

    def clean_duration(self):
        value = int(self.cleaned_data['duration'])
        return value

    def clean(self):
        cleaned = super().clean()
        if not (
            cleaned.get('is_breakfast')
            or cleaned.get('is_lunch')
            or cleaned.get('is_dinner')
            or cleaned.get('is_dessert')
        ):
            raise forms.ValidationError('Нужно выбрать хотя бы один приём пищи.')
        return cleaned

