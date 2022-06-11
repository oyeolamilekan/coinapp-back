from django.db import models

from django.utils.translation import gettext_lazy as _


class RecievingCurrenciesStatus(models.TextChoices):
    TRON = "TRX", _("TRX")
    LITECOIN = "LTC", _("LTC")
    DASH = "DASH", _("DASH")


class CurrencyType(models.TextChoices):
    DOLLARS = "DOLLARS", _("DOLLARS")
    NAIRA = "NAIRA", _("NAIRA")


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
    SUCCESSFUL: The transaction has been successful, and accepted by the blockchain
    REJECTED: The transaction has failed, and rejected by the blockchain
    PENDING: Transactions has just been initialized
    CONFIRMATION: Transaction is being confirmed by the blockchain
    """

    SUCCESSFUL = "SUCCESSFUL", _("SUCCESSFUL")
    REJECTED = "REJECTED", _("REJECTED")
    PENDING = "PENDING", _("PENDING")
    CONFIRMATION = "CONFIRMATION", _("CONFIRMATION")


class BlockChainType(models.TextChoices):
    """
    This is the status of a block chain
    SUCCESSFUL: The transaction has been successful, and accepted by the blockchain
    REJECTED: The transaction has failed, and rejected by the blockchain
    PENDING: Transactions has just been initialized
    CONFIRMATION: Transaction is being confirmed by the blockchain
    """

    BEP20 = "BEP20", _("BEP20")


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
    GIFTCARD = "GIFTCARD", _("GIFTCARD")
    DATA = "DATA", _("DATA")
    POWER = "POWER", _("POWER")