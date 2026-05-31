from decimal import Decimal

from django.conf import settings
from django.db import migrations


def create_missing_wallets(apps, schema_editor):
    Wallet = apps.get_model('wallet', 'Wallet')
    User = apps.get_model(settings.AUTH_USER_MODEL.split('.')[0], settings.AUTH_USER_MODEL.split('.')[1])
    existing_user_ids = set(Wallet.objects.values_list('user_id', flat=True))
    wallets = [
        Wallet(user_id=user_id, balance=Decimal('0.00'))
        for user_id in User.objects.exclude(id__in=existing_user_ids).values_list('id', flat=True)
    ]
    Wallet.objects.bulk_create(wallets)


class Migration(migrations.Migration):
    dependencies = [
        ('wallet', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(create_missing_wallets, migrations.RunPython.noop),
    ]
