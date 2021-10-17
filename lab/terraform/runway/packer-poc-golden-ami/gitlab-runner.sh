#!/bin/bash
sudo yum update -y  &&
pip3 install runway &&

 # GitLab Runner DL and install 
sudo curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.rpm.sh | sudo bash && \\
sudo curl -L --output /usr/local/bin/gitlab-runner https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64 && \\
export GITLAB_RUNNER_DISABLE_SKEL=true; sudo -E yum install gitlab-runner -y

sleep 30 &

 # Terraform DL and install 

TERRAFORM_VER=`curl -s https://api.github.com/repos/hashicorp/terraform/releases/latest |  grep tag_name | cut -d: -f2 | tr -d \"\,\v | awk '{$1=$1};1'`
sudo wget https://releases.hashicorp.com/terraform/${TERRAFORM_VER}/terraform_${TERRAFORM_VER}_linux_amd64.zip &&
sudo unzip terraform_${TERRAFORM_VER}_linux_amd64.zip &&
sudo mv terraform /usr/local/bin/