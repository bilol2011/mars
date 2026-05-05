import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bilol_project.settings')
django.setup()

from apps.accounts.models import User

users = User.objects.all()
print(f'Total users: {users.count()}')

for user in users:
    print(f'{user.email} - {user.get_full_name()} - {user.role}')
