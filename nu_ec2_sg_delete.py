# pylint: disable=I0011
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0301
# pylint: disable=C0325

import boto3
import botocore

client = boto3.client('ec2')

try:
    response = client.delete_security_group(
        GroupName='nu-default-sg'
    )
    print('Group deleted')
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'InvalidGroup.NotFound':
        print('Item not found')
