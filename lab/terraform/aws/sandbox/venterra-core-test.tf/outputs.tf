output "vpc_arn" {
  description = "The ARN of the VPC"
  value       = aws_vpc.this.arn
}

output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.this.id
}


output "pub_subnet_by_az" {
  description = "Map of Availiability Zone/Public Subnets"
  value = {
    for subnet in module.public_subnet_group :
    subnet.az => subnet.subnet_ids
  }
}

output "pri_subnet_by_az" {
  description = "Map of Availiability Zone/Private Subnets"
  value = {
    for subnet in module.private_subnet_group :
    subnet.az => subnet.subnet_ids
  }
}
