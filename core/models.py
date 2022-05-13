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


class BlockChainStatus(models.TextChoices):
    """
    This is the status of a block chain
    CONFIRMED
    REJECTED
    """

    CONFIRMED = "CONFIRMED", _("CONFIRMED")
    REJECTED = "REJECTED", _("REJECTED")
    CONFIRMATION = "CONFIRMATION", _("CONFIRMATION")


class InstantOrderStatus(models.TextChoices):
    """
    This choices are denoted the transaction status

    DONE: This transaction has been successfully executed
    CONFIRM: This transactions has successfully been queued up for execution
    CANCELLED: This order was cancelled by the exchange.
    """

    DONE = "DONE", _("DONE")
    CONFIRM = "CONFIRM", _("CONFIRM")
    CANCELLED = "CANCELLED", _("CANCELLED")


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
    image = models.ImageField(null=True)
    short_title = models.CharField(max_length=300)
    ticker = models.CharField(max_length=200, null=True, blank=True)
    is_live = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.title} - {self.short_title}"

    class Meta:
        verbose_name_plural = "Accepted Crypto"


class Network(BaseModel):
    title = models.CharField(max_length=300)
    image = models.ImageField(null=True)
    slug = models.SlugField()

    def __str__(self) -> str:
        return self.title


class Bills(BaseModel):
    title = models.CharField(max_length=300)
    network = models.ForeignKey(
        Network,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
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
    expected_amount = models.DecimalField(decimal_places=5, max_digits=20, default=0.00)
    blockchain_deposit_status = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        default=BlockChainStatus.CONFIRMED,
        choices=BlockChainStatus.choices,
    )
    is_overpaid = models.BooleanField(default=False)
    related_currency = models.ForeignKey(
        AcceptedCrypto,
        on_delete=models.CASCADE,
        null=True,
    )
    is_abadoned = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    transaction_receipt_email = models.CharField(max_length=300, null=True)

    def __str__(self) -> str:
        return f"{self.bills_type}"

    class Meta:
        verbose_name_plural = "Bills Recharge"
        ordering = ("-created",)


class Transaction(BaseModel):
    bill = models.ForeignKey(BillsRecharge, on_delete=models.CASCADE)
    recieve_amount = models.DecimalField(decimal_places=5, default=0.00, max_digits=20)
    buying_amount = models.DecimalField(decimal_places=5, default=0.00, max_digits=20)
    instant_order_response = models.JSONField(default=dict)
    bill_payment_response = models.JSONField(default=dict)
    instant_order_status = models.CharField(
        max_length=300,
        choices=InstantOrderStatus.choices,
        default=InstantOrderStatus.DONE,
    )
    instant_order_id = models.CharField(max_length=300, blank=True)
    reason = models.CharField(max_length=300, blank=True)
    bill_payment_status = models.CharField(
        max_length=300, choices=TransactionStatus.choices
    )

    def __str__(self) -> str:
        return f"{self.bill}"

    class Meta:
        verbose_name_plural = "Transaction"
        ordering = ("-created",)

    @property
    def profit(cls):
        return cls.recieve_amount - cls.buying_amount

    @property
    def blockchain(cls):
        return cls.bill.related_currency.title
