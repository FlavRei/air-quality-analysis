variable "project_id" {
  type        = string
  description = "The GCP project ID."
}

variable "region" {
  type        = string
  default     = "europe-west9"
  description = "The GCP region to deploy resources."
}

variable "zone" {
  type        = string
  default     = "europe-west9-c"
  description = "The GCP zone to deploy resources."
}

variable "public_key_path" {
  type        = string
  description = "The public key to use for SSH access."
}
