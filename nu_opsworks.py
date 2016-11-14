# pylint: disable=I0011
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0301
# pylint: disable=C0325
import boto3

client = boto3.client('opsworks')

# Create OpsWorks Stack (Don't forget to change: VpcId, ServiceRoleArn, DefaultInstanceProfileArn, DefaultSubnetId and DefaultSshKeyName)
response = client.create_stack(
    Name='Nu Stack',
    Region='us-east-1',
    VpcId='vpc-ee20898a',
    ServiceRoleArn='arn:aws:iam::837404746161:role/aws-opsworks-ec2-role',
    DefaultInstanceProfileArn='arn:aws:iam::837404746161:instance-profile/aws-opsworks-ec2-role',
    DefaultOs='Amazon Linux 2016.09',
    DefaultSubnetId='subnet-13695f38',
    ConfigurationManager={
        'Name': 'Chef',
        'Version': '12'
    },
    UseCustomCookbooks=True,
    UseOpsworksSecurityGroups=False,
    CustomCookbooksSource={
        'Type': 'git',
        'Url': 'https://github.com/fabiogoma/NuRecipes.git',
        'Revision': 'master'
    },
    DefaultSshKeyName='string',
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
        'sg-3a47f047',
    ],
    AutoAssignPublicIps=True,
    CustomRecipes={
        'Deploy': [
            'aws_worker::docker_install',
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
