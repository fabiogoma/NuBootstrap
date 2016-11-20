# pylint: disable=I0011
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0301
# pylint: disable=C0325

import time
import boto3

client = boto3.client('opsworks')

# Create OpsWorks Stack (Don't forget to change: VpcId, ServiceRoleArn, DefaultInstanceProfileArn, DefaultSubnetId and DefaultSshKeyName)
response = client.create_stack(
    Name='Nu Stack',
    Region='us-west-2',
    VpcId='vpc-7a659f1d',
    ServiceRoleArn='arn:aws:iam::678982507510:role/aws-opsworks-service-role',
    DefaultInstanceProfileArn='arn:aws:iam::678982507510:instance-profile/aws-opsworks-ec2-role',
    DefaultOs='Amazon Linux 2016.09',
    DefaultSubnetId='subnet-1e8eb768',
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
stack_id = response['StackId']
print('Stack ID: ' + stack_id)

# Create OpsWorks Layer (Don't forget to check the security id)
# Example: aws ec2 describe-security-groups --filters 'Name=group-name,Values=nu-default-sg'
response = client.create_layer(
    StackId=stack_id,
    Type='custom',
    Name='Nu Layer',
    Shortname='nu',
    CustomSecurityGroupIds=[
        'sg-a5b3e7dc',
    ],
    AutoAssignPublicIps=True,
    CustomRecipes={
        'Deploy': [
            'nucookbook::docker_install',
            'nucookbook::docker_provisioner',
        ],
    }
)
layer_id = response['LayerId']
print('Layer ID: ' + layer_id)

# Create OpsWorks Instance
response = client.create_instance(
    StackId=stack_id,
    LayerIds=[
        layer_id,
    ],
    InstanceType='t2.micro',
    Hostname='nuprovisioner',
    Architecture='x86_64',
    RootDeviceType='ebs'
)
instance_id = response['InstanceId']
print('Instance ID: ' + instance_id)

# Start OpsWorks instance_id
response = client.start_instance(
    InstanceId=instance_id
)
print('Instance requested to start')

properties = open('opsworks-ids.properties', 'w')

properties.write('[IDs]\n')
properties.write('stack_id=' + stack_id + '\n')
properties.write('layer_id=' + layer_id + '\n')
properties.write('instance_id=' + instance_id + '\n')

while True:
    response = client.describe_instances(
        InstanceIds=[
            instance_id
        ]
    )
    status = response['Instances'][0]['Status']

    if status == 'online':
        public_ip = response['Instances'][0]['PublicIp']
        properties.write('public_ip=' + public_ip + '\n')
        properties.close()
        print('Public IP: ' + public_ip)
        print('Host ' + status)
        break
    else:
        time.sleep(10)
