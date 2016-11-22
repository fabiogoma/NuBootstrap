# pylint: disable=I0011
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0301
# pylint: disable=C0325

import boto3
import botocore

client = boto3.client('sqs')

# Delete Launch Queue
try:
    response = client.get_queue_url(
        QueueName='sqs_launch',
    )
    launch_queue_url = response['QueueUrl']

    response = client.delete_queue(
        QueueUrl=launch_queue_url
    )
    print(launch_queue_url + ' deleted')
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue':
        print('Non existent queue')

# Delete Destroy Queue
try:
    response = client.get_queue_url(
        QueueName='sqs_destroy',
    )
    destroy_queue_url = response['QueueUrl']

    response = client.delete_queue(
        QueueUrl=destroy_queue_url
    )
    print(destroy_queue_url + ' deleted')
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue':
        print('Non existent queue')

# Delete Update Queue
try:
    response = client.get_queue_url(
        QueueName='sqs_update',
    )
    update_queue_url = response['QueueUrl']

    response = client.delete_queue(
        QueueUrl=update_queue_url
    )
    print(update_queue_url + ' deleted')
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue':
        print('Non existent queue')
