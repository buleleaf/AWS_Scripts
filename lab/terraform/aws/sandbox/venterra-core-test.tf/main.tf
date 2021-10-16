locals {
  igw_count = flatten([for az, subnets in var.vpc_subnets : [
    for subnet in subnets.public : subnet
  ]]) == [] ? 0 : 1


  tgw_attachments = { for az, subnets in var.vpc_subnets : az => {
    for name, cidr in subnets.tgw_attached : "tgw" => {
      name = name
      cidr = cidr
    }
  } }

}

output "test" {
  value = local.tgw_attachments
}

resource "aws_vpc" "this" {
  cidr_block           = var.cidr_block
  enable_dns_support   = "true"
  enable_dns_hostnames = "true"
  tags = {
    Name = var.environment
  }
}

resource "aws_internet_gateway" "this" {
  count  = local.igw_count
  vpc_id = aws_vpc.this.id
  tags = {
    Name = var.environment
  }
}

resource "aws_route_table" "public" {
  count  = local.igw_count
  vpc_id = aws_vpc.this.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.this[0].id
  }

  tags = {
    Name = "${var.environment}-public"
  }
}

# See the README for explanation of transit gateway attachments and associated subnets.

resource "aws_subnet" "transitgw_subnet" {
  for_each          = local.tgw_attachments
  vpc_id            = aws_vpc.this.id
  cidr_block        = each.value.tgw.cidr
  availability_zone = each.key

  tags = {
    Name = "${var.environment}-${each.value.tgw.name}"
  }

}

resource "aws_ec2_transit_gateway_vpc_attachment" "this" {
  subnet_ids         = [for subnet in aws_subnet.transitgw_subnet : subnet.id]
  transit_gateway_id = var.tgw_id
  vpc_id             = aws_vpc.this.id
}

resource "aws_route_table" "transitgw_route_table" {
  depends_on = [aws_ec2_transit_gateway_vpc_attachment.this]
  vpc_id     = aws_vpc.this.id

  route {
    cidr_block         = "0.0.0.0/0"
    transit_gateway_id = var.tgw_id
  }

  tags = {
    Name = "${var.environment}-transit-route-table"
  }
}

resource "aws_route_table_association" "transitgw_route_association" {
  for_each       = aws_subnet.transitgw_subnet
  subnet_id      = each.value.id
  route_table_id = aws_route_table.transitgw_route_table.id
}

module "private_subnet_group" {
  for_each          = var.vpc_subnets
  source            = "./subnet"
  availability_zone = each.key
  cidr_blocks       = each.value.private
  environment       = var.environment
  vpc_id            = aws_vpc.this.id
  route_table       = aws_route_table.transitgw_route_table.id
  subnet_type       = "private"
}

module "public_subnet_group" {
  for_each          = var.vpc_subnets
  source            = "./subnet"
  availability_zone = each.key
  cidr_blocks       = each.value.public
  environment       = var.environment
  vpc_id            = aws_vpc.this.id
  route_table       = local.igw_count == 1 ? aws_route_table.public[0].id : null
  subnet_type       = "public"
}
