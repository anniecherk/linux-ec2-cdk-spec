#!/usr/bin/env python3
import os

from aws_cdk import App, Environment
from aws_ec2_tiny_linux_cdk_spec.aws_ec2_tiny_linux_cdk_spec_stack import AwsEc2TinyLinuxCdkSpecStack

app = App()

# Get AWS account ID and region from environment variables
account_id = os.environ.get("AWS_ACCOUNT_FOR_EC2_TINY_LINUX_CDK_SPEC")
region = os.environ.get("AWS_REGION_FOR_EC2_TINY_LINUX_CDK_SPEC")

# Check if the environment variables are set
if not account_id or not region:
    raise ValueError("Please set AWS_ACCOUNT_FOR_EC2_TINY_LINUX_CDK_SPEC and AWS_REGION_FOR_EC2_TINY_LINUX_CDK_SPEC environment variables")

AwsEc2TinyLinuxCdkSpecStack(app, "AwsEc2TinyLinuxCdkSpecStack",
    env=Environment(account=account_id, region=region)
)

app.synth()
