# pylint: disable=I0011
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0301
# pylint: disable=C0325

import boto3

client = boto3.client('opsworks')

response = client.stop_instance(
    InstanceId='eb8138be-9aed-4102-9e74-6088051d076d'
)

