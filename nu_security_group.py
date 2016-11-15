# pylint: disable=I0011
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0301
# pylint: disable=C0325

import boto3

client = boto3.client('ec2')

# Create EC2 Security Group (Don't forget to change VpcId')
response = client.create_security_group(
    GroupName='nu-default-sg',
    Description='Nu Security Group',
    VpcId='vpc-7a659f1d'
)
group_id = response['GroupId']

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

print(group_id)