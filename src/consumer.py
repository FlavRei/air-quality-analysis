import json
from kafka import KafkaConsumer

BOOTSTRAP_SERVERS = ['34.170.23.156:9094']  
TOPIC = 'air-quality'

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Waiting for messages...")

for message in consumer:
    print("Message received:", message.value)
