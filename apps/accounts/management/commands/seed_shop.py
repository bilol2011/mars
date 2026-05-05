from django.core.management.base import BaseCommand
from apps.accounts.models import ShopItem


class Command(BaseCommand):
    help = 'Seed sample shop items'

    def handle(self, *args, **kwargs):
        items_data = [
            {
                'name': 'Mars Pen',
                'slug': 'mars-pen',
                'description': 'Sifatli Mars markali ruchka',
                'category': 'stationery',
                'price_coins': 100,
                'price_som': 10000,
                'stock': 50,
            },
            {
                'name': 'Keyboard Sticker',
                'slug': 'keyboard-sticker',
                'description': 'Klaviatura uchun stikerlar to\'plami',
                'category': 'accessories',
                'price_coins': 50,
                'price_som': 5000,
                'stock': 100,
            },
            {
                'name': 'Mars Mug',
                'slug': 'mars-mug',
                'description': 'Mars logosi bilan chashka',
                'category': 'accessories',
                'price_coins': 150,
                'price_som': 15000,
                'stock': 30,
            },
            {
                'name': 'Branded Cap',
                'slug': 'branded-cap',
                'description': 'Mars brendli bosh kiyim',
                'category': 'clothing',
                'price_coins': 200,
                'price_som': 20000,
                'stock': 25,
            },
            {
                'name': 'USB Flash Drive',
                'slug': 'usb-flash-drive',
                'description': '64GB USB flesh xotira',
                'category': 'electronics',
                'price_coins': 300,
                'price_som': 30000,
                'stock': 40,
            },
            {
                'name': 'Wireless Mouse',
                'slug': 'wireless-mouse',
                'description': 'Simsiz sichqon',
                'category': 'electronics',
                'price_coins': 250,
                'price_som': 25000,
                'stock': 35,
            },
            {
                'name': 'Mouse',
                'slug': 'mouse',
                'description': 'Oddiy sichqon',
                'category': 'electronics',
                'price_coins': 150,
                'price_som': 15000,
                'stock': 50,
            },
            {
                'name': 'Keyboard',
                'slug': 'keyboard',
                'description': 'Mekanik klaviatura',
                'category': 'electronics',
                'price_coins': 400,
                'price_som': 40000,
                'stock': 30,
            },
            {
                'name': 'MARS Futbolka',
                'slug': 'mars-tshirt',
                'description': 'Mars logosi bilan futbolka',
                'category': 'clothing',
                'price_coins': 200,
                'price_som': 20000,
                'stock': 40,
            },
            {
                'name': 'AirPods Max',
                'slug': 'airpods-max',
                'description': 'Apple AirPods Max quloqchin',
                'category': 'electronics',
                'price_coins': 2000,
                'price_som': 200000,
                'stock': 5,
            },
            {
                'name': 'Wireless Keyboard & Mouse',
                'slug': 'wireless-keyboard-mouse',
                'description': 'Simsiz klaviatura va sichqon to\'plami',
                'category': 'electronics',
                'price_coins': 500,
                'price_som': 50000,
                'stock': 20,
            },
            {
                'name': 'Branded Hoodie',
                'slug': 'branded-hoodie',
                'description': 'Mars brendli xudi',
                'category': 'clothing',
                'price_coins': 350,
                'price_som': 35000,
                'stock': 25,
            },
            {
                'name': 'Mars Backpack',
                'slug': 'mars-backpack',
                'description': 'Mars logosi bilan sumka',
                'category': 'accessories',
                'price_coins': 300,
                'price_som': 30000,
                'stock': 30,
            },
            {
                'name': 'AirPods',
                'slug': 'airpods',
                'description': 'Apple AirPods quloqchin',
                'category': 'electronics',
                'price_coins': 1000,
                'price_som': 100000,
                'stock': 10,
            },
            {
                'name': 'Smartwatch',
                'slug': 'smartwatch',
                'description': 'Aqlli soat',
                'category': 'electronics',
                'price_coins': 800,
                'price_som': 80000,
                'stock': 15,
            },
            {
                'name': 'Smartphone',
                'slug': 'smartphone',
                'description': 'Smartfon',
                'category': 'electronics',
                'price_coins': 3000,
                'price_som': 300000,
                'stock': 5,
            },
            {
                'name': 'Planshet Samsung',
                'slug': 'samsung-tablet',
                'description': 'Samsung planshet',
                'category': 'electronics',
                'price_coins': 2500,
                'price_som': 250000,
                'stock': 8,
            },
            {
                'name': 'Scrobar',
                'slug': 'screwdriver',
                'description': 'O\'rnatish asboblari to\'plami',
                'category': 'accessories',
                'price_coins': 100,
                'price_som': 10000,
                'stock': 50,
            },
            {
                'name': 'Notepad',
                'slug': 'notepad',
                'description': 'Qog\'oz daftar',
                'category': 'stationery',
                'price_coins': 50,
                'price_som': 5000,
                'stock': 100,
            },
            {
                'name': 'Phone Stand',
                'slug': 'phone-stand',
                'description': 'Telefon ushlagichi',
                'category': 'accessories',
                'price_coins': 80,
                'price_som': 8000,
                'stock': 60,
            },
            {
                'name': 'Mug',
                'slug': 'mug',
                'description': 'Oddiy chashka',
                'category': 'accessories',
                'price_coins': 100,
                'price_som': 10000,
                'stock': 50,
            },
            {
                'name': 'Branded Thermos',
                'slug': 'branded-thermos',
                'description': 'Mars brendli termos',
                'category': 'accessories',
                'price_coins': 250,
                'price_som': 25000,
                'stock': 30,
            },
            {
                'name': 'Branded Powerbank',
                'slug': 'branded-powerbank',
                'description': 'Mars brendli powerbank',
                'category': 'electronics',
                'price_coins': 400,
                'price_som': 40000,
                'stock': 25,
            },
            {
                'name': 'Yandex Station',
                'slug': 'yandex-station',
                'description': 'Yandex smart speaker',
                'category': 'electronics',
                'price_coins': 1500,
                'price_som': 150000,
                'stock': 10,
            },
        ]

        created_count = 0
        updated_count = 0

        for item_data in items_data:
            item, created = ShopItem.objects.get_or_create(
                slug=item_data['slug'],
                defaults=item_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {item.name}'))
            else:
                # Update existing item
                for key, value in item_data.items():
                    setattr(item, key, value)
                item.save()
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'Updated: {item.name}'))

        self.stdout.write(self.style.SUCCESS(
            f'\nSummary: {created_count} items created, {updated_count} items updated'
        ))
