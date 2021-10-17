#!/bin/bash
sudo yum update -y &&
sudo amazon-linux-extras install ansible2 -y &&
sudo yum install amazon-cloudwatch-agent -y