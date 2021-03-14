# pip install boto3

import boto3
import json

region = 'ap-southeast-1'

iam_client = boto3.client('iam', region_name=region)

managed_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "cloudwatch:PutMetricData",
                "ec2messages:GetEndpoint",
                "logs:DescribeLogStreams",
                "ds:CreateComputer",
                "s3:ListBucket",
                "ec2messages:GetMessages",
                "ssmmessages:OpenControlChannel",
                "ssm:PutConfigurePackageResult",
                "ssm:ListInstanceAssociations",
                "ssm:GetParameter",
                "ssm:UpdateAssociationStatus",
                "ssm:GetManifest",
                "logs:CreateLogStream",
                "ec2messages:DeleteMessage",
                "s3:AbortMultipartUpload",
                "ssm:UpdateInstanceInformation",
                "ec2messages:FailMessage",
                "ssmmessages:OpenDataChannel",
                "ssm:GetDocument",
                "ssm:PutComplianceItems",
                "ec2:DescribeInstanceStatus",
                "s3:ListBucketMultipartUploads",
                "ssm:DescribeAssociation",
                "logs:DescribeLogGroups",
                "ssm:GetDeployablePatchSnapshotForInstance",
                "ec2:DescribeTags",
                "ec2messages:AcknowledgeMessage",
                "ssmmessages:CreateControlChannel",
                "ssm:GetParameters",
                "logs:CreateLogGroup",
                "logs:PutLogEvents",
                "s3:ListMultipartUploadParts",
                "ssmmessages:CreateDataChannel",
                "s3:PutObject",
                "s3:GetObject",
                "ssm:PutInventory",
                "ds:DescribeDirectories",
                "ec2messages:SendReply",
                "ssm:ListAssociations",
                "ssm:UpdateInstanceAssociationStatus"
            ],
            "Resource": "*"
        }
    ]
}

response = iam_client.create_policy(
    PolicyName='EdwardsEC2RoleforSSMandCWAgent',
    PolicyDocument=json.dumps(managed_policy)

)
print(response)