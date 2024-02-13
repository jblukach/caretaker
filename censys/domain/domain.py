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
                if name.startswith('www.'):
                    domains.append(name.lower())
                    name = name[4:]
                    domains.append(name.lower())
                else:
                    domains.append(name.lower())
                    name = 'www.' + name
                    domains.append(name.lower())

    ### EMAIL DOMAINS ###

    count = 0
    s3.download_file(os.environ['S3_EMAIL'], 'dns.txt', '/tmp/dns.txt')

    with open('/tmp/dns.txt') as f:
        for line in f:
            domains.append(line.strip())
            count += 1
    f.close()

    print('Email: '+str(count))

    ### HOTEL DOMAINS ###

    count = 0
    s3.download_file(os.environ['S3_BUCKET'], 'hotels.txt', '/tmp/hotels.txt')

    with open('/tmp/hotels.txt') as f:
        for line in f:
            domains.append(line.strip())
            count += 1
    f.close()

    print('Hotels: '+str(count))

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