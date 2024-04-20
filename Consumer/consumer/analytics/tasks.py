import os
from pathlib import Path
from datetime import datetime
from consumer.celery import app
from .services import get_analytic_methods


BASE_DIR = Path(__file__).resolve().parent.parent
FILE = os.path.join(BASE_DIR, 'logs/log-celery.txt')
FILE_JOURNAL = os.path.join('/var/www/consumer/journal', 'journal.txt')


@app.task
def calculate_analytic():

    get_analytic_methods()

    with open(FILE, mode='a', encoding='utf8') as log:
        log.write(f"Выполнен расчет аналитических данных, время: {datetime.now()}\n")

    with open(FILE_JOURNAL, mode='a', encoding='utf8') as log:
        log.write(f"Выполнен расчет аналитических данных, время: {datetime.now()}\n")

    return
