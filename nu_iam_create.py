# pylint: disable=I0011
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0301
# pylint: disable=C0325

import boto3
import botocore

client = boto3.client('iam')

# Create default opsworks role for EC2 (aws-opsworks-service-role)
try:
    response = client.create_role(
        Path='/',
        RoleName='aws-opsworks-ec2-role',
        AssumeRolePolicyDocument='{ "Version": "2008-10-17", "Statement": [ { "Effect": "Allow", "Principal": { "Service": "ec2.amazonaws.com" }, "Action": "sts:AssumeRole" } ] }'
    )
    print(response['Role']['RoleName'])
    print(response['Role']['RoleId'])
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'EntityAlreadyExists':
        print('Role aws-opsworks-ec2-role already exists')

# Create default role for AWS opsworks (aws-opsworks-service-role)
try:
    response = client.create_role(
        Path='/',
        RoleName='aws-opsworks-service-role',
        AssumeRolePolicyDocument='{ "Version": "2008-10-17", "Statement": [ { "Effect": "Allow", "Principal": { "Service": "opsworks.amazonaws.com" }, "Action": "sts:AssumeRole" } ] }'
    )
    print(response['Role']['RoleName'])
    print(response['Role']['RoleId'])
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'EntityAlreadyExists':
        print('Role aws-opsworks-service-role already exists')

# Create instance profile
try:
    response = client.create_instance_profile(
        InstanceProfileName='aws-opsworks-ec2-role',
        Path='/'
    )
    print(response['InstanceProfile']['InstanceProfileName'])
    print(response['InstanceProfile']['InstanceProfileId'])
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'EntityAlreadyExists':
        print('Instance profile aws-opsworks-service-role already exists')

# Add role to instance profile
try:
    response = client.add_role_to_instance_profile(
        InstanceProfileName='aws-opsworks-ec2-role',
        RoleName='aws-opsworks-ec2-role'
    )
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'LimitExceeded':
        print('Only 1 instance sessions per Instance Profile is allowed')


# Put a policy to the role
response = client.put_role_policy(
    RoleName='aws-opsworks-service-role',
    PolicyName='aws-opsworks-service-policy',
    PolicyDocument='{ "Version": "2012-10-17", "Statement":[{"Action":["ec2:*","iam:PassRole","cloudwatch:GetMetricStatistics","cloudwatch:DescribeAlarms","ecs:*","elasticloadbalancing:*","rds:*"],"Effect":"Allow","Resource":["*"]}]}'
)
