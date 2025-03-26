FROM apache/flink:1.15-scala_2.12

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    net-tools curl \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pyflink apache-flink google-cloud-bigtable protobuf==3.20.1

RUN curl -L -o /opt/flink/lib/flink-connector-kafka_2.12-1.15.0.jar https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/1.15.0/flink-connector-kafka-1.15.0.jar
RUN curl -L -o /opt/flink/lib/kafka-clients-2.8.0.jar https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/2.8.0/kafka-clients-2.8.0.jar

COPY flink/job-ingestion.py /opt/flink/job-ingestion.py
COPY flink/flink-conf.yaml /opt/flink/conf/flink-conf.yaml

ENTRYPOINT ["/opt/flink/bin/jobmanager.sh", "start-foreground"]
