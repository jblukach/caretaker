import boto3
import datetime
import json
import os
import requests

def dateconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    feed = dynamodb.Table(os.environ['FEED_TABLE'])

    response = requests.get('https://api.cybercure.ai/feed/get_url?type=csv')
    data = response.text

    now = datetime.datetime.now()
    orig = datetime.datetime.utcfromtimestamp(0)
    epoch = int((now - orig).total_seconds() * 1000.0)
    seen = json.dumps(now, default=dateconverter)
    seen = seen.replace('"','')

    domains = []

    for line in data.splitlines():
        try:
            urls = line.split(',')
            for url in urls:
                out = url.split('/')
                domains.append(out[2])
                print(out[2])
        except:
            continue   

    domains = list(set(domains))
    print('Domains: '+str(len(domains)))

    s3 = boto3.client('s3')
    s3.download_file(os.environ['S3_BUCKET'], 'domains.txt', '/tmp/domains.txt')

    nddns = []

    with open('/tmp/domains.txt', 'r') as f:
        for item in f.readlines():
            nddns.append(item)
    
    nddns = list(set(nddns))
    print('ND DNS: '+str(len(nddns)))

    matches = list(set(domains).intersection(nddns))
    print('Matches: '+str(len(matches)))

    for match in matches:
        feed.put_item(
            Item = {
                'pk': 'DNS#',
                'sk': 'DNS#'+str(match)+'#SOURCE#cybercure.ai',
                'dns': str(match),
                'source': 'cybercure.ai',
                'last': seen,
                'epoch': epoch
            }
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Check Cyber Cure Blocklist')
    }