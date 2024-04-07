import boto3
import datetime
import json
import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

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

        retry_strategy = Retry(
            total = 3,
            status_forcelist = [429, 500, 502, 503, 504],
            backoff_factor = 1
        )

        adapter = HTTPAdapter(
            max_retries = retry_strategy
        )

        http = requests.Session()
        http.mount("https://", adapter)

        headers = {'User-Agent': 'Project Caretaker (https://github.com/jblukach/caretaker)'}
        response = http.get('https://geo.tundralabs.net/'+ip, headers=headers)

        data = response.text
        data = json.loads(data)

        data['pk'] = 'IP#'
        data['sk'] = 'IP#'+str(ip)
        data['ip'] = ip
        data['latitude'] = str(data['latitude'])
        data['longitude'] = str(data['longitude'])

        epoch = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
        ttl = epoch+2592000 # plus 30 days

        data['ttl'] = ttl

        dynamodb = boto3.resource('dynamodb')
        map = dynamodb.Table(os.environ['MAP_TABLE'])

        map.put_item(
            Item = data
        )

    return {
        'statusCode': 200,
        'body': json.dumps('MaxMind GeoLite2 Enrichment')
    }