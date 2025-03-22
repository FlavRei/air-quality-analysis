variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "Region where to deploy the cluster"
  type        = string
  default     = "us-central1"
}

variable "credentials_file" {
  description = "Path to the service account JSON file"
  type        = string
}

variable "network" {
  description = "VPC Network Name"
  type        = string
  default     = "default"
}

variable "subnetwork" {
  description = "Subnet Name"
  type        = string
  default     = "default"
}
