terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.58"
    }
  }
}
# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

terraform {
  backend "local" {
  }
}

# Gets the latest AMI ID
data "aws_ssm_parameter" "latest-ecs" {
  name = "/aws/service/ecs/optimized-ami/amazon-linux-2/recommended"
}

resource "aws_vpc" "my_vpc" {
  cidr_block = "172.16.0.0/16"

  tags = {
    Name = "dmansfield-lab"
  }
}

resource "aws_subnet" "my_subnet" {
  vpc_id            = aws_vpc.my_vpc.id
  cidr_block        = "172.16.10.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "dmansfield-lab"
  }
}

resource "aws_network_interface" "foo" {
  subnet_id   = aws_subnet.my_subnet.id
  private_ips = ["172.16.10.100"]

  tags = {
    Name = "dmansfield-lab"
  }
}

resource "aws_instance" "web" {
  ami           = jsondecode(data.aws_ssm_parameter.latest-ecs.value).image_id
  instance_type = "t3.micro"

  network_interface {
    network_interface_id = aws_network_interface.foo.id
    device_index         = 0
  }

  tags = {
    Name = "dmansfield-lab"
  }
}
