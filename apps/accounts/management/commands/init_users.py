from django.core.management.base import BaseCommand
from apps.accounts.models import User, UserLevel, Wallet

class Command(BaseCommand):
    help = 'Initialize UserLevel and Wallet for all users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        self.stdout.write(f'Total users: {users.count()}')
        
        for user in users:
            UserLevel.objects.get_or_create(user=user)
            Wallet.objects.get_or_create(user=user)
        
        self.stdout.write(self.style.SUCCESS('UserLevel and Wallet created for all users'))
