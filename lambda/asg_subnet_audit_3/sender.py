import os

from .aws import SNS


def sender_stdout(report, **kwargs):
    print(report)
    return True


def sender_sns(report, **kwargs):
    subject = 'ASG Subnet Audit Report'
    return SNS(kwargs['region']).publish(
        TopicArn=os.environ['SNS_TOPIC'],
        Message=report,
        Subject=subject
    )


class SendReport:
    def __init__(self, report):
        self._report = report

    def send(self, sender=sender_stdout, **kwargs):
        return sender(self._report, **kwargs)
