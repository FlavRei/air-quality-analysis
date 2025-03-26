import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer

KAFKA_BOOTSTRAP_SERVERS = ['34.170.23.156:9094']
TOPIC = 'air-quality'

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_sensor_data():
    """Simulates data generation from an air quality sensor."""
    return {
        "sensor_id": f"sensor_{random.randint(1, 100)}",
        "timestamp": datetime.now().isoformat(),
        "temperature": round(random.uniform(15, 35), 2),
        "humidity": round(random.uniform(30, 90), 2),
        "pm25": round(random.uniform(5, 50), 2),
        "co2": round(random.uniform(300, 800), 2),
        "nox": round(random.uniform(0, 100), 2)
    }

if __name__ == "__main__":
    print("Starting producer... Press Ctrl+C to stop.")
    try:
        while True:
            data = generate_sensor_data()
            
            producer.send(TOPIC, value=data)
            print(f"Message sent: {data}")
            
            time.sleep(3)
    except KeyboardInterrupt:
        print("Producer shutdown.")
    finally:
        producer.close()
