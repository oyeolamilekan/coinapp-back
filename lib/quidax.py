from quidaxapi.quidax import Quidax
from decouple import config

quidax = Quidax(config("CRYPTO_PROVIDER"))