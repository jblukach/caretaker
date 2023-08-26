import boto3
import json
import os
import requests

def handler(event, context):

    for record in event['Records']:

        try:
            ip = record['dynamodb']['NewImage']['ip']['S']
        except:
            pass

        try:
            ip = record['dynamodb']['OldImage']['ip']['S']
        except:
            pass

        response = requests.get('https://geo.tundralabs.net/'+ip)
        data = response.text
        data = json.loads(data)

        data['pk'] = 'IP#'
        data['sk'] = 'IP#'+str(ip)
        data['ip'] = ip
        data['latitude'] = str(data['latitude'])
        data['longitude'] = str(data['longitude'])

        dynamodb = boto3.resource('dynamodb')
        map = dynamodb.Table(os.environ['MAP_TABLE'])

        map.put_item(
            Item = data
        )

    return {
        'statusCode': 200,
        'body': json.dumps('MaxMind GeoLite2 Enrichment')
    }