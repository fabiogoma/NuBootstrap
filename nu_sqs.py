# pylint: disable=I0011
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0301
# pylint: disable=C0325

import boto3

client = boto3.client('sqs')

response = client.create_queue(
    QueueName='sqs_launch'
)
launch_queue_url = response['QueueUrl']

response = client.create_queue(
    QueueName='sqs_destroy'
)
destroy_queue_url = response['QueueUrl']

print('Launch Queue URL: ' + launch_queue_url)
print('Destroy Queue URL: ' + destroy_queue_url)
