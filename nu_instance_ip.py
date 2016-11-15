# pylint: disable=I0011
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0301
# pylint: disable=C0325

import boto3

client = boto3.client('opsworks')

response = client.describe_instances(
    StackId='d06be382-2070-4d7d-b1f1-ad7352be6b4d'
)

print('Public IP: ' + response['Instances'][0]['PublicIp'])
