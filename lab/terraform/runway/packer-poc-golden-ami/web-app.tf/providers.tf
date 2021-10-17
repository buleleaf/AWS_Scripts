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
  region = "us-east-2"
  default_tags {
    tags = {
      Name = "${var.environment}-webapp-poc"
      Environment          = var.environment
      Purpose              = "webapp-poc"
      Backup-plan-schedule = "daily"
      Update-schedule      = "not-applicable"
      Uptime-scheduler     = "all"
      Created-by           = "terraform"
    }
  }
}
