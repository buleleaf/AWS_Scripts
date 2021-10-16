output "subnet_ids" {
  value       = [for subnet in aws_subnet.subnet : subnet.id]
  description = "Subnet ID's"
}

# This is here to give the root output something to use as the key
output "az" {
  value       = var.availability_zone
  description = "Availability Zone"
}
