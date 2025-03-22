### Update kubectl config
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
