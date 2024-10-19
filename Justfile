
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
    # source .venv/bin/activate
    cdk deploy

connect: 
    #!/bin/zsh
    instanceID=$(aws cloudformation describe-stacks --stack-name AwsEc2TinyLinuxCdkSpecStack --query "Stacks[0].Outputs[?OutputKey=='InstanceId'].OutputValue" --output text)
    aws ssm start-session --target $instanceID --document-name AWS-StartInteractiveCommand --parameters command="/usr/local/bin/session-manager-zsh.sh"


# destroys the instance & vpc & iam role & everything else
# if u don't do this u'll keep getting billed for all the resources being up
destroy:
    # source .venv/bin/activate
    cdk destroy