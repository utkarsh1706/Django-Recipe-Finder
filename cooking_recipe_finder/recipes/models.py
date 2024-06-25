from mongoengine import Document, StringField, URLField

class Recipe(Document):
    name = StringField(max_length=255, required=True)
    recipe = StringField(required=True)
    image = StringField(required=True)

    def __str__(self):
        return self.name
