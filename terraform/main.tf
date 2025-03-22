provider "google" {
  project     = var.project_id
  region      = var.region
  credentials = file(var.credentials_file)
}

resource "google_container_cluster" "primary" {
  name               = "kafka-cluster"
  location           = var.region
  initial_node_count = 1
  deletion_protection = false

  node_config {
    machine_type = "n1-standard-1"
    oauth_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    tags = ["kafka-node"]
  }
}

output "kubeconfig" {
  value = google_container_cluster.primary.endpoint
}

resource "google_compute_firewall" "allow_nodeport" {
  name    = "allow-kafka-nodeport"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["30000-32767"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags = ["kafka-node"]
}

resource "google_compute_firewall" "allow_lb_kafka" {
  name    = "allow-kafka-lb-9094"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["9094"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["kafka-node"]
}
