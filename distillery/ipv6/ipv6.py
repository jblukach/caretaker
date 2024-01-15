import boto3
import ipaddress
import json
import os
import sqlite3
from boto3.dynamodb.conditions import Key

def handler(event, context):

    if os.path.exists('/tmp/distillery.sqlite3'):
        os.remove('/tmp/distillery.sqlite3')

    db = sqlite3.connect('/tmp/distillery.sqlite3')
    db.execute('CREATE TABLE IF NOT EXISTS distillery (pk INTEGER PRIMARY KEY, cidr  BLOB, firstip INTEGER, lastip INTEGER)')
    db.execute('CREATE INDEX firstip_index ON distillery (firstip)')
    db.execute('CREATE INDEX lastip_index ON distillery (lastip)')

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    response = table.query(
        KeyConditionExpression=Key('pk').eq('ASN#') & Key('sk').begins_with('ASN#IPv6#')
    )
    responsedata = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.query(
            KeyConditionExpression=Key('pk').eq('ASN#') & Key('sk').begins_with('ASN#IPv6#'),
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        responsedata.update(response['Items'])

    for item in responsedata:

        netrange = ipaddress.IPv6Network(item['cidr'])
        first, last = netrange[0], netrange[-1]
        firstip = int(ipaddress.IPv6Address(first))
        lastip = int(ipaddress.IPv6Address(last))

        db.execute('INSERT INTO distillery (cidr, firstip, lastip) VALUES (?, ?, ?)', (item['cidr'], str(firstip), str(lastip)))

    db.commit()
    db.close()

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/distillery.sqlite3',
        os.environ['S3_BUCKET'],
        'distillery.sqlite3',
        ExtraArgs = {
            'ContentType': "application/x-sqlite3"
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Download Addresses')
    }