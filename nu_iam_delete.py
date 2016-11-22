# pylint: disable=I0011
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0301
# pylint: disable=C0325

import boto3
import botocore

client = boto3.client('iam')

try:
    response = client.delete_role_policy(
        RoleName='aws-opsworks-service-role',
        PolicyName='aws-opsworks-service-policy'
    )    
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'NoSuchEntity': 
        print('Item not found')

try:
    response = client.remove_role_from_instance_profile(
        InstanceProfileName='aws-opsworks-ec2-role',
        RoleName='aws-opsworks-ec2-role'
    )    
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'NoSuchEntity': 
        print('Item not found')

try:
    response = client.delete_instance_profile(
        InstanceProfileName='aws-opsworks-ec2-role'
    )    
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'NoSuchEntity': 
        print('Item not found')

try:
    response = client.delete_role(
        RoleName='aws-opsworks-service-role'
    )    
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'NoSuchEntity': 
        print('Item not found')

try:
    response = client.delete_role(
        RoleName='aws-opsworks-ec2-role'
    )
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'NoSuchEntity': 
        print('Item not found')
