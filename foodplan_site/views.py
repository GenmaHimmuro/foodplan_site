from django.shortcuts import get_object_or_404, render

from .models import Recipe


def recipe_detail(request, pk: int):
    recipe = get_object_or_404(
        Recipe.objects.prefetch_related('ingredients__ingredient'), pk=pk
    )
    return render(request, 'card.html', {'recipe': recipe})


def recipe_list(request):
    diet_type = request.GET.get('diet_type')  # classic/low_carb/vegetarian/keto
    dish_type = request.GET.get('dish_type')  # breakfast/lunch/dinner/dessert

    qs = Recipe.objects.all().order_by('name')
    if diet_type:
        qs = qs.filter(diet_type=diet_type)
    if dish_type:
        qs = qs.filter(dish_type=dish_type)

    return render(request, 'recipes_list.html', {
        'recipes': qs,
        'diet_type': diet_type,
        'dish_type': dish_type,
    })
