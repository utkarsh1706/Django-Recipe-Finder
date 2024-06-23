from mongoengine import Document, StringField, FileField

class Recipe(Document):
    name = StringField(max_length=255, required=True)
    ingredients = StringField(required=True)
    recipe = StringField(required=True)
    image = FileField()

    def __str__(self):
        return self.name
