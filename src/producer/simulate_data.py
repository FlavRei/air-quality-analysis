import json
import random
import time
from datetime import datetime
from faker import Faker
from kafka import KafkaProducer

fake = Faker()

KAFKA_BOOTSTRAP_SERVERS = ['34.155.116.106:9092']
KAFKA_TOPIC = 'sensor_data'

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def generate_sensor_data():
    """
    Generates a sensor data message with potential errors.
    """
    data = {
        "sensor_id": f"sensor_{random.randint(1, 100)}",
        "timestamp": datetime.now().isoformat(),
        "location": fake.city(),
        "measures": {
            "temperature": round(random.uniform(15, 35), 2),
            "humidity": round(random.uniform(30, 90), 2),
            "pm25": round(random.uniform(5, 50), 2),
            "co2": round(random.uniform(300, 800), 2)
        }
    }

    anomaly_chance = random.random()
    if anomaly_chance < 0.2:
        key_to_remove = random.choice(list(data["measures"].keys()))
        del data["measures"][key_to_remove]
    elif anomaly_chance < 0.3:
        key_to_modify = random.choice(list(data["measures"].keys()))
        data["measures"][key_to_modify] = "error"
    elif anomaly_chance < 0.4:
        data["debug_info"] = fake.sentence()

    return data


def main():
    try:
        while True:
            sensor_data = generate_sensor_data()
            print(f"Sending the message: {sensor_data}")
            producer.send(KAFKA_TOPIC, sensor_data)
            time.sleep(2)
    except KeyboardInterrupt:
        print("Stopping the simulation.")
    finally:
        producer.flush()
        producer.close()


if __name__ == "__main__":
    main()
