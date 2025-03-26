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
    disk_type = "pd-standard"
    disk_size_gb = 10
    oauth_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    tags = ["kafka-node"]
  }
}

resource "google_container_cluster" "flink_cluster" {
  name               = "flink-cluster"
  location           = var.region
  initial_node_count = 1
  deletion_protection = false

  node_config {
    machine_type = "n1-standard-1"
    disk_type = "pd-standard"
    disk_size_gb = 20
    oauth_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    tags = ["flink-node"]
  }
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

resource "google_compute_firewall" "allow_flink_jobmanager" {
  name    = "allow-flink-jobmanager-8081"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["8081"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["flink-node"]
}

resource "google_bigtable_instance" "flink_instance" {
  name         = "flink-instance"
  deletion_protection = false
  
  cluster {
    cluster_id   = "flink-cluster"
    zone         = var.zone
    num_nodes    = 1
    storage_type = "HDD"
  }
}

resource "google_bigtable_table" "air_quality_table" {
  name           = "air-quality"
  deletion_protection = "UNPROTECTED"
  instance_name  = google_bigtable_instance.flink_instance.name
  column_family {
    family = "cf1"
  }
}
