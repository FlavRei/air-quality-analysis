### Connect to Kafka cluster
gcloud container clusters get-credentials kafka-cluster --region us-central1 --project air-quality-analysis-454417

### Deploy Kafka cluster on GKE
kubectl create namespace kafka
kubectl create -f https://strimzi.io/install/latest/?namespace=kafka -n kafka
kubectl get pods -n kafka -w
kubectl apply -f kafka-cluster.yaml -n kafka
kubectl get svc -n kafka

### Delete Kafka cluster
kubectl delete -f kafka-cluster.yaml -n kafka
kubectl delete -f https://strimzi.io/install/latest/?namespace=kafka -n kafka
kubectl delete namespace kafka

### Connect to Flink cluster
gcloud container clusters get-credentials flink-cluster --region us-central1 --project air-quality-analysis-454417

### Create secret for BigTable
kubectl create namespace flink
kubectl create secret generic gcp-credentials --from-file=credentials.json="C:\Users\flavi\Projets\air-quality-analysis-454417-0bfec0ff4e14.json" -n flink

### Deploy Flink cluster on GKE
kubectl create -f https://strimzi.io/install/latest/?namespace=flink -n flink
kubectl get pods -n flink -w
kubectl apply -f flink-jobmanager.yaml -n flink
kubectl apply -f flink-taskmanager.yaml -n flink
kubectl apply -f flink-jobmanager-service.yaml -n flink
kubectl apply -f flink-job-submit.yaml -n flink
kubectl get svc -n flink

### Access to the dashboard
kubectl port-forward service/flink-jobmanager 8081:8081 -n flink
kubectl port-forward pod/flink-jobmanager-0 8081:8081 -n flink --address 127.0.0.1

### Delete Kafka cluster
kubectl delete -f flink-jobmanager.yaml -n flink
kubectl delete -f flink-taskmanager.yaml -n flink
kubectl delete -f flink-jobmanager-service.yaml -n flink
kubectl delete -f flink-job-submit.yaml -n flink
kubectl delete -f https://strimzi.io/install/latest/?namespace=flink -n flink
kubectl delete namespace flink