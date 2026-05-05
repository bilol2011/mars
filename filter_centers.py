import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bilol_project.settings')
django.setup()

from apps.courses.models import EducationalCenter

centers = EducationalCenter.objects.all()
print(f'Total centers: {centers.count()}')

for center in centers:
    print(f'{center.name} - {center.city}')
