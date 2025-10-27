from collections import OrderedDict
from foodplan_site.models import Recipe


def create_menu(user_subscription):
    diet_type = user_subscription.diet_type
    excluded_allergens = user_subscription.excluded_allergens.values_list('code', flat=True)

    available_dishes = (
        Recipe.objects
        .filter(diet_type=diet_type)
        .exclude(ingredients__ingredient__allergen__code__in=excluded_allergens)
        .order_by('?')
        .distinct()
    )

    meal_fields = OrderedDict([
        ('breakfast', user_subscription.is_breakfast),
        ('lunch', user_subscription.is_lunch),
        ('dinner', user_subscription.is_dinner),
        ('dessert', user_subscription.is_dessert),
    ])

    menu = {}

    for meal_name, is_included in meal_fields.items():
        if not is_included:
            continue

        raw_dish = available_dishes.filter(dish_type=meal_name).first()
        if not raw_dish:
            continue

        raw_ingredients = {
            ri.ingredient.name: f'{ri.quantity} {ri.unit}'
            for ri in raw_dish.ingredients.all()
        }

        menu[meal_name] = {
            'dish_title': f"{raw_dish.get_dish_type_display()}: {raw_dish.name}",
            'description': getattr(raw_dish, 'description', ''),
            'image': raw_dish.image.url if raw_dish.image else None,
            'ingredients': raw_ingredients,
        }

    return menu
