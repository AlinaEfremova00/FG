import json
from django.core.management.base import BaseCommand
from recipes.models import Ingredient

class Command(BaseCommand):
    help = 'Загружает ингредиенты из JSON-файла'

    def handle(self, *args, **kwargs):
        with open('data/ingredients.json', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                name = item['name']
                unit = item['measurement_unit']
                Ingredient.objects.get_or_create(name=name, measurement_unit=unit)
        self.stdout.write(self.style.SUCCESS('Ингредиенты загружены!'))
