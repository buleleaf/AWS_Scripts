import json
import csv
import boto3



iam = boto3.client("iam")
marker = None

field = ['UserName', 'Effect', 'Action', 'NotAction', 'Resource', 'Condition', 'Permission Source']
row = []

paginator = iam.get_paginator('list_users')
response_iterator = paginator.paginate( PaginationConfig={'PageSize': 1000,'StartingToken': marker})
for page in response_iterator:
    u = page['Users']
    for user in u:
        # print(user['UserName'])
        print("Fetching IAM permissions for "+user['UserName'])
        inline_user_policies=iam.list_user_policies(UserName=user['UserName'])
        managed_policies= iam.list_attached_user_policies(UserName=user['UserName'])
        groups=iam.list_groups_for_user(UserName=user['UserName'])
        if len(groups['Groups']) > 0:
            for group in groups['Groups']:
                group_inline_policies = iam.list_group_policies(GroupName=group['GroupName'])
                group_managed_policies = iam.list_attached_group_policies(GroupName=group['GroupName'])
                if len(group_inline_policies['PolicyNames']) > 0:
                    for policy in group_inline_policies['PolicyNames']:
                        group_inline_policiy_detail= iam.get_group_policy(GroupName=group['GroupName'],PolicyName=policy)
                        data=json.dumps(group_inline_policiy_detail['PolicyDocument'])
                        permissions=json.loads(data)['Statement']
                        for permission in permissions:
                            # print(permission)
                            row.append(permission)

                if len(group_managed_policies['AttachedPolicies']) > 0:
                    for policy in group_managed_policies['AttachedPolicies']:
                        group_managed_policiy_detail= iam.get_policy(PolicyArn=policy['PolicyArn'])
                        policy_version = iam.get_policy_version(PolicyArn = policy['PolicyArn'], VersionId = group_managed_policiy_detail['Policy']['DefaultVersionId'])
                        data=json.dumps(policy_version['PolicyVersion']['Document'])
                        permissions=json.loads(data)['Statement']
                        for permission in permissions:
                            # print(permission)
                            row.append(permission)

        if len(inline_user_policies['PolicyNames']) > 0:
            for policy in inline_user_policies['PolicyNames']:
                user_inline_policiy_detail= iam.get_user_policy(UserName=user['UserName'],PolicyName=policy)
                data=json.dumps(user_inline_policiy_detail['PolicyDocument'])
                permissions=json.loads(data)['Statement']
                for permission in permissions:
                    # print(permission)
                    row.append(permission)

        if len(managed_policies['AttachedPolicies']) >0:
            for policy in managed_policies['AttachedPolicies']:
                user_managed_policiy_detail= iam.get_policy(PolicyArn=policy['PolicyArn'])
                policy_version = iam.get_policy_version(PolicyArn = policy['PolicyArn'], VersionId = user_managed_policiy_detail['Policy']['DefaultVersionId'])
                data=json.dumps(policy_version['PolicyVersion']['Document'])
                permissions=json.loads(data)['Statement']
                for permission in permissions:
                    # print(permission)
                    row.append(permission)

print(row)

filename = 'iam-user-audit.csv'

with open(filename, 'w', encoding='utf-8') as outfile:
    fieldnames = field
    rows = row
    writer = csv.DictWriter(outfile, fieldnames=list(fieldnames, rows))
    # writerrow = csv.DictWriter(outfile, fieldnames=list(rows))
    writer.writeheader()