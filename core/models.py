from django.db import models

from base.base_model import BaseModel
from django.utils.translation import gettext_lazy as _

from core.status import (
    BillsType,
    BlockChainStatus,
    BlockChainType,
    CurrencyType,
    InstantOrderStatus,
    TransactionStatus,
)


class AcceptedCrypto(BaseModel):
    title = models.CharField(max_length=300)
    image = models.ImageField(null=True, blank=True)
    short_title = models.CharField(max_length=300)
    is_bep_20 = models.BooleanField(default=False)
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
    currency = models.CharField(
        max_length=300,
        choices=CurrencyType.choices,
        default=CurrencyType.NAIRA,
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
        default=BlockChainStatus.PENDING,
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


class WalletAddress(BaseModel):
    blockchain_type = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        choices=BlockChainType.choices,
        default=BlockChainType.BEP20,
    )
    desposit_address = models.CharField(max_length=300)

    def __str__(self) -> str:
        return f"{self.desposit_address}"

    class Meta:
        verbose_name_plural = "WalletAddress"
        ordering = ("-created",)


class POSWithdrawal(BaseModel):
    reference_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    desposit_address = models.ForeignKey(
        WalletAddress,
        on_delete=models.CASCADE,
    )
    expected_amount = models.DecimalField(
        decimal_places=5,
        max_digits=20,
        default=0.00,
    )
    blockchain_deposit_status = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        default=BlockChainStatus.PENDING,
        choices=BlockChainStatus.choices,
    )
    is_overpaid = models.BooleanField(default=False)
    is_underpaid = models.BooleanField(default=False)
    related_currency = models.ForeignKey(
        AcceptedCrypto,
        on_delete=models.CASCADE,
        null=True,
    )
    is_abadoned = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    instant_order_response = models.JSONField(default=dict)
    instant_order_status = models.CharField(
        max_length=300,
        choices=InstantOrderStatus.choices,
        default=InstantOrderStatus.DONE,
    )
    instant_order_id = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name_plural = "Withdrawal Request"
        ordering = ("-created",)


class Transaction(BaseModel):
    bill = models.ForeignKey(
        BillsRecharge,
        on_delete=models.CASCADE,
        null=True,
    )
    pos_withdrawal = models.ForeignKey(
        POSWithdrawal,
        on_delete=models.CASCADE,
        null=True,
    )
    recieve_amount = models.DecimalField(
        decimal_places=5,
        default=0.00,
        max_digits=20,
    )
    buying_amount = models.DecimalField(
        decimal_places=5,
        default=0.00,
        max_digits=20,
    )
    instant_order_response = models.JSONField(default=dict)
    bill_payment_response = models.JSONField(default=dict)
    instant_order_status = models.CharField(
        max_length=300,
        choices=InstantOrderStatus.choices,
        default=InstantOrderStatus.DONE,
    )
    instant_order_id = models.CharField(
        max_length=300,
        blank=True,
    )
    reason = models.CharField(max_length=300, blank=True)
    bill_payment_status = models.CharField(
        max_length=300,
        choices=TransactionStatus.choices,
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
