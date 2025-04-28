variable "project_id" {
  description = "The Google Cloud Project ID where resources will be created"
  type        = string
}

variable "region" {
  description = "The Google Cloud region where resources will be created"
  type        = string
  default     = "us-central1"
}

variable "agentfleet_api_key" {
  description = "The API key for authenticating with AgentFleet"
  type        = string
  sensitive   = true
}

variable "agentfleet_api_url" {
  description = "The URL of the AgentFleet API"
  type        = string
}

variable "cloudbuild_sa_email" {
  description = "The email of the Cloud Build service account"
  type        = string
}

variable "repository_name" {
  description = "The name of the agent repository"
  type        = string
}

variable "staging_project_id" {
  description = "The Google Cloud Project ID for staging environment"
  type        = string
}

variable "prod_project_id" {
  description = "The Google Cloud Project ID for production environment"
  type        = string
}

variable "use_github_actions" {
  description = "Whether to set up GitHub Actions integration"
  type        = bool
  default     = false
}
