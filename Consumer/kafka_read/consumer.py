import requests
import json
import sys, types, os
from pathlib import Path
from dotenv import load_dotenv


m = types.ModuleType('kafka.vendor.six.moves', 'Mock module')
setattr(m, 'range', range)
sys.modules['kafka.vendor.six.moves'] = m

from kafka import KafkaConsumer
from kafka.errors import KafkaError


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

KAFKA_CONFIG = {
    "bootstrap_servers": os.getenv('BOOTSTRAP_SERVERS', 'localhost:29092'),
    "topic": os.getenv('TOPIC', 'check_topic'),
}

URL = os.getenv('URL', 'http://localhost:9000/api/add_checks/')

consumer = KafkaConsumer(
    KAFKA_CONFIG["topic"],
    bootstrap_servers=KAFKA_CONFIG["bootstrap_servers"],
    enable_auto_commit=False
)
for msg in consumer:
    received_data = json.loads(msg.value.decode())
    r = requests.post(url=URL, json=received_data)

consumer.close()
