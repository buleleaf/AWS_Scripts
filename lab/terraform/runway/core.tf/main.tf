
### VPC ###
resource "aws_vpc" "this" {
  cidr_block           = var.cidr_block
  enable_dns_support   = "true"
  enable_dns_hostnames = "true"
  tags = {
    Name = "${var.environment}-vpc"
  }
}
### Internet Gateway ###
resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id
  tags = {
    Name = "${var.environment}-internet_gateway"
  }

}

### Route Table - Public  ###
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.this.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.this.id
  }

  tags = {
    Name = "${var.environment}-public-route-table"
  }
}

### Subnets  ###

module "subnet_group" {
  for_each           = var.vpc_subnets
  source             = "./subnet"
  availability_zone  = each.key
  public_cidr        = each.value.public
  private_cidr       = each.value.private
  company            = var.company
  environment        = var.environment
  vpc_id             = aws_vpc.this.id
  internet_gateway   = aws_internet_gateway.this.id
  public_route_table = aws_route_table.public.id

}
