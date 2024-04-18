import os
import json
import logging
from pathlib import Path
from datetime import datetime

from .models import Transaction
import sys, types

logger = logging.getLogger(__name__)

m = types.ModuleType('kafka.vendor.six.moves', 'Mock module')
setattr(m, 'range', range)
sys.modules['kafka.vendor.six.moves'] = m

from kafka import KafkaProducer
from kafka.errors import KafkaError

BASE_DIR = Path(__file__).resolve().parent.parent.parent
FILE = os.path.join(BASE_DIR, 'logs/checks.log')


def write_checks_log(data):
    with open(FILE, mode='a', encoding='utf8') as log:
        count_items = len(data["items"])
        log.write(f"Записана транзакция, время: {datetime.now()}, "
                  f"id чека: {data["transaction_id"]}, время по чеку: {data["timestamp"]}, "
                  f"всего наименований товаров: {count_items}\n")

    return None


def send_to_kafka():
    """ Отправка сообщения в Kafka """

    transaction = Transaction.objects.last()
    products = transaction.items.all()

    check = {
        "transaction_id": transaction.transaction_id,
        "timestamp": transaction.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "total_amount": float(transaction.total_amount),
        "nds_amount": float(transaction.nds_amount),
        "tips_amount": float(transaction.tips_amount),
        "payment_method": transaction.payment_method,
        "place_id": transaction.place_id,
        "place_name": transaction.place_name,
    }
    items = []
    for product in products:
        item = {
            "product_id": product.product_id,
            "quantity": product.quantity,
            "price": float(product.price),
            "category": product.category,
        }
        items.append(item)

    check.update({"items": items})
    json_check = json.dumps(check).encode('utf-8')

    producer = KafkaProducer(bootstrap_servers='localhost:29092')

    try:
        future = producer.send('check_topic', json_check)
        result = future.get(timeout=10)
    except KafkaError as e:
        logger.error(f"Ошибка Kafka: {e}")

    producer.flush()
    return None
