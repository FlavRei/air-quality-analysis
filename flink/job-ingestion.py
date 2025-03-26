from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer
from pyflink.common.serialization import SimpleStringSchema
import json
from google.cloud import bigtable
import logging

logging.basicConfig(level=logging.INFO)

KAFKA_BOOTSTRAP_SERVERS = "34.58.195.179:9094"
TOPIC = "air-quality"
GROUP_ID = "pyflink-consumer-group"

def write_to_bigtable(sensor_data):
    client = bigtable.Client(project='air-quality-analysis-454417', admin=True)
    instance = client.instance('flink-instance')
    table = instance.table('air-quality')
    
    row_key = sensor_data['sensor_id'].encode()
    bt_row = table.direct_row(row_key)
    
    bt_row.set_cell('cf1', 'timestamp', sensor_data['timestamp'])
    bt_row.set_cell('cf1', 'temperature', str(sensor_data['temperature']))
    bt_row.set_cell('cf1', 'humidity', str(sensor_data['humidity']))
    bt_row.set_cell('cf1', 'pm25', str(sensor_data['pm25']))
    bt_row.set_cell('cf1', 'co2', str(sensor_data['co2']))
    bt_row.set_cell('cf1', 'nox', str(sensor_data['nox']))
    
    bt_row.commit()

def process_message(message):
    try:
        sensor_data = json.loads(message)
        logging.info("Message processed: %s", sensor_data)
        write_to_bigtable(sensor_data)
    except Exception as e:
        logging.error("Error processing message: %s", e)
        raise e

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    kafka_props = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': GROUP_ID,
        'auto.offset.reset': 'earliest'
    }
    kafka_consumer = FlinkKafkaConsumer(
        topics=TOPIC,
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props)

    ds = env.add_source(kafka_consumer)
    ds.map(lambda msg: process_message(msg))
    
    env.execute("Kafka to BigTable PyFlink Job")

if __name__ == '__main__':
    main()
