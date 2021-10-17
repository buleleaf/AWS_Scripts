## ASG Resources

resource "aws_security_group" "asg" {
  name   = "${local.name_prefix}-asg"
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
  vpc_zone_identifier = ["${var.asg_subnet}",""]
  desired_capacity    = var.desired_capacity
  max_size            = var.max_size
  min_size            = var.min_size
  launch_configuration = aws_launch_configuration.this.name

  dynamic "tag" {
    for_each = data.aws_default_tags.current.tags
    content {
      key                 = tag.key
      value               = tag.value
      propagate_at_launch = true
    }
  }
}

resource "aws_launch_configuration" "this" {
  name            = local.name_prefix
  image_id = "ami-074cce78125f09d61"
  # image_id = jsondecode(data.aws_ssm_parameter.latest-ami.value).image_id
  key_name = "dmansfield-lab"
  # key_name = var.instance_keypair
  instance_type = "t2.micro"
  iam_instance_profile = aws_iam_instance_profile.ecs_server_profile.name
  security_groups = [aws_security_group.asg.id]
  root_block_device {
    volume_size = 15
  }
}

# ALB Resources

resource "aws_security_group" "alb" {
  name   = "${local.name_prefix}-alb"
  vpc_id = var.vpc_id
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lb" "front_end" {
  name               = local.name_prefix
  internal           = true
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.alb_subnets

  enable_deletion_protection = true
}

resource "aws_lb_listener" "front_end" {
  load_balancer_arn = aws_lb.front_end.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.front_end.arn
  }
}

resource "aws_lb_target_group" "front_end" {
  name     = local.name_prefix
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id
}

resource "aws_autoscaling_attachment" "asg_attachment_alb" {
  autoscaling_group_name = aws_autoscaling_group.this.id
  alb_target_group_arn   = aws_lb_target_group.front_end.arn
}