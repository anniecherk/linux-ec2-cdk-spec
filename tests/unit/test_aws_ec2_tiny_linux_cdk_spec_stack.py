import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_ec2_tiny_linux_cdk_spec.aws_ec2_tiny_linux_cdk_spec_stack import AwsEc2TinyLinuxCdkSpecStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_ec2_tiny_linux_cdk_spec/aws_ec2_tiny_linux_cdk_spec_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsEc2TinyLinuxCdkSpecStack(app, "aws-ec2-tiny-linux-cdk-spec")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
