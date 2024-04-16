import os
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent.parent
FILE = os.path.join(BASE_DIR, 'logs/checks.log')


def write_checks_log(data):
    with open(FILE, mode='a', encoding='utf8') as log:
        count_items = len(data["items"])
        log.write(f"Записана транзакция, время: {datetime.now()}, "
                  f"id чека: {data["transaction_id"]}, время по чеку: {data["timestamp"]}, "
                  f"всего наименований товаров: {count_items}\n")

    return None

