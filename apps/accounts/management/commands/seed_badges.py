from django.core.management.base import BaseCommand
from apps.accounts.models import Badge


class Command(BaseCommand):
    help = 'Seed gamification badges'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding badges...')
        
        badges_data = [
            {
                'name': 'Birinchi Kurs',
                'slug': 'birinchi-kurs',
                'description': 'Birinchi kursni tugatdingiz',
                'icon': 'fa-star',
                'points_required': 50,
                'badge_type': 'course'
            },
            {
                'name': 'Tez O\'rganuvchi',
                'slug': 'tez-organuvchi',
                'description': 'Bir kunda 10 ta dars tugatdingiz',
                'icon': 'fa-bolt',
                'points_required': 100,
                'badge_type': 'lesson'
            },
            {
                'name': 'Kurs Mutaxassisi',
                'slug': 'kurs-mutaxassisi',
                'description': '5 ta kurs tugatdingiz',
                'icon': 'fa-graduation-cap',
                'points_required': 500,
                'badge_type': 'course'
            },
            {
                'name': 'Dars Ustasi',
                'slug': 'dars-ustasi',
                'description': '50 ta dars tugatdingiz',
                'icon': 'fa-book',
                'points_required': 300,
                'badge_type': 'lesson'
            },
            {
                'name': 'Seriya Qahramoni',
                'slug': 'seriya-qahramoni',
                'description': '7 kun ketma-ket o\'qidingiz',
                'icon': 'fa-fire',
                'points_required': 150,
                'badge_type': 'streak'
            },
            {
                'name': 'Bronza O\'quvchi',
                'slug': 'bronza-organuvchi',
                'description': 'Bronza darajasiga erishdingiz',
                'icon': 'fa-medal',
                'points_required': 500,
                'badge_type': 'level'
            },
            {
                'name': 'Kumush O\'quvchi',
                'slug': 'kumush-organuvchi',
                'description': 'Kumush darajasiga erishdingiz',
                'icon': 'fa-medal',
                'points_required': 2000,
                'badge_type': 'level'
            },
            {
                'name': 'Oltin O\'quvchi',
                'slug': 'oltin-organuvchi',
                'description': 'Oltin darajasiga erishdingiz',
                'icon': 'fa-trophy',
                'points_required': 5000,
                'badge_type': 'level'
            },
            {
                'name': 'Platinum O\'quvchi',
                'slug': 'platinum-organuvchi',
                'description': 'Platinum darajasiga erishdingiz',
                'icon': 'fa-gem',
                'points_required': 10000,
                'badge_type': 'level'
            },
            {
                'name': 'Diamond O\'quvchi',
                'slug': 'diamond-organuvchi',
                'description': 'Diamond darajasiga erishdingiz',
                'icon': 'fa-crown',
                'points_required': 20000,
                'badge_type': 'level'
            },
            {
                'name': 'Dasturchi',
                'slug': 'dasturchi',
                'description': 'Dasturlash kurslarini tugatdingiz',
                'icon': 'fa-code',
                'points_required': 1000,
                'badge_type': 'category'
            },
            {
                'name': 'Dizayner',
                'slug': 'dizayner',
                'description': 'Dizayn kurslarini tugatdingiz',
                'icon': 'fa-palette',
                'points_required': 800,
                'badge_type': 'category'
            },
            {
                'name': 'Marketing Mutaxassisi',
                'slug': 'marketing-mutaxassisi',
                'description': 'Marketing kurslarini tugatdingiz',
                'icon': 'fa-bullhorn',
                'points_required': 600,
                'badge_type': 'category'
            },
        ]
        
        for badge_data in badges_data:
            badge, created = Badge.objects.get_or_create(
                slug=badge_data['slug'],
                defaults={
                    'name': badge_data['name'],
                    'description': badge_data['description'],
                    'icon': badge_data['icon'],
                    'points_required': badge_data['points_required'],
                    'badge_type': badge_data['badge_type'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created badge: {badge.name}')
            else:
                self.stdout.write(f'Badge already exists: {badge.name}')
        
        self.stdout.write(self.style.SUCCESS('Badges seeded successfully!'))
