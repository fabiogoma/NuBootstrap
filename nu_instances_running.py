# pylint: disable=I0011
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0301
# pylint: disable=C0325

import boto3

client = boto3.client('ec2')

response = client.describe_instances(
    Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                'running'
            ]
        }
    ]
)

i = 0
print len(response)
while i < len(response):
    print response['Reservations'][i]['Instances'][0]['InstanceId']
    print response['Reservations'][i]['Instances'][0]['PublicIpAddress']
    print response['Reservations'][i]['Instances'][0]['SecurityGroups'][0]['GroupName']
    print "\n"
    i += 1
