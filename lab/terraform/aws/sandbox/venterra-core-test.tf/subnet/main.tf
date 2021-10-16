resource "aws_subnet" "subnet" {
  # for_each        = { for subnet in var.cidr_blocks : subnet.name => subnet.cidr }
  for_each          = var.cidr_blocks
  vpc_id            = var.vpc_id
  cidr_block        = each.value
  availability_zone = var.availability_zone

  tags = {
    Name = each.key
  }
}

resource "aws_route_table_association" "route_table_association" {
  for_each       = aws_subnet.subnet
  subnet_id      = each.value.id
  route_table_id = var.route_table
}
