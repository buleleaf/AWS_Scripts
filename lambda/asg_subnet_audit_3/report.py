from .aws import AutoScaling
from .formatter import FormatReport
from .sender import SendReport


def stateless_ha(asg):
    return 'StatelessHa' in asg['Tags']


def not_enough_subnets(asg):
    return len(asg['VPCZoneIdentifier'].split(',')) < 2


def enough_subnets(asg):
    return len(asg['VPCZoneIdentifier'].split(',')) >= 2


def asg_name(asg):
    return asg['AutoScalingGroupName']


def asg_subnet_report(sender, region):
    autoscaling_groups = list(
        filter(stateless_ha, AutoScaling(region).describe_auto_scaling_groups())
    )

    report = {
        'Insufficient Subnets': map(
            asg_name, filter(not_enough_subnets, autoscaling_groups)
        ),
        'Sufficient Subnets': map(
            asg_name, filter(enough_subnets, autoscaling_groups)
        ),
    }
    return SendReport(FormatReport(report).format()).send(sender, region=region)
