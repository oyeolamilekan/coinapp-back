from django.db import models

from base.base_model import BaseModel
from django.utils.translation import gettext_lazy as _

class RecievingCurrenciesStatus(models.TextChoices):
    TRON = "TRX", _("TRX")
    LITECOIN = "LTC", _("LTC")
    DASH = "DASH", _("DASH")

class TransactionStatus(models.TextChoices):
    """
    This choices are text used to denote the current status of a transaction.

    SUCCESS: Transaction has been successfully processed and both parties have been settled.
    ABANDONED: If transaction has been abadoned
    """

    SUCCESS = "SUCCESS", _("SUCCESS")
    FAILED = "FAILED", _("FAILED")
    OVER_PAID = "OVER_PAID", _("OVER_PAID")

class BillStatus(models.TextChoices):
    """
    This choices are text used to denote the current status of a transaction.

    SUCCESS: Transaction has been successfully processed and both parties have been settled.
    ABANDONED: If transaction has been abadoned
    """

    SUCCESS = "SUCCESS", _("SUCCESS")
    ABANDONED = "ABANDONED", _("ABANDONED")


class BillsType(models.TextChoices):
    """
    This choices are text used to denote the current status of a transaction.

    SUCCESS: Transaction has been successfully processed and both parties have been settled.
    ABANDONED: If transaction has been abadoned
    """

    AIRTIME = "AIRTIME", _("AIRTIME")
    DATA = "DATA", _("DATA")
    POWER = "POWER", _("POWER")

class AcceptedCrypto(BaseModel):
    title = models.CharField(max_length=300)
    short_title = models.CharField(max_length=300)
    is_live = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.title} - {self.short_title}"

    class Meta:
        verbose_name_plural = "Accepted Crypto"


class Bills(BaseModel):
    title = models.CharField(max_length=300)
    slug = models.SlugField()
    types = models.CharField(
        max_length=300,
        choices=BillsType.choices,
    )
    amount = models.DecimalField(decimal_places=3, max_digits=20)

    def __str__(self) -> str:
        return f"{self.title} - {self.types} - {self.amount}"
    
    class Meta:
        verbose_name_plural = "Bills"
        ordering = ("-created",)


class BillsRecharge(BaseModel):
    bills_type = models.ForeignKey(Bills, on_delete=models.CASCADE)
    reference = models.CharField(max_length=355, blank=True, null=True)
    recieving_id = models.CharField(max_length=300)
    desposit_address = models.CharField(max_length=300)
    expected_amount = models.DecimalField(decimal_places=3, max_digits=20, default=0.00)
    related_currency = models.ForeignKey(AcceptedCrypto, on_delete=models.CASCADE, null=True)
    is_abadoned = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    transaction_receipt_email = models.CharField(max_length=300, null=True)

    def __str__(self) -> str:
        return f"{self.bills_type}"
    
    class Meta:
        verbose_name_plural = "Bills Recharge"

class Transaction(BaseModel):
    bill = models.ForeignKey(BillsRecharge, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=5, default=0.00, max_digits=20)
    status = models.CharField(max_length=300, choices=TransactionStatus.choices)

    def __str__(self) -> str:
        return f"{self.bill}"
    
    class Meta:
        verbose_name_plural = "Transaction"
