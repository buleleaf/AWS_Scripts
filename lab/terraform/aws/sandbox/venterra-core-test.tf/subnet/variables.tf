variable "availability_zone" {
  type        = string
  description = "Availability Zone"
}

variable "cidr_blocks" {
  type        = map(string)
  description = "CIDR for subnets (generally /24)"
}

variable "environment" {
  type        = string
  description = "Environment Name"
}

variable "vpc_id" {
  type        = string
  description = "VPC Id"
}

variable "route_table" {
  type        = string
  description = "Route table to associate with the subnet"
  default     = ""
}

variable "subnet_type" {
  type        = string
  description = "prefix for subnet name tag"
  default     = ""
}
