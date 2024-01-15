import boto3
import netaddr
import json
import os
from boto3.dynamodb.conditions import Key

def handler(event, context):

    ndlist = []

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    response = table.query(
        KeyConditionExpression=Key('pk').eq('ASN#') & Key('sk').begins_with('ASN#IPv4#')
    )
    responsedata = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.query(
            KeyConditionExpression=Key('pk').eq('ASN#') & Key('sk').begins_with('ASN#IPv4#'),
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        responsedata.update(response['Items'])

    for item in responsedata:   
        network = netaddr.IPNetwork(item['cidr'])
        for addr in network:
            ndlist.append(str(addr))

    ndlist = list(set(ndlist))
    print('ND: '+str(len(ndlist)))

    with open('/tmp/addresses.txt', 'w') as f:
        for item in ndlist:
            f.write("%s\n" % item)

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/addresses.txt',
        os.environ['S3_BUCKET'],
        'addresses.txt',
        ExtraArgs = {
            'ContentType': "text/plain"
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Download Addresses')
    }