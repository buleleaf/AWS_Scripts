# Provider and access setup
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.58"
    }
  }
}

provider "aws" {
  default_tags {
    tags = {
      Environment          = var.environment
      Purpose              = "webapp-poc"
      Backup-plan-schedule = "daily"
      Update-schedule      = "not-applicable"
      Uptime-scheduler     = "all"
      Created-by           = "terraform"
    }
  }
}
