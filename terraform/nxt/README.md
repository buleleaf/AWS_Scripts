# NXT Farms Infrastructure

## Summary:
Infrastructure as Code for NXT Farms using runway, terraform, and kubectl to launch into a cloud (currently AWS).

### Modules

### tfstate.cfn

This is the only Cloudformation in this repo which bootstraps the state files for Terraform. It launches a s3 bucket and dynamodb table for state locking.

### core.tf

Launches VPC, Subnets, and NAT Gateways

### eks.tf

Launches AWS EKS cluster

### cloudfront.tf

Launches Cloudfront Static client with S3 as the origin