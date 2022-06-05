from core.models import WalletAddress
from django.core.management.base import BaseCommand, CommandError
from lib.quidax import quidax


class Command(BaseCommand):
    help = "initializes the wallet address"

    def handle(self, *args, **options):
        users = quidax.users.all_sub_account()
        for user in users.get("data"):
            user_id = user.get("id")
            wallet_address_obj = quidax.wallets.fetch_payment_address(user_id, "busd")
            wallet_address = wallet_address_obj.get("data").get("address")
            wallet = WalletAddress.objects.create(desposit_address=wallet_address)
            wallet.save()
        self.stdout.write(self.style.SUCCESS("Wallet address successful created."))
