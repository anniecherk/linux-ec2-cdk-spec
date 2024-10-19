# first time set up:
#
# template was gen'd w:
# cdk init --language=python
#
# source .venv/bin/activate
# pip install -r requirements.txt
# cdk bootstrap
# 
# install session manager plugin on macos
# https://docs.aws.amazon.com/systems-manager/latest/userguide/install-plugin-macos-overview.html


# it's python don't forget
# source .venv/bin/activate

# run whenever you want to change the infra
deploy:
    #!/bin/zsh
    # source .venv/bin/activate
    export AWS_ACCOUNT_FOR_EC2_TINY_LINUX_CDK_SPEC=$(aws sts get-caller-identity --query "Account" --output text)
    export AWS_REGION_FOR_EC2_TINY_LINUX_CDK_SPEC="us-west-2"
    cdk deploy

connect:
    #!/bin/zsh
    # source .venv/bin/activate
    export AWS_ACCOUNT_FOR_EC2_TINY_LINUX_CDK_SPEC=$(aws sts get-caller-identity --query "Account" --output text)
    export AWS_REGION_FOR_EC2_TINY_LINUX_CDK_SPEC="us-west-2"
    instanceID=$(aws cloudformation describe-stacks --stack-name AwsEc2TinyLinuxCdkSpecStack --query "Stacks[0].Outputs[?OutputKey=='InstanceId'].OutputValue" --output text)
    aws ssm start-session --target $instanceID --document-name AWS-StartInteractiveCommand --parameters command="sudo -u pumpernickle /bin/zsh -l"


# destroys the instance & vpc & iam role & everything else
# if u don't do this u'll keep getting billed for all the resources being up
destroy:
    #!/bin/zsh
    # source .venv/bin/activate
    export AWS_ACCOUNT_FOR_EC2_TINY_LINUX_CDK_SPEC=$(aws sts get-caller-identity --query "Account" --output text)
    export AWS_REGION_FOR_EC2_TINY_LINUX_CDK_SPEC="us-west-2"
    cdk destroy

