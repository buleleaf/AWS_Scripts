import logging
import os

from .report import asg_subnet_report
from .sender import sender_sns, sender_stdout

logging.getLogger('boto3').setLevel(logging.ERROR)
logging.getLogger('botocore').setLevel(logging.ERROR)
LOGFMT = ("[%(levelname)s] %(asctime)s.%(msecs)dZ {aws_request_id} "
          "%(thread)d %(message)s")
DATEFMT = "%Y-%m-%dT%H:%M:%S"


def configure_logging(log_context, log_level=logging.INFO, logfmt=LOGFMT,
                      datefmt=DATEFMT):
    """Configure logging."""
    logfmt = logfmt.format(**log_context)
    while logging.root.handlers:
        logging.root.removeHandler(logging.root.handlers[-1])
    logging.basicConfig(level=log_level, datefmt=datefmt, format=logfmt)
    logging.getLogger('boto3').setLevel(logging.ERROR)
    logging.getLogger('botocore').setLevel(logging.ERROR)
    return logging.getLogger()


def lambda_handler(event, context):
    """Lambda Entrypoint."""
    configure_logging({'aws_request_id': context.aws_request_id},
                      logfmt=LOGFMT, datefmt=DATEFMT, log_level=logging.INFO)
    return main(event, context, sender_sns)


def main(event, context, sender=sender_stdout):
    logging.info(event)
    asg_subnet_report(sender, os.environ['AWS_DEFAULT_REGION'])


if __name__ == '__main__':
    configure_logging({'aws_request_id': "local"},
                      logfmt=LOGFMT, datefmt=DATEFMT, log_level=logging.INFO)
    print(main(None, None))
