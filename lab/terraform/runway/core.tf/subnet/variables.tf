variable "availability_zone" {
  type        = string
  description = "Availability Zone"
}

variable "public_cidr" {
  type        = string
  description = "CIDR for public subnet (generally /24)"
}

variable "company" {
  type        = string
  description = "Company Name"
}

variable "environment" {
  type        = string
  description = "Environment Name"

}

variable "internet_gateway" {
  type        = string
  description = "Id of the Internet Gateway"
  default     = ""
}

variable "public_route_table" {
  type        = string
  description = "Public route table to associate with the subnet"
  default     = ""
}

variable "private_cidr" {
  type        = string
  description = "CIDR for privat subnet (generally /24)"
}

variable "vpc_id" {
  type        = string
  description = "VPC Id"
  default     = ""
}

