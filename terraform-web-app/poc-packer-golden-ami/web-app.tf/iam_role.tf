locals {
  managed_policies = [
    "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore",
    "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
  ]
}

## ASG Roles and Policies
resource "aws_iam_role" "ecs_server_role" {
  name               = local.name_prefix
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role_policy.json
}

resource "aws_iam_instance_profile" "ecs_server_profile" {
  name = local.name_prefix
  role = aws_iam_role.ecs_server_role.name
}

data "aws_iam_policy_document" "ec2_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "ecs_service_policy_attach" {
  for_each   = toset(local.managed_policies)
  role       = aws_iam_role.ecs_server_role.name
  policy_arn = each.key
}
