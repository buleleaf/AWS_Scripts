# Packer AMI Builder
- Runs Packer to create an AMI
- Runs an Ansible Playbook during AMI creation

## Packer AMI Builder Config
- Creates a new AMI and builds a Manifest

## Ansible Playbook
- For POC this creates an Apache Web Server

## Shell Scripts
- install-packages.sh
    - Installs Ansible agent
    - Installs CloudWatch Agent
- update-ssm-param.sh
    - Gets the AMI ID from the Manifest JSON and updates SSM Param Store