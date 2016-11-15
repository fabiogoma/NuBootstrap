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

response = client.stop_instance(
    InstanceId=instance_id
)
print('Instance stop requested')

while True:
    try:
        response = client.delete_instance(
            InstanceId=instance_id
        )
        print('Instance deleted')
        break
    except botocore.exceptions.ClientError:
        # Instance still running. Try again in 10 sec
        time.sleep(10)

response = client.delete_layer(
    LayerId=layer_id
)
print('Layer deleted')

response = client.delete_stack(
    StackId=stack_id
)
print('Stack deleted')
