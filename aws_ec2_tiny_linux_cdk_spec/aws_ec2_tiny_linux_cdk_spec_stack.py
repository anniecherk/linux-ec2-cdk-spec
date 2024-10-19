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
            "sudo apt-get update -y",
            "sudo apt-get install -y zsh curl git",
            "sudo chsh -s /usr/bin/zsh ubuntu",
            "su - ubuntu -c 'sh -c \"$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)\" \"\" --unattended'",
            "echo 'export SHELL=/usr/bin/zsh' >> /home/ubuntu/.bashrc",
            "echo 'exec /usr/bin/zsh' >> /home/ubuntu/.bashrc",
            "sudo apt-get install -y build-essential",
            "echo '#!/bin/bash' | sudo tee /usr/local/bin/session-manager-zsh.sh > /dev/null",
            "echo 'exec /usr/bin/zsh -l' | sudo tee -a /usr/local/bin/session-manager-zsh.sh > /dev/null",
            "sudo chmod +x /usr/local/bin/session-manager-zsh.sh",
            "echo 'Session Manager script created at /usr/local/bin/session-manager-zsh.sh'"
        )

        # Define the EC2 instance
        instance = ec2.Instance(
            self, "MyInstance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.lookup(
                name="ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*",
                owners=["099720109477"]  # Canonical's AWS account ID
            ),
            vpc=vpc,
            security_group=security_group,
            role=role,
            user_data=startup_commands
        )

        # Output the Instance ID upon deployment
        CfnOutput(self, "InstanceId", value=instance.instance_id)
