from core.models import WalletAddress
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'initializes the wallet address'

    def handle(self, *args, **options):
        wallet = WalletAddress.objects.create(desposit_address = '')
        wallet.save()
