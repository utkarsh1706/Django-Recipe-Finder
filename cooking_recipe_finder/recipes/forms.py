from django import forms
from django.core.exceptions import ValidationError
from .models import Recipe

class RecipeForm(forms.Form):
    name = forms.CharField(max_length=255)
    recipe = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField()

    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        if not image:
            raise ValidationError("No image found")

        if image.size > 5 * 1024 * 1024:  # 5 MB
            raise ValidationError("Image file too large (max 5 MB)")

        if not image.content_type.startswith('image'):
            raise ValidationError("File is not an image")

        return image
