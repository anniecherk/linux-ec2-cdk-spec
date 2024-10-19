from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    CfnOutput,
)
from constructs import Construct

# yup that's me, pumpernickle
USER = "pumpernickle"

class AwsEc2TinyLinuxCdkSpecStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define the VPC
        vpc = ec2.Vpc(self, "ec2-tiny-linux-vpc")

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

        # Organize startup commands
        update_system = [
            "sudo apt-get update -y",
        ]

        install_tools = [
            "sudo apt-get install -y zsh curl git build-essential",
        ]

        # nb! USER is being escaped in the python string, not in the shell command!
        create_user = [
            f"sudo useradd -m -s /usr/bin/zsh {USER}",
            f"sudo usermod -aG sudo {USER}",
            f"echo '{USER} ALL=(ALL) NOPASSWD:ALL' | sudo tee -a /etc/sudoers",
        ]

        configure_zsh = [
            f"su - {USER} -c 'sh -c \"$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)\" \"\" --unattended'",
            f"echo 'export SHELL=/usr/bin/zsh' | sudo tee -a /home/{USER}/.bashrc",
            f"echo 'exec /usr/bin/zsh' | sudo tee -a /home/{USER}/.bashrc",
            # without these the session manager puts us someplace weird
            f"echo 'cd /home/{USER}' | sudo tee -a /home/{USER}/.zshrc",
            f"echo 'cd /home/{USER}' | sudo tee -a /home/{USER}/.bashrc",
            f"echo 'cd /home/{USER}' | sudo tee -a /etc/profile",
        ]

        set_permissions = [
            f"sudo chown -R {USER}:{USER} /home/{USER}",
            f"sudo chmod 755 /home/{USER}",
            f"sudo chmod -R u+w /home/{USER}",
        ]

        configure_from_dotfiles_repo = [
            "git clone https://github.com/anniecherk/dotfiles.git /home/{USER}/dotfiles",
            "cd /home/{USER}/dotfiles/ubuntu",
            "sudo ./install.sh",
            "./ubuntu_install.sh",
        ]

        # the time has come: 
        # we have all the ingredients, let us brew the potion
        startup_commands = ec2.UserData.for_linux()
        startup_commands.add_commands(*(
            update_system +
            install_tools +
            create_user +
            configure_zsh +
            set_permissions +
            configure_from_dotfiles_repo
        ))
        # for debugging you can see the results of the startup commands
        # via `sudo cat /var/log/cloud-init-output.log` on the instance

        # Define the EC2 instance
        instance = ec2.Instance(
            self, "MyEC2Instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.lookup(
                name="ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*",
                owners=["099720109477"]  # Canonical's AWS account ID
            ),
            vpc=vpc,
            security_group=security_group,
            role=role,
            user_data=startup_commands
        )

        # output the instance id: we need this to be able to easily connect
        CfnOutput(self, "InstanceId", value=instance.instance_id)
