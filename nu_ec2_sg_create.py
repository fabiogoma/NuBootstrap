# pylint: disable=I0011
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0301
# pylint: disable=C0325

import boto3
import botocore

client = boto3.client('ec2')

group_id = ''

try:
    # Create EC2 Security Group (Don't forget to change VpcId')
    response = client.create_security_group(
        GroupName='nu-default-sg',
        Description='Nu Security Group',
        VpcId='vpc-7a659f1d'
    )
    group_id = response['GroupId']
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'InvalidGroup.Duplicate':
        print('Group already exists')
        response = client.describe_security_groups(
            GroupNames=[
                'nu-default-sg',
            ]
        )
        group_id = response['SecurityGroups'][0]['GroupId']

properties = open('ec2-security.properties', 'w')
properties.write('[IDs]\n')
properties.write('security_group_id=' + group_id + '\n')
properties.close()

try:
    # Allowing traffic on port 22
    response = client.authorize_security_group_ingress(
        GroupId=group_id,
        IpProtocol='tcp',
        FromPort=22,
        ToPort=22,
        CidrIp='0.0.0.0/0',
    )

    # Allowing traffic on port 80
    response = client.authorize_security_group_ingress(
        GroupId=group_id,
        IpProtocol='tcp',
        FromPort=80,
        ToPort=80,
        CidrIp='0.0.0.0/0',
    )
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'InvalidPermission.Duplicate':
        print('Permission already set')

print('Security Group ID: ' + group_id)
