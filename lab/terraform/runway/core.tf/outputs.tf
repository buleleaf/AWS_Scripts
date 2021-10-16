output "vpc_arn" {
  description = "The ARN of the VPC"
  value       = aws_vpc.this.arn
}

output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.this.id
}

output "eips_by_az" {
  description = "Map of Availiability Zone/Elastic EIP's"
  value = {
    for subnet in module.subnet_group :
    subnet.az => subnet.eip
  }
}

output "ngws_by_az" {
  description = "Map of Availiability Zone/Nat Gateways"
  value = {
    for subnet in module.subnet_group :
    subnet.az => subnet.ngw
  }
}

output "pub_subnet_by_az" {
  description = "Map of Availiability Zone/Public Subnets"
  value = {
    for subnet in module.subnet_group :
    subnet.az => subnet.public_subnet
  }
}

output "pri_subnet_by_az" {
  description = "Map of Availiability Zone/Private Subnets"
  value = {
    for subnet in module.subnet_group :
    subnet.az => subnet.private_subnet
  }
}