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

properties = open('sqs.properties', 'w')
properties.write('[IDs]\n')
properties.write('launch_queue_url=' + launch_queue_url + '\n')
properties.write('destroy_queue_url=' + destroy_queue_url + '\n')
properties.close()

print('Launch Queue URL: ' + launch_queue_url)
print('Destroy Queue URL: ' + destroy_queue_url)
