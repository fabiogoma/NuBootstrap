# pylint: disable=I0011
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0301
# pylint: disable=C0325

import sys
import boto3
import botocore

client = boto3.client('ec2')

instance_id = str(sys.argv[1])

try:
    # Create EC2 Security Group (Don't forget to change VpcId')
    response = client.describe_instances(
        InstanceIds=[
            instance_id,
        ],
    )
    instance_status = response['Reservations'][0]['Instances'][0]['State']['Name']
    public_name_dns = response['Reservations'][0]['Instances'][0]['PublicDnsName']
    print('Instance State: ' + instance_status)
    print('Public DNS: ' + public_name_dns)
except botocore.exceptions.ClientError as e:
    #if e.response['Error']['Code'] == 'InvalidGroup.Duplicate':
    #    print('Group already exists')
    print(e.response['Error']['Code'])
