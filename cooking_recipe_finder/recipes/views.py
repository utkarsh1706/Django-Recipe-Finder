from django.shortcuts import render, redirect, get_object_or_404
from django.core.cache import cache
from django.conf import settings
from .models import Recipe
from .forms import RecipeForm
from .utils import handle_uploaded_image
import json
import os

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

def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = Recipe()
            recipe.name = form.cleaned_data['name']
            recipe.recipe = form.cleaned_data['recipe']
            recipe.image = "/" + handle_uploaded_image(request.FILES['image'])
            
            recipe.save()
            
            cache.set(f"recipe:{recipe.id}", recipe.to_json(), timeout=60*15)
            
            return redirect('home')
    else:
        form = RecipeForm()
    
    return render(request, 'recipes/add_recipe.html', {'form': form})

def delete_recipe(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        return redirect('all_recipes')
    
    if request.method == 'POST':
        image_path = os.path.join(settings.BASE_DIR, "recipes", recipe.image.lstrip('/'))
        if os.path.exists(image_path):
            os.remove(image_path)
        recipe.delete()
        cache.delete(f"recipe:{recipe_id}")
        return redirect('all_recipes')
    
    return render(request, 'recipes/confirm_delete.html', {'recipe': recipe})