# pylint: disable=I0011
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0301
# pylint: disable=C0325

import boto3

client = boto3.client('opsworks')

response = client.stop_instance(
    InstanceId='f1afa8c7-99a9-4a6b-9767-80bc1ae150ab'
)

