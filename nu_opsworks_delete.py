# pylint: disable=I0011
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0301
# pylint: disable=C0325

import ConfigParser
import time
import boto3
import botocore

client = boto3.client('opsworks')

config = ConfigParser.RawConfigParser()
config.read('opsworks-ids.properties')

instance_id = config.get('IDs', 'instance_id')
layer_id = config.get('IDs', 'layer_id')
stack_id = config.get('IDs', 'stack_id')

try:
    response = client.stop_instance(
        InstanceId=instance_id
    )
    print('Instance stop requested')
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'ResourceNotFoundException':
        print('Instance not found')

while True:
    try:
        response = client.delete_instance(
            InstanceId=instance_id
        )
        print('Instance deleted')
        break
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            break
        else:
            time.sleep(10)

try:
    response = client.delete_layer(
        LayerId=layer_id
    )
    print('Layer deleted')
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'ResourceNotFoundException':
        print('Layer not found')

try:
    response = client.delete_stack(
        StackId=stack_id
    )
    print('Stack deleted')
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'ResourceNotFoundException':
        print('Stack not found')
