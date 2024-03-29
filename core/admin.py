from django.contrib import admin

from core.models import (
    AcceptedCrypto,
    Bills,
    BillsRecharge,
    Transaction,
    Network,
    WalletAddress,
    POSWithdrawal,
    POSTransaction,
)

admin.site.site_header = "COINAPP ADMIN"

admin.site.site_title = "COINAPP"


class BillsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "types",
        "slug",
    )
    prepopulated_fields = {"slug": ("title",)}


class WalletAddressAdmin(admin.ModelAdmin):
    list_display = ["blockchain_type", "desposit_address"]


class NetworkAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
    )
    prepopulated_fields = {"slug": ("title",)}


class AcceptedCryptoAdmin(admin.ModelAdmin):
    list_display = ("title", "short_title", "is_live")


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "bill",
        "recieve_amount",
        "buying_amount",
        "profit",
        "blockchain",
        "bill_payment_status",
        "instant_order_status",
    )


class BillsRechargeAdmin(admin.ModelAdmin):
    list_display = (
        "bills_type",
        "reference",
        "recieving_id",
        "desposit_address",
        "expected_amount",
        "is_abadoned",
        "is_paid",
        "related_currency",
        "blockchain_deposit_status",
        "transaction_receipt_email",
    )


class POSWithdrawalAdmin(admin.ModelAdmin):
    list_display = (
        "reference_id",
        "desposit_address",
        "expected_amount",
        "blockchain_deposit_status",
        "is_overpaid",
        "is_underpaid",
        "related_currency",
        "is_abadoned",
        "is_paid",
    )

class POSTransactionlAdmin(admin.ModelAdmin):
    list_display = (
        "reference_id",
        "is_overpaid",
        "is_paid",
        "is_overpaid",
        "amount",
        "currency",
    )

admin.site.register(POSTransaction, POSTransactionlAdmin)
admin.site.register(POSWithdrawal, POSWithdrawalAdmin)
admin.site.register(Bills, BillsAdmin)
admin.site.register(BillsRecharge, BillsRechargeAdmin)
admin.site.register(AcceptedCrypto, AcceptedCryptoAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(WalletAddress, WalletAddressAdmin)
