import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bilol_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create superuser
if not User.objects.filter(email='admin@bilol.uz').exists():
    admin = User.objects.create_superuser(
        email='admin@bilol.uz',
        username='admin',
        password='admin123'
    )
    print(f"Superuser created successfully!")
    print(f"Email: admin@bilol.uz")
    print(f"Username: admin")
    print(f"Password: admin123")
else:
    print("Superuser already exists!")
