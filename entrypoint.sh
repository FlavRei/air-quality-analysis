#!/bin/bash
echo "Starting the Flink Cluster..."
/opt/flink/bin/start-cluster.sh

sleep 10

echo "Submitting the PyFlink job..."
/opt/flink/bin/flink run -py /opt/flink/job.py
