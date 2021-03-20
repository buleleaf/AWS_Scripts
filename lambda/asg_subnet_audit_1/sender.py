def sender_stdout(report):
    print(report)
    return True


def sender_sns(report):
    import os
    import boto3
    subject = 'SQL Backups Audit Report'
    boto3.client('sns').publish(
        TopicArn=os.environ['SNS_TOPIC'],
        Message=report,
        Subject=subject
    )


class SendReport:
    def __init__(self, sender=sender_stdout):
        self._sender = sender

    def send(self, report):
        return self._sender(report)


