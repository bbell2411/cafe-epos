from api.models import MenuItem
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        items = [
            {"name": "Flat White", "unit_price_p": 350, "vat_rate_percent": 20.0},
            {"name": "Croissant", "unit_price_p": 280, "vat_rate_percent": 0.0},
            {"name": "Iced Tea", "unit_price_p": 300, "vat_rate_percent": 20.0},
            {"name": "Kids Meal", "unit_price_p": 700, "vat_rate_percent": 5.0}
        ]
        
        for item in items:
            MenuItem.objects.get_or_create(
                name=item['name'],
                defaults={
                    'unit_price_p': item['unit_price_p'],
                    'vat_rate_percent': item['vat_rate_percent']
                }
            )
        self.stdout.write(self.style.SUCCESS("MenuItem table successfully seeded!"))