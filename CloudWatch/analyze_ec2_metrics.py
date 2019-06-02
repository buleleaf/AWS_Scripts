"""Analyze output of metrics script."""
import datetime
import argparse
import logging
import json
import statistics

from statistics import mean, median, variance
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()
log.setLevel(logging.INFO)

parser = argparse.ArgumentParser(description='Get cloudwatch data from alarm')
parser.add_argument('tag', help='Tag to check instances by')
parser.add_argument('tag_value', help='Tag Value to check instances by')
args = parser.parse_args()

js_report = open('metric_report-{}-{}.json'.format(args.tag, args.tag_value), 'r')  # noqa: E501
report = json.loads(js_report.read())
js_report.close
analysis = {}
analysis_output = []


def save_and_log(line):
    """Log and prepare to save to file."""
    log.info(line)
    analysis_output.append(line)


report_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")   # noqa: E501
for region in report:
    save_and_log("Analyzing {}".format(region))
    for instance in report[region]:
        analysis[instance] = {}
        save_and_log('')
        save_and_log("  Analyzing {}".format(report[region][instance]['Metadata']['Name']))  # noqa: E501
        for metric in report[region][instance]:
            if metric != 'Metadata':
                datapoints = [a['Average'] for a in report[region][instance][metric]['Datapoints']]  # noqa: E501

                save_and_log("    Metric: {}".format(metric))
                save_and_log("    -------------------------")
                save_and_log("    Mean: {}".format(mean(datapoints)))
                save_and_log("    Median: {}".format(median(datapoints)))
                save_and_log("    Variance: {}".format(variance(datapoints)))
                save_and_log("    Minimum: {}".format(min(datapoints)))
                save_and_log("    Maximum: {}".format(max(datapoints)))
                save_and_log('')
                if report[region][instance][metric].get('Threshold'):
                    save_and_log('    Alarms:')
                    if report[region][instance][metric]['Operator'] == 'GreaterThanOrEqualToThreshold':  # noqa: E501
                        operator = "Greater Than"
                        execeeding_points = [a['Average'] for a in report[region][instance][metric]['Datapoints'] if a['Average'] >= report[region][instance][metric]['Threshold']]  # noqa: E501
                    elif report[region][instance][metric]['Operator'] == 'GreaterThanThreshold':  # noqa: E501
                        operator = "Greater Than"
                        execeeding_points = [a['Average'] for a in report[region][instance][metric]['Datapoints'] if a['Average'] > report[region][instance][metric]['Threshold']]  # noqa: E501
                    elif report[region][instance][metric]['Operator'] == 'LessThanOrEqualToThreshold':  # noqa: E501
                        operator = "Less Than"
                        execeeding_points = [a['Average'] for a in report[region][instance][metric]['Datapoints'] if a['Average'] <= report[region][instance][metric]['Threshold']]  # noqa: E501
                    elif report[region][instance][metric]['Operator'] == 'LessThanThreshold':  # noqa: E501
                        operator = "Less Than"
                        execeeding_points = [a['Average'] for a in report[region][instance][metric]['Datapoints'] if a['Average'] < report[region][instance][metric]['Threshold']]  # noqa: E501
                    save_and_log("    Points Exceeding Threshold: {}".format(len(execeeding_points)))  # noqa: E501
                    save_and_log("    Percentage {0} Threshold: {1:.3%}".format(operator, float(len(execeeding_points)/float(len(datapoints)))))  # noqa: E501

                if report[region][instance][metric].get('AlarmAnalysis'):
                    save_and_log("    OK->ALARM->OK Transitions: {}".format(len(report[region][instance][metric]['AlarmAnalysis'])))  # noqa: E501
                    alarm_durations = [a['AlarmDurationMinutes'] for a in report[region][instance][metric]['AlarmAnalysis']]  # noqa: E501
                    save_and_log("    Average Alarm Duration: {} minutes".format(int(mean(alarm_durations))))  # noqa: E501
                    save_and_log("    Min Alarm Duration: {}".format(min(alarm_durations)))  # noqa: E501
                    save_and_log("    Max Alarm Duration: {}".format(max(alarm_durations)))  # noqa: E501
                    save_and_log('')
                else:
                    save_and_log('    No history of alarms')
                    save_and_log('')

txt_report = open('metric_analysis-{}-{}-{}.txt'.format(args.tag, args.tag_value, report_time), 'w')  # noqa: E501
log.info('Saved output: metric_analysis-{}-{}-{}.txt'.format(args.tag, args.tag_value, report_time))  # noqa: E501
for line in analysis_output:
        txt_report.write("%s\n" % line)
txt_report.close
