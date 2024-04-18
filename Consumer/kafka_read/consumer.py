import requests
import json
import sys, types


m = types.ModuleType('kafka.vendor.six.moves', 'Mock module')
setattr(m, 'range', range)
sys.modules['kafka.vendor.six.moves'] = m

from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'check_topic',
    bootstrap_servers='localhost:29092',
    enable_auto_commit=False
)
for msg in consumer:
    received_data = json.loads(msg.value.decode())
    r = requests.post('http://127.0.0.1:9000/api/add_checks/', json=received_data)

consumer.close()
