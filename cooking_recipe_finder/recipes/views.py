from django.shortcuts import render, redirect
from django.core.cache import cache
from .models import Recipe
import json

def home(request):
    return render(request, 'recipes/home.html')

def search_results(request):
    query = request.GET.get('q')
    if query:
        cached_result = cache.get(f"search:{query}")
        if cached_result:
            recipe_ids = json.loads(cached_result)
            recipes = [json.loads(cache.get(f"recipe:{recipe_id}")) for recipe_id in recipe_ids if cache.get(f"recipe:{recipe_id}")]
        else:
            recipes = Recipe.objects(name__icontains=query)
            cache.set(f"search:{query}", json.dumps([str(recipe.id) for recipe in recipes]), timeout=60*15)  # Cache for 15 minutes
            for recipe in recipes:
                cache.set(f"recipe:{recipe.id}", recipe.to_json(), timeout=60*15)
    else:
        recipes = []
    return render(request, 'recipes/search_results.html', {'recipes': recipes})

def all_recipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/all_recipes.html', {'recipes': recipes})