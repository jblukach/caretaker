import boto3
import json
import os
import sqlite3
from boto3.dynamodb.conditions import Key

def handler(event, context):

    if os.path.exists('/tmp/allcidrs.sqlite3'):
        os.remove('/tmp/allcidrs.sqlite3')

    db = sqlite3.connect('/tmp/allcidrs.sqlite3')
    db.execute('CREATE TABLE IF NOT EXISTS allcidrs (pk INTEGER PRIMARY KEY, cidr  BLOB, firstip INTEGER, lastip INTEGER)')
    db.execute('CREATE INDEX firstip_index ON allcidrs (firstip)')
    db.execute('CREATE INDEX lastip_index ON allcidrs (lastip)')

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    response = table.query(
        KeyConditionExpression=Key('pk').eq('ASN#') & Key('sk').begins_with('ASN#IPv')
    )
    responsedata = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.query(
            KeyConditionExpression=Key('pk').eq('ASN#') & Key('sk').begins_with('ASN#IPv'),
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        responsedata.update(response['Items'])

    print('Downloaded ' + str(len(responsedata)) + ' IPv4/6 cidrs')

    for item in responsedata:

        db.execute('INSERT INTO allcidrs (cidr, firstip, lastip) VALUES (?, ?, ?)', (item['cidr'], str(item['firstip']), str(item['lastip'])))

    db.commit()
    db.close()

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/allcidrs.sqlite3',
        os.environ['S3_BUCKET'],
        'allcidrs.sqlite3',
        ExtraArgs = {
            'ContentType': "application/x-sqlite3"
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Download Addresses')
    }