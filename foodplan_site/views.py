from django.shortcuts import get_object_or_404, render

from .models import Recipe


def recipe_detail(request, pk: int):
    recipe = get_object_or_404(
        Recipe.objects.prefetch_related('ingredients__ingredient'), pk=pk
    )
    return render(request, 'card.html', {'recipe': recipe})


def recipe_list(request):
    diet_type = request.GET.get('diet_type')
    dish_type = request.GET.get('dish_type')

    recipes = Recipe.objects.all().order_by('name')
    if diet_type:
        recipes = recipes.filter(diet_type=diet_type)
    if dish_type:
        recipes = recipes.filter(dish_type=dish_type)

    return render(request, 'recipes_list.html', {
        'recipes': recipes,
        'diet_type': diet_type,
        'dish_type': dish_type,
    })
