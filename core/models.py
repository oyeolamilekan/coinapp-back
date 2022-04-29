from django.db import models

from base.base_model import BaseModel
from django.utils.translation import gettext_lazy as _


class TransactionStatus(models.TextChoices):
    """
    This choices are text used to denote the current status of a transaction.

    SUCCESS: Transaction has been successfully processed and both parties have been settled.
    ABANDONED: If transaction has been abadoned
    """

    SUCCESS = "SUCCESS", _("SUCCESS")
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


class BillsRecharge(BaseModel):
    bills_type = models.ForeignKey(Bills, on_delete=models.CASCADE)
    recieving_id = models.CharField(max_length=300)
    desposit_address = models.CharField(max_length=300)

    def __str__(self) -> str:
        return f"{self.recieving_id} - {self.bills_type} - {self.desposit_address}"

class Transaction(BaseModel):
    bill = models.ForeignKey(BillsRecharge, on_delete=models.CASCADE)
    status = models.CharField(max_length=300, choices=TransactionStatus.choices)

    def __str__(self) -> str:
        return f"{self.bill} - {self.status}"