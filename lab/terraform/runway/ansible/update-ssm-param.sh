#!/bin/bash

AMI_ID=$(jq -r '.builds[-1].artifact_id' manifest.json | cut -d ":" -f2)

aws ssm put-parameter --region us-east-2 --name "AnsibleAMI" --type "String" --value $AMI_ID --overwrite