#!/usr/bin/env python3
"""Audit IAM Users for Permissions."""
import csv
import functools
import logging
import os

import boto3

FORMAT = '%(asctime)-15s %(levelname)s %(module)s.%(funcName)s %(message)s'
DATEFMT = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATEFMT)


@functools.lru_cache
def boto3_client(resource, region=os.environ['AWS_DEFAULT_REGION']):
    """Create Boto3 Client from resource and region."""
    return boto3.client(resource, region)


def list_users(**kwargs):
    """List IAM Users."""
    client = boto3_client("iam")
    paginator = client.get_paginator('list_users')
    for page in paginator.paginate(**kwargs):
        for user in page['Users']:
            yield user


def get_group_policy(group, policy):
    """IAM Boto3 Group Policy Document from group name and policy."""
    return boto3_client('iam').get_group_policy(
        GroupName=group, PolicyName=policy
    )['PolicyDocument']


def inline_policy_on_group(group, policy):
    """Group Policy Permissions."""
    for permission in get_group_policy(group, policy)['Statement']:
        yield permission


def list_group_policies(name):
    """List IAM Boto3 Group Policy Names."""
    return boto3_client('iam').list_group_policies(GroupName=name)[
        'PolicyNames'
    ]


def list_groups_for_user(name):
    """Groups a IAM User is a member of."""
    return boto3_client('iam').list_groups_for_user(UserName=name)['Groups']


def list_attached_group_policies(name):
    """List IAM Boto3 Group Managed Policy Names."""
    return boto3_client('iam').list_attached_group_policies(GroupName=name)['AttachedPolicies']


def group_inline_policies_permissions(group):
    """Permission on inline policies from group."""
    for policy in list_group_policies(group['GroupName']):
        for permission in inline_policy_on_group(group['GroupName'], policy):
            yield permission


def group_permissions_by_username(name):
    """Permissions from Group from Inline/Managed Policies."""
    for group in list_groups_for_user(name):
        for permission in group_inline_policies_permissions(group):
            yield permission

        for attached_policy in list_attached_group_policies(group['GroupName']):
            statements = statements_default_policy_doc_from_arn(attached_policy['PolicyArn'])
            for permission in statements:
                yield permission


def list_user_policies(name):
    """User Policy Names."""
    return boto3_client('iam').list_user_policies(UserName=name)['PolicyNames']


def get_user_policy(name, policy):
    """User Policy Document."""
    return boto3_client('iam').get_user_policy(
        UserName=name, PolicyName=policy
    )['PolicyDocument']


def inline_user_policies_by_name(name):
    """Permissions from inline User Policies."""
    for policy in list_user_policies(name):
        for permission in get_user_policy(name, policy)['Statement']:
            yield permission


def list_attached_user_policies(username):
    """Managed Policies attached directly to IAM User."""
    return boto3_client('iam').list_attached_user_policies(UserName=username)[
        'AttachedPolicies'
    ]


def default_policy_doc_from_arn(arn):
    """Default IAM Policy Document from ARN."""
    return boto3_client('iam').get_policy_version(
        PolicyArn=arn,
        VersionId=boto3_client('iam').get_policy(PolicyArn=arn)['Policy'][
            'DefaultVersionId'
        ],
    )['PolicyVersion']


def statements_default_policy_doc_from_arn(arn):
    """Permissions from Default IAM Policy Document from ARN."""
    return default_policy_doc_from_arn(arn)['Document']['Statement']


def managed_user_policies_by_name(username):
    """IAM User Manager Policies Permissions."""
    for policy in list_attached_user_policies(username):
        statements = statements_default_policy_doc_from_arn(policy['PolicyArn'])
        for permission in statements:
            yield permission


def user_policies_by_name(username):
    """Permissions for User from Inline/Managed Policies on User."""
    for permission in inline_user_policies_by_name(username):
        yield permission
    for permission in managed_user_policies_by_name(username):
        yield permission


def format_permission(permission, user):
    permission['UserName'] = user['UserName']
    return permission


def breakout_permissions(permission):
    if isinstance(permission['Action'], str):
        yield permission
    elif isinstance(permission['Action'], list):
        for action in permission['Action']:
            new = permission.copy()
            new['Action'] = action
            yield new


def process_user(user):
    """Process User."""
    logging.info("Fetching IAM permissions for %s", user['UserName'])
    for permission in all_user_policy_permissions(user):
        for p in breakout_permissions(permission):
            yield format_permission(p, user)


def all_user_policy_permissions(user):
    """IAM User retrieving permissions from associated policies."""
    for permission in group_permissions_by_username(user['UserName']):
        yield permission

    for permission in user_policies_by_name(user['UserName']):
        yield permission


def fieldnames(rows):
    """Find all unique keys in rows of dicts."""
    fields = set()
    for row in rows:
        for key in row.keys():
            fields.add(key)
    return list(fields)


def write_csv_file(rows, filename='iam-user-audit.csv'):
    """Write CSV to specified file."""
    with open(filename, 'w', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames(rows))
        writer.writeheader()
        writer.writerows(rows)


def main():
    write_csv_file(
        [
            permission
            for user in list_users(PaginationConfig={'PageSize': 1000})
            for permission in process_user(user)
        ]
    )


if __name__ == '__main__':
    main()
