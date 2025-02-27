provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_compute_network" "kafka_network" {
  name = "kafka-network"
}

resource "google_compute_firewall" "allow_ssh" {
  name    = "allow-ssh"
  network = google_compute_network.kafka_network.self_link

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "kafka_firewall" {
  name    = "allow-kafka"
  network = google_compute_network.kafka_network.self_link

  allow {
    protocol = "tcp"
    ports    = ["9092"]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "allow_kafka_connect" {
  name    = "allow-kafka-connect"
  network = "kafka-network"

  allow {
    protocol = "tcp"
    ports    = ["8083"]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_instance" "kafka_vm" {
  name         = "kafka-vm"
  machine_type = "e2-medium"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
    }
  }

  network_interface {
    network = google_compute_network.kafka_network.name
    access_config {}
  }

  metadata = {
    ssh-keys = "flavian.reignault:${file(var.public_key_path)}"
  }
}

output "kafka_external_ip" {
  value = google_compute_instance.kafka_vm.network_interface[0].access_config[0].nat_ip
}

resource "google_pubsub_topic" "kafka_data_topic" {
  name = "kafka-data-topic"
}

resource "google_pubsub_subscription" "kafka_data_sub" {
  name  = "kafka-data-topic-sub"
  topic = google_pubsub_topic.kafka_data_topic.name
  ack_deadline_seconds = 20
  message_retention_duration = "600s"
}

