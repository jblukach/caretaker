import boto3
import json
import os

def handler(event, context):

    s3 = boto3.client('s3')

    ### IP ###

    files = s3.list_objects(
        Bucket = os.environ['STAGE_BUCKET'],
        Prefix = 'ip'
    )['Contents']

    for file in files:
        print(file['Key'])



        break

    ### DNS ###

    files = s3.list_objects(
        Bucket = os.environ['STAGE_BUCKET'],
        Prefix = 'dns'
    )['Contents']

    for file in files:
        print(file['Key'])



        break

    return {
        'statusCode': 200,
        'body': json.dumps('Publish Distillery')
    }