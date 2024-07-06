from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_results, name='search_results'),
    path('all-recipes/', views.all_recipes, name='all_recipes'),
    path('add/', views.add_recipe, name='add_recipe'),
    path('recipes/delete/<str:recipe_id>/', views.delete_recipe, name='delete_recipe'),
]
