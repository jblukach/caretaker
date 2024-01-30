import boto3
import datetime
import ipaddress
import json
import os
import requests

def dateconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    feed = dynamodb.Table(os.environ['FEED_TABLE'])
    verify = dynamodb.Table(os.environ['VERIFY_TABLE'])

    iplist = []
    ndlist = []

    s3 = boto3.client('s3')
    s3.download_file(os.environ['S3_BUCKET'], 'addresses.txt', '/tmp/addresses.txt')

    with open('/tmp/addresses.txt', 'r') as f:
        for item in f.readlines():
            ndlist.append(str(item[:-1]))

    ndlist = list(set(ndlist))
    print('ND: '+str(len(ndlist)))

    headers = {'User-Agent': 'Project Caretaker (https://github.com/jblukach/caretaker)'}
    response = requests.get('https://raw.githubusercontent.com/drb-ra/C2IntelFeeds/master/feeds/IPC2s-30day.csv', headers=headers)
    data = response.text

    now = datetime.datetime.now()
    orig = datetime.datetime.utcfromtimestamp(0)
    epoch = int((now - orig).total_seconds() * 1000.0)
    seen = json.dumps(now, default=dateconverter)
    seen = seen.replace('"','')

    for line in data.splitlines():
        if line.startswith('#'):
            continue
        else:
            out = line.split(',')
            if ipaddress.ip_network(out[0]).version == 4:
                iplist.append(str(out[0]))
            else:
                continue

    iplist = list(set(iplist))
    print('BL: '+str(len(iplist)))

    matches = list(set(iplist).intersection(ndlist))
    print('Matches: '+str(len(matches)))

    for match in matches:
        feed.put_item(
            Item = {
                'pk': 'IP#',
                'sk': 'IP#'+str(match)+'#SOURCE#github.com/drb-ra',
                'ip': str(match),
                'source': 'github.com/drb-ra',
                'last': seen,
                'epoch': epoch
            }
        )
        verify.put_item(
            Item = {
                'pk': 'IP#',
                'sk': 'IP#'+str(match)+'#SOURCE#github.com/drb-ra',
                'ip': str(match),
                'source': 'github.com/drb-ra',
                'last': seen,
                'epoch': epoch
            }
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Check C2 Intel Feeds Blocklist')
    }