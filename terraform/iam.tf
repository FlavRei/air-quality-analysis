resource "google_service_account" "my_service_account" {
  account_id   = "terraform"
  display_name = "Service Account for Composer and Dataflow"
}

resource "google_project_iam_member" "composer_admin" {
  project = var.project_id
  role    = "roles/composer.admin"
  member  = "serviceAccount:${google_service_account.my_service_account.email}"
}

resource "google_project_iam_member" "dataflow_admin" {
  project = var.project_id
  role    = "roles/dataflow.admin"
  member  = "serviceAccount:${google_service_account.my_service_account.email}"
}

resource "google_project_iam_member" "storage_admin" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.my_service_account.email}"
}

resource "google_project_iam_member" "bigquery_data_editor" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.my_service_account.email}"
}
