from django.contrib import admin

from core.models import AcceptedCrypto, Bills, BillsRecharge, Transaction


class BillsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "types",
        "slug",
    )
    prepopulated_fields = {"slug": ("title",)}


class AcceptedCryptoAdmin(admin.ModelAdmin):
    list_display = ("title", "short_title", "is_live")


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("bill", "amount", "status")


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
        "transaction_receipt_email",
    )


admin.site.register(Bills, BillsAdmin)
admin.site.register(BillsRecharge, BillsRechargeAdmin)
admin.site.register(AcceptedCrypto, AcceptedCryptoAdmin)
admin.site.register(Transaction, TransactionAdmin)
