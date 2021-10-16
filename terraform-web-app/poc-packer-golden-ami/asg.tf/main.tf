## ASG Security Group
resource "aws_security_group" "this" {
  name   = local.name_prefix
  vpc_id = var.vpc_id
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_autoscaling_group" "this" {
  name                = local.name_prefix
  vpc_zone_identifier = [var.subnet_id]
  desired_capacity    = var.desired_capacity
  max_size            = var.max_size
  min_size            = var.min_size

  launch_template {
    id      = aws_launch_template.this.id
    version = "$Latest"
  }

  dynamic "tag" {
    for_each = data.aws_default_tags.current.tags
    content {
      key                 = tag.key
      value               = tag.value
      propagate_at_launch = true
    }
  }
}

resource "aws_launch_template" "this" {
  name_prefix            = local.name_prefix
  update_default_version = true
  block_device_mappings {
    device_name = "/dev/sda1"
    ebs { volume_size = 20 }
  }
  instance_type = var.instance_type
  ebs_optimized = var.ebs_optimized
  iam_instance_profile {
    name = aws_iam_instance_profile.ecs_server_profile.arn
  }
  image_id = jsondecode(data.aws_ssm_parameter.latest-ecs.value).image_id
  key_name = var.instance_keypair
  vpc_security_group_ids = [
    aws_security_group.this.id
  ]
}

resource "aws_lb" "this" {
  name               = local.name_prefix
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb_sg.id]
  subnets            = aws_subnet.public.*.id

  enable_deletion_protection = true

  access_logs {
    bucket  = aws_s3_bucket.lb_logs.bucket
    prefix  = "test-lb"
    enabled = true
  }

  tags = {
    Environment = "production"
  }
}
