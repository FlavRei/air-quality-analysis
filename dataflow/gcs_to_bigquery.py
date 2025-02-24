import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions
import json


class CleanData(beam.DoFn):
    def process(self, element):
        record = json.loads(element)
        measures = record.get('measures', {})
        measures.setdefault('temperature', 0.0)
        measures.setdefault('humidity', 0.0)
        measures.setdefault('pm25', 0.0)
        measures.setdefault('co2', 0)
        record['measures'] = measures
        yield record


def run(argv=None):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='GCS path of JSON files, ex: gs://air-quality-analysis-data/raw/sensor_data-*.json')
    parser.add_argument('--output_table', required=True, help='Destination BigQuery table, ex: project:dataset.table')
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True

    table_schema = 'sensor_id:STRING, timestamp:TIMESTAMP, location:STRING, mesures:STRING'

    with beam.Pipeline(options=pipeline_options) as p:
        (
            p
            | 'ReadFromGCS' >> beam.io.ReadFromText(known_args.input)
            | 'CleanData' >> beam.ParDo(CleanData())
            | 'ConvertToBQ' >> beam.Map(lambda r: {
                    'sensor_id': r.get('sensor_id', ''),
                    'timestamp': r.get('timestamp', ''),
                    'location': r.get('location', ''),
                    'measures': json.dumps(r.get('measures', {}))
                })
            | 'WriteToBQ' >> beam.io.WriteToBigQuery(
                    known_args.output_table,
                    schema=table_schema,
                    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                    create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
                )
        )


if __name__ == '__main__':
    run()
