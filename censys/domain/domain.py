import boto3
import json
import os
from boto3.dynamodb.conditions import Key

def handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TLD_TABLE'])

    response = table.query(
        KeyConditionExpression = Key('pk').eq('TLD#')
    )
    responsedata = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.query(
            KeyConditionExpression = Key('pk').eq('TLD#'),
            ExclusiveStartKey = response['LastEvaluatedKey']
        )
        responsedata.update(response['Items'])

    tlds = []

    for entry in responsedata:
        tlds.append(entry['sk'])

    print('DynamoDB: '+str(len(responsedata)))
    print('TLDs: '+str(len(tlds)))

    s3 = boto3.client('s3')
    s3.download_file(os.environ['S3_BUCKET'], 'certificates.json', '/tmp/certificates.json')

    with open('/tmp/certificates.json') as json_file:
        data = json.load(json_file)
        print('S3: '+str(len(data)))

    domains = []

    for entry in data:
        for name in entry['names']:
            if name.split('.')[-1] in tlds:
                if name.startswith('*.'):
                    name = name[2:]
                domains.append(name.lower())

    print('Domains: '+str(len(domains)))
    domains = list(set(domains))
    print('Unique: '+str(len(domains)))

    with open('/tmp/domains.txt', 'w') as f:
        for item in domains:
            f.write("%s\n" % str(item))
    f.close()

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/domains.txt',
        os.environ['S3_BUCKET'],
        'domains.txt',
        ExtraArgs = {
            'ContentType': "text/plain"
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Check List of Top-Level Domains')
    }