import boto3


class AWSLambda:
    def __init__(self, region):
        self._client = boto3.client('lambda', region)

    def list_functions(self, **kwargs):
        for page in self._client.get_paginator(
            'list_functions'
        ).paginate(**kwargs):
            for function in page['Functions']:
                yield function
