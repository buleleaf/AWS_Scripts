import boto3
from botocore.exceptions import ClientError
import csv



# with open('instances.csv', 'r') as f:
#     csv_reader = csv.reader(f)
#     instances = list(csv_reader)


ec2client = boto3.client('ec2', region_name='us-west-2')
responses = ec2client.describe_instances(
    Filters=[
        {
            'Name': 'platform',
            'Values': [
                'windows',
            ]
        },
    ],
    InstanceIds=[
        "i-0c1a59bdcc4da596d",
        "i-0568301413cc21146",
        "i-0194f1e826f91426e",
        "i-037a98e67fc2fba01",
        "i-d159a38e",
        "i-04e27a1da6b73418a",
        "i-7285b5b5",
        "i-46696a5e",
        "i-09474ed253ad224da",
        "i-0b36d13e502272abe",
        "i-0f3d82eae836d41e5",
        "i-0a353a3c76f9f89db",
        "i-09e68fca17791facf",
        "i-bd5ba1e2",
        "i-327ebfa6",
        "i-098a8249307746fdb",
        "i-006a7a82041e8d642",
        "i-0356edd8e62c34f5b",
        "i-063cba386fcbb7b33",
        "i-0298e26173d93418f",
        "i-0631a9bf9a3502841",
        "i-050c1790",
        "i-7510296d",
        "i-0b378685552b7bb1e",
        "i-0d68c5ccd8e0a8d87",
        "i-056e0dc3583fae9e4",
        "i-08c4455fb37731bb3",
        "i-07f2281d9c7b8e3a9",
        "i-02bf2dbae921dbd03",
        "i-0df08e257603748d5",
        "i-933c358b",
        "i-29a36876",
        "i-0c7d1e1e0b9ff1f3f",
        "i-def52881",
        "i-0d4443ab6b8ca8cbe",
        "i-000ea53584bc2d58b",
        "i-0006c37d9f08f0c3a",
        "i-0ce36af1583479f61",
        "i-c2c8d1da",
        "i-ab3c35b3",
        "i-0d85d20c397567272",
        "i-68d8cb70",
        "i-0a99a7c63e58b7f97",
        "i-0739d234b6222f399",
        "i-0077b637959de672c",
        "i-0626219feb1a0800f",
        "i-0d6643a84367d34b1",
        "i-08a771e55a1e51860",
        "i-089259b10ff48073d",
        "i-05a2441c5ba4969e7",
        "i-bdf429e2",
        "i-73356a6b",
        "i-02877b75ad3cf4e47",
        "i-0e8b1d966c45c4df3",
        "i-008e5476baa12aae2",
        "i-030c3ace035cb39bc",
        "i-0f93b978f9c0572d6",
        "i-0daa9d560791bdc8c",
        "i-cadbd9d2",
        "i-0dd26d7e3133fc077",
        "i-00d65932893fde636",
        "i-04721fca4b6ca4c22",
        "i-0ffdb1541df22c496",
        "i-0303ffddb485d8a33",
        "i-017e7b472e9713d74",
        "i-fed2dce6",
        "i-013ba0cd462d0af0c",
        "i-509b8048",
        "i-048e90b6b5aff9914",
        "i-0d7a49b80890a272e",
        "i-05fde3740c4e52d72",
        "i-0ed24b04284a77c95",
        "i-0b13ec28e89ba1fdc",
        "i-f606dbee",
        "i-0eaa08d8815331cd8",
        "i-061213f35072b88d0",
        "i-007c2377a52526d68",
        "i-bc1ce228",
        "i-0570011dd71dce742",
        "i-46f8949e",
        "i-0ddfc0535e6a7c2d3",
        "i-0896e97821ded8dba",
        "i-1aad668e",
        "i-98f41283",
        "i-078ad6e8d5507b4ca",
        "i-eb55b0f0",
        "i-0f95165fe9f7e70a4",
        "i-69f41272",
        "i-fb58a2a4",
        "i-e9d9e6f1",
        "i-448331eb",
        "i-e5f7f7fd",
        "i-9eea39c1",
        "i-05add562cb07b1629",
        "i-6429d0cb",
        "i-f455b0ef",
        "i-001100501e832b907",
        "i-0ff09da60ea8f77d0",
        "i-064b8d84791d9b34f",
        "i-01e42495",
        "i-09f6ce9f774e9783e",
        "i-828d4a2d",
        "i-039a4ae3101d8ad2a",
        "i-0ef8b8babc3813aef",
        "i-0fa6e1d7c1d852c0c",
        "i-b730ab22",
        "i-0226243dd80e85374",
        "i-0fb90f53ba1d30d2b",
        "i-ad969ab5",
        "i-0ae768fe813c46131",
        "i-041f2dc5a8f247140",
        "i-d96d53c1",
        "i-05cceebbdb856fd8c",
        "i-0f1edf12f65566bbe",
        "i-0fd7bd385d9dd0448",
        "i-02eb397ec1da7abe1",
        "i-7284926a",
        "i-04cc954d4f7804c7d",
        "i-07ecec10e2f76b95b",
        "i-0bbbf727ca7e5781d",
        "i-02e0dd7f91c8386c0",
        "i-05011815b7fecda81",
        "i-0fb84d9d912dee37e",
        "i-38babb20",
        "i-0fdfe6355f3c29760",
        "i-4f29d010",
        "i-0dc41210e32a9668e",
        "i-06f4994cddcb152c4",
        "i-b5d7cead",
        "i-02a2a0b1b4d755e88",
        "i-0adaf3e97cf43d2b5",
        "i-0f8af50589e6b0387",
        "i-0691feb856a2b6096",
        "i-00adbb9d0de22beec",
        "i-075f2d8832852044c",
        "i-bc5ba1e3",
        "i-0db2ea94f1fd9e899",
        "i-040efbff1a773be64",
        "i-1583040d",
        "i-097cc769325358a6c",
        "i-0ae0dd24e1ed0018b",
        "i-0a6c85896a2e02862",
        "i-01f6f619",
        "i-09f85229e99fa1243",
        "i-0afc00592cfe9bacf",
        "i-cc44d758",
        "i-cb5de4d3",
        "i-3b3f3623",
        "i-0df750d1d4c2c5be5",
        "i-00855aad2d60b90a9",
        "i-022976b45b04ae359",
        "i-02575e5cdef6122c8",
        "i-0a38fb77f7ea628ba",
        "i-04b1e9d9ec359e888",
        "i-0b0f150ecec1b0fda",
        "i-323f362a",
        "i-a22ca4ba",
        "i-04d21d7b8b627a1f2",
        "i-061a5a31fbdd36366",
        "i-c95d8d96",
        "i-056d2000b7a09d539",
        "i-0c4b9b5409ed177a1",
        "i-01444ab3e9c3698fa",
        "i-0014c68e9a090636b",
        "i-04921d33e4cc7c5ec",
        "i-09f3fb004e1cb1a19",
        "i-0d80ba3247b418be3",
        "i-0c16572db5e4ad0b1",
        "i-47732c5f",
        "i-d031b7c8",
        "i-0b5bcf3d7a147035b",
        "i-094385b3eb8bc3f72",
        "i-09fa325ea8596e65b",
        "i-097b1aac1ad655a26",
        "i-08333bbf229da809d",
        "i-a394530c",
        "i-0946e698d7e97077a",
        "i-040235efbf830045f",
        "i-07561ef488a6f44ce",
        "i-0b7f47bf3324623cb",
        "i-96bdd38e",
        "i-71d5ea69",
        "i-07589ade9a5d3de59",
        "i-091b007a4321557d2",
        "i-3ad72695",
        "i-84f7119f",
        "i-7529b4e1",
        "i-04b25c6a878f016f1",
        "i-08a42b2badf148512",
        "i-08a45bcff5908bbd1",
        "i-3ec23d61",
        "i-b6454bae",
        "i-0a52465dc4f93e894"
    ]
)
instance_result = set()
for reservations in responses['Reservations']:
    for instance in reservations['Instances']:
        if (instance['InstanceId']):
            instance_result.add(instance['InstanceId'])
print(len(instance_result))
print(instance_result)


# try:
#     response = ec2.delete_security_group(GroupId='{}'.format(security_groups))
#     print(response)
#     .format(str(security_groups)[-1:1]))
#     print('Deleting Security Group: {}'.format(str(security_groups)[-1:1]))
#     print('Security Group Deleted')
# except ClientError as e:
#     print(e)    
#     for sg in security_groups:
#         print(sg)
#         response = ec2.delete_security_group(GroupId='sg-0683d3523a393f9e1')
        
#         # try:
#             for gid in sg_groupid:
#                 response = ec2.delete_security_group(GroupId='{}'.format(gid))
#                 print('Security Group Deleted')
#         except ClientError as e:
#             print(e)
