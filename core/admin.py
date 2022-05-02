from django.contrib import admin

from core.models import Bills, BillsRecharge, Transaction

class BillsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "types",
        "slug",
    )
    prepopulated_fields = {"slug": ("title",)}

class BillsRechargeAdmin(admin.ModelAdmin):
    list_display = (
        "bills_type",
        "reference",
        "recieving_id",
        "desposit_address",
        "expected_amount",
        "recieving_currency",
        "is_abadoned",
        "is_paid",
        "transaction_receipt_email",
    )

admin.site.register(Bills, BillsAdmin)
admin.site.register(BillsRecharge, BillsRechargeAdmin)
admin.site.register(Transaction)