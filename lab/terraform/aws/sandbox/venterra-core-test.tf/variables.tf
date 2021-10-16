
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

variable "environment" {
  type        = string
  description = "Environment Name"
}

variable "vpc_subnets" {
  type = map(object({
    tgw_attached = map(string)
    private      = map(string)
    public       = map(string)
  }))
  description = "Subnet map"
}

variable "tags" {
  description = "A map of tags to add to all resources"
  type        = map(string)
  default     = {}
}

variable "tgw_id" {
  type        = string
  description = "Transit Gateway ID"
}
