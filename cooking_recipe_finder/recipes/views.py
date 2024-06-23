from django.shortcuts import render
from django.core.cache import cache
from .models import Recipe
import json

def home(request):
    return render(request, 'recipes/home.html')

def search_results(request):
    query = request.GET.get('q')
    if query:
        recipes = cache.get(query)
        if not recipes:
            recipes = Recipe.objects(name__icontains=query)
            cache.set(query, recipes.to_json(), timeout=60*15)  # Cache for 15 minutes
        else:
            recipes = json.loads(recipes)
    else:
        recipes = []
    return render(request, 'recipes/search_results.html', {'recipes': recipes})
