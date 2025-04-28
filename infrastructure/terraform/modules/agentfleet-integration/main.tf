/**
 * # AgentFleet Integration Module
 *
 * This module sets up the necessary infrastructure components
 * to integrate AgentFleet with Agent Starter Pack deployments.
 */

# Secret for the AgentFleet API Key
resource "google_secret_manager_secret" "agentfleet_api_key" {
  secret_id = "agentfleet-api-key"
  
  replication {
    automatic = true
  }
}

# Initial secret version - in production use terraform.tfvars or similar to provide this value
resource "google_secret_manager_secret_version" "agentfleet_api_key_version" {
  secret      = google_secret_manager_secret.agentfleet_api_key.id
  secret_data = var.agentfleet_api_key
}

# Grant Cloud Build access to the secret
resource "google_secret_manager_secret_iam_member" "cloudbuild_secretaccessor" {
  secret_id = google_secret_manager_secret.agentfleet_api_key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${var.cloudbuild_sa_email}"
}

# If using GitHub Actions, create a service account for GitHub Actions
resource "google_service_account" "github_actions_sa" {
  count        = var.use_github_actions ? 1 : 0
  account_id   = "github-actions-agentfleet"
  display_name = "Service Account for GitHub Actions AgentFleet Integration"
  project      = var.project_id
}

# Grant GitHub Actions SA access to the secret
resource "google_secret_manager_secret_iam_member" "github_actions_secretaccessor" {
  count      = var.use_github_actions ? 1 : 0
  secret_id  = google_secret_manager_secret.agentfleet_api_key.id
  role       = "roles/secretmanager.secretAccessor"
  member     = "serviceAccount:${google_service_account.github_actions_sa[0].email}"
}

# Create a custom Cloud Build trigger for agent registration
resource "google_cloudbuild_trigger" "agentfleet_registration" {
  name        = "agentfleet-registration"
  description = "Trigger for registering agents with AgentFleet"
  project     = var.project_id
  
  trigger_template {
    branch_name = "main"
    repo_name   = var.repository_name
  }
  
  filename = "infrastructure/ci-cd/agent-starter-pack-integration/agentfleet-integration.yaml"

  substitutions = {
    _AGENTFLEET_API_URL = var.agentfleet_api_url
    _STAGING_PROJECT_ID = var.staging_project_id
    _PROD_PROJECT_ID    = var.prod_project_id
    _REGION             = var.region
  }
}

# Create a custom Artifact Registry repository for the agent CLI
resource "google_artifact_registry_repository" "agentfleet_cli" {
  location      = var.region
  repository_id = "agentfleet-cli"
  description   = "Repository for AgentFleet CLI"
  format        = "DOCKER"
}
