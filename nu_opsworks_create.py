# pylint: disable=I0011
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0301
# pylint: disable=C0325

import time
import boto3

client_opsworks = boto3.client('opsworks')
client_ec2 = boto3.client('ec2')
client_iam = boto3.client('iam')

response_ec2 = client_ec2.describe_vpcs()
vpc_id = response_ec2['Vpcs'][0]['VpcId']

response_ec2 = client_ec2.describe_subnets(
    Filters=[
        {
            'Name': 'vpc-id',
            'Values': [
                vpc_id,
            ]
        },
    ]
)
subnet_id = response_ec2['Subnets'][0]['SubnetId']

response_ec2 = client_ec2.describe_security_groups(
    GroupNames=[
        'nu-default-sg',
    ]
)
security_group_id = response_ec2['SecurityGroups'][0]['GroupId']


response_iam = client_iam.get_role(
    RoleName='aws-opsworks-service-role'
)
service_role_arn = response_iam['Role']['Arn']

response_iam = client_iam.get_instance_profile(
    InstanceProfileName='aws-opsworks-ec2-role'
)
default_instance_profile_arn = response_iam['InstanceProfile']['Arn']

# Create OpsWorks Stack (Don't forget to change: VpcId, ServiceRoleArn, DefaultInstanceProfileArn, DefaultSubnetId and DefaultSshKeyName)
response_opsworks = client_opsworks.create_stack(
    Name='Nu Stack',
    Region='us-west-2',
    VpcId=vpc_id,
    ServiceRoleArn=service_role_arn,
    DefaultInstanceProfileArn=default_instance_profile_arn,
    DefaultOs='Amazon Linux 2016.09',
    DefaultSubnetId=subnet_id,
    ConfigurationManager={
        'Name': 'Chef',
        'Version': '12'
    },
    UseCustomCookbooks=True,
    UseOpsworksSecurityGroups=False,
    CustomCookbooksSource={
        'Type': 'git',
        'Url': 'https://github.com/fabiogoma/NuCookbooks.git',
        'Revision': 'master'
    },
    DefaultSshKeyName='fabiom',
    DefaultRootDeviceType='ebs'
)
stack_id = response_opsworks['StackId']
print('Stack ID: ' + stack_id)

# Create OpsWorks Layer (Don't forget to check the security id)
# Example: aws ec2 describe-security-groups --filters 'Name=group-name,Values=nu-default-sg'
response_opsworks = client_opsworks.create_layer(
    StackId=stack_id,
    Type='custom',
    Name='Nu Layer',
    Shortname='nu',
    CustomSecurityGroupIds=[
        security_group_id,
    ],
    AutoAssignPublicIps=True,
    CustomRecipes={
        'Deploy': [
            'nucookbook::docker_install',
            'nucookbook::docker_provisioner',
        ],
    }
)
layer_id = response_opsworks['LayerId']
print('Layer ID: ' + layer_id)

# Create OpsWorks Instance
response_opsworks = client_opsworks.create_instance(
    StackId=stack_id,
    LayerIds=[
        layer_id,
    ],
    InstanceType='t2.micro',
    Hostname='nuprovisioner',
    Architecture='x86_64',
    RootDeviceType='ebs'
)
instance_id = response_opsworks['InstanceId']
print('Instance ID: ' + instance_id)

# Start OpsWorks instance_id
response_opsworks = client_opsworks.start_instance(
    InstanceId=instance_id
)
print('Instance requested to start')

properties = open('opsworks-ids.properties', 'w')

properties.write('[IDs]\n')
properties.write('stack_id=' + stack_id + '\n')
properties.write('layer_id=' + layer_id + '\n')
properties.write('instance_id=' + instance_id + '\n')

while True:
    response_opsworks = client_opsworks.describe_instances(
        InstanceIds=[
            instance_id
        ]
    )
    status = response_opsworks['Instances'][0]['Status']

    if status == 'online':
        public_ip = response_opsworks['Instances'][0]['PublicIp']
        properties.write('public_ip=' + public_ip + '\n')
        properties.close()
        print('Public IP: ' + public_ip)
        print('Host ' + status)
        break
    else:
        time.sleep(10)
