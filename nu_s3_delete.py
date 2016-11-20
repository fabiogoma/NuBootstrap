# pylint: disable=I0011
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0301
# pylint: disable=C0325

import boto3

client = boto3.client('s3')

response = client.delete_object(
    Bucket='nustorage',
    Key='nubootstrap.yml.gz'
)
print("Object deleted")

response = client.delete_bucket(
    Bucket='nustorage'
)
print("Bucket deleted")
