""" Load dependencies """

from sturdy_stacker_core_blueprints import version  # pylint: disable=W0403
from sturdy_stacker_core_blueprints.utils import standalone_output  # pylint: disable=W0403

from troposphere import Ref, Output, sns

from stacker.blueprints.base import Blueprint


class SnsTopic(Blueprint):
    """Blueprint for setting up SNS topic."""

    VARIABLES = {}

    def create_topic(self):
        """Sets up the SNS topic."""
        template = self.template

        pagerdutyalert = template.add_resource(
            sns.Topic(
                'Topic'
            )
        )

        template.add_output(
            Output(
                "%sARN" % pagerdutyalert.title,
                Description='SNS topic',
                Value=Ref(pagerdutyalert)
            )
        )

    def create_template(self):
        self.template.add_version('2010-09-09')
        self.template.add_description('Create SNS topic '
                                      "- {0}".format(version()))
        self.create_topic()


# Helper section to enable easy blueprint -> template generation
# (just run `python <thisfile>` to output the json)
if __name__ == "__main__":
    from stacker.context import Context

    standalone_output.json(SnsTopic('test',
                                    Context({"namespace": "test"}),
                                    None))
