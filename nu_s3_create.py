# pylint: disable=I0011
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0301
# pylint: disable=C0325

import boto3
import botocore

try:
    client = boto3.client('s3')
    response = client.create_bucket(
        Bucket='nustorage',
        CreateBucketConfiguration={
            'LocationConstraint': 'us-west-2'
        }
    )
    print("Bucket 'nustorage' created")
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
        print('Bucket already available')

s3 = boto3.resource('s3')
s3.Bucket('nustorage').upload_file('/home/fabiom/vms/aws/bootstrap/nubootstrap.yml.gz', 'nubootstrap.yml.gz')
