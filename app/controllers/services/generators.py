import pytz
from datetime import datetime


def get_now():
    return datetime.now(
        pytz.timezone('America/Sao_Paulo'))