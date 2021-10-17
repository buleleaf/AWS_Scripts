locals {
  name_prefix = "${var.environment}-${data.aws_region.current.name}-packer-poc"
}

data "aws_region" "current" {}

# Gets the latest AMI ID
data "aws_ssm_parameter" "latest-ami" {
  name = "/aws/service/ami-amazon-linux-latest/"
}

data "aws_default_tags" "current" {}
