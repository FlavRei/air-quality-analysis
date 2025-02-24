provider "google" {
  project = "air-quality-analysis-451718"
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

resource "google_compute_instance" "kafka_vm" {
  name         = "kafka-vm"
  machine_type = "e2-medium"
  zone         = "europe-west9-c"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
    }
  }

  network_interface {
    network = google_compute_network.kafka_network.name
    access_config {}
  }
}

output "kafka_external_ip" {
  value = google_compute_instance.kafka_vm.network_interface[0].access_config[0].nat_ip
}

resource "google_composer_environment" "composer_env" {
  name   = "air-quality-composer"
  region = var.region

  config {
    software_config {
      image_version = "composer-3-airflow-2.10.2"
    }
  }
}
