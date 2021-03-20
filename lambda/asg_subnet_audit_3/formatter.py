def formatter_text(report):
    txt_report = 'ASG Subnet Audit for Snowblower\n\n'
    for key in report:
        txt_report += '{}\n'.format(key)
        txt_report += '\n'.join(report[key])
        txt_report += '\n\n'

    return txt_report


class FormatReport:
    def __init__(self, report):
        self._report = report

    def format(self, formatter=formatter_text):
        return formatter(self._report)
