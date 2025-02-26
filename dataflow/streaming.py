import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromPubSub, WriteToBigQuery
import json

def parse_message(message):
    return json.loads(message.decode('utf-8'))

options = PipelineOptions(
    project='air-quality-analysis-451718',
    region='europe-west1',
    temp_location='gs://air-quality-analysis-data/temp/',
    streaming=True
)

with beam.Pipeline(options=options) as p:
    (p
     | "ReadFromPubSub" >> ReadFromPubSub(topic="projects/air-quality-analysis-451718/topics/kafka-data-topic")
     | "ParseMessage" >> beam.Map(parse_message)
     | "WriteToBigQuery" >> WriteToBigQuery(
           table="air-quality-analysis-451718:streaming.sensor_data",
           schema='SCHEMA_AUTODETECT',
           create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
           write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
       )
    )
