locals {
  name_prefix = "${var.environment}-${data.aws_region.current.name}"
}

data "aws_region" "current" {}

# Gets the latest AMI ID
data "aws_ssm_parameter" "latest-ecs" {
  name = "/aws/service/ecs/optimized-ami/amazon-linux-2/recommended"
}

data "aws_default_tags" "current" {}
