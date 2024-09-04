from aws_cdk import (
    CfnOutput,
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
)

from constructs import Construct

class AwsEc2TinyLinuxCdkSpecStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define the VPC
        vpc = ec2.Vpc(
            self, "ec2-tiny-linux-vpc",
        )

        # Define the Security Group
        security_group = ec2.SecurityGroup(
            self, "InstanceSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,
            description="Allow outbound traffic to vpc, no open ports: we will use SSM for access",
        )

        # Define the IAM Role for SSM
        role = iam.Role(
            self, "InstanceSSMRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"),
            ]
        )

        startup_commands = ec2.UserData.for_linux()
        startup_commands.add_commands(
            "sudo yum update -y",
            "sudo yum install -y zsh",
            "chsh -s /bin/zsh ssm-user"
        )

        # Define the EC2 instance
        instance = ec2.Instance(
            self, "MyInstance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
            security_group=security_group,
            role=role,
            user_data=startup_commands
        )

        # Output the Instance ID upon deployment
        CfnOutput(self, "InstanceId", value=instance.instance_id)