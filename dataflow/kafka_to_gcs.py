import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions
from apache_beam.io.kafka import ReadFromKafka
import json


class DecodeKafkaMessage(beam.DoFn):
    def process(self, element):
        key, value = element
        record = json.loads(value.decode('utf-8'))
        yield record


def run(argv=None):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--bootstrap_servers', required=True, help='List of Kafka servers, ex: 34.155.116.106:9092')
    parser.add_argument('--topic', required=True, help='Topic Kafka to read')
    parser.add_argument('--output', required=True, help='GCS path to write files, ex: gs://air-quality-analysis-data/raw/sensor_data')
    parser.add_argument('--max_records', type=int, default=10, help='Maximum number of records to process')
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True

    with beam.Pipeline(options=pipeline_options) as p:
        records = (
            p
            | 'ReadFromKafka' >> ReadFromKafka(
                    consumer_config={'bootstrap.servers': known_args.bootstrap_servers},
                    topics=[known_args.topic],
                    max_num_records=known_args.max_records
                )
            | 'DecodeMessage' >> beam.ParDo(DecodeKafkaMessage())
        )

        (
            records
            | 'ConvertToJson' >> beam.Map(lambda r: json.dumps(r))
            | 'WriteToGCS' >> beam.io.WriteToText(known_args.output, file_name_suffix='.json')
        )


if __name__ == '__main__':
    run()
