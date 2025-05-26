import boto3
from botocore.client import Config

# Configure R2 client
client = boto3.client('s3',
    endpoint_url='https://.r2.cloudflarestorage.com',
    aws_access_key_id='',
    aws_secret_access_key='',
    config=Config(signature_version='s3v4')
)

# 1. Delete all objects
paginator = client.get_paginator('list_objects_v2')
for page in paginator.paginate(Bucket=''):
    print(f"Deleting objects in bucket '': {page.get('Contents', [])}")
    for obj in page.get('Contents', []):
        print(f"Deleting object: {obj['Key']}")
        client.delete_object(Bucket='', Key=obj['Key'])

# 2. Delete bucket (optional)
client.delete_bucket(Bucket='')