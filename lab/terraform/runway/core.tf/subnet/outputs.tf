output "eip" {
  value       = aws_eip.this.public_ip
  description = "Elastic IP for NGW"
}

output "ngw" {
  value       = aws_nat_gateway.this.id
  description = "nat_gateway"
}

output "private_subnet" {
  value       = aws_subnet.private.id
  description = "Private Subnet"
}

output "public_subnet" {
  value       = aws_subnet.public.id
  description = "Public Subnet"
}

# This is here to give the root output something to use as the key
output "az" {
  value       = var.availability_zone
  description = "Availability Zone"
}
