import boto3

region = 'us-west-2'

def account_alias():
    iam_client = boto3.client('iam')
    response = iam_client.list_account_aliases()["AccountAliases"][0]
    return(response)


def main():

    alias = account_alias()

    print(alias)

if __name__ == '__main__':
    main()
