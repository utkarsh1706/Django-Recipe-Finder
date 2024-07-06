import os
from django.conf import settings

def handle_uploaded_image(image):
    static_images_dir = os.path.join(settings.BASE_DIR, 'recipes', 'static', 'recipes', 'images')
    if not os.path.exists(static_images_dir):
        os.makedirs(static_images_dir)
    image_path = os.path.join(static_images_dir, image.name)
    with open(image_path, 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)
    return os.path.join('static', 'recipes', 'images', image.name)