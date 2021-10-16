
data "aws_availability_zones" "available" {
  state = "available"
}

variable "cidr_block" {
  type        = string
  description = "VPC Cidr Block"
}

variable "region" {
  type        = string
  description = "AWS Region"
}

variable "company" {
  type        = string
  description = "Company Name"
  default     = "nxt"
}

variable "environment" {
  type        = string
  description = "Environment Name"
}

variable "vpc_subnets" {
  type        = map(any)
  description = "Subnet map"
  default     = {}
}
variable "vpc_id" {
  type        = string
  description = "VPC Id"
  default     = ""
}