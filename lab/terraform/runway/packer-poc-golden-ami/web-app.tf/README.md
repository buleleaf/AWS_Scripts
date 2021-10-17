The POC is almost complete and just needs some finshing touches before it is ready for presentation.

There are some things I need to reach out to the customer for:
- GitLab Runner token
- Verify which subnets to put the Gitlab runner server, and web application resources

### Completed
- Terraform resources for ASG and ALB tested working
	- Some resources are hard coded due to no remote tfstate
- Bash script installs software on GitLab runner
- Packer Golden AMI (from previous task)


### GitLab Runner Bash script URL resources
- GL Runner agent on AL2: http://www.notyourdadsit.com/blog/2020/10/3/gitlab-install-gitlab-runner-on-aws-linux-2
- Terraform: https://techviewleo.com/install-terraform-on-amazon-linux/



## Things that still need to be configured
- Security Groups
	- Server/client model for ALB/Web servers
- AMI latest image for EC2
- SSM Param store to get Packer AMI
	- IAM Permissions to access SSM Param store
- Outputs
- GitLab runner configured to kick off Packer/Terraform


### Apache
may need to install:
https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.WebServerDB.CreateWebServer.html

## Packer Golden AMI POC
This POC illustrates how Packer can be used to build an AMI image and update a current running web application with the new AMI.

### Packer
- Builds an AMI with Apache Web server which is installed via Ansible Playbook
- Runs a Terraform apply to update resources

### Terraform
- Builds web server resources
- Applies changes to resources
