variable "region" {
  type        = string
  default     = "us-east-1"
  description = "Region the resources will be created in."
}

variable "vpc_id" {
  type        = string
  default     = "vpc-061a960d39acfeb6a"
  description = "VPC the resources will be created in."
}

# Subnets: talent-segregated-Fronts
variable "subnet_id" {
  type    = string
  default = ["subnet-007f105c6372d7d3c"]
}

variable "instance_type" {
  type        = string
  default     = "t2.micro"
  description = "Type of instance to launch in ASG."
}

variable "instance_keypair" {
  type        = string
  description = "ASG Instance Keypair"
  default     = "talent-packer-poc"
}

variable "desired_capacity" {
  type        = number
  default     = 1
  description = "Desired number of instances to maintain in ASG."
}

variable "max_size" {
  type        = number
  default     = 1
  description = "Max number of instances to allow in the ASG."
}

variable "min_size" {
  type        = number
  default     = 1
  description = "Min number of instances to keep in the ASG."
}

variable "ebs_optimized" {
  type        = bool
  description = "Configure whether or not to use EBS Optimized instances. Only certain instance type support this. Default is false."
  default     = false
}
