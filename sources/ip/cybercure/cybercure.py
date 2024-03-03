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
    response = requests.get('https://api.cybercure.ai/feed/get_ips?type=csv', headers=headers)
    data = response.text

    now = datetime.datetime.now()
    orig = datetime.datetime.utcfromtimestamp(0)
    epoch = int((now - orig).total_seconds() * 1000.0)
    seen = json.dumps(now, default=dateconverter)
    seen = seen.replace('"','')

    f = open('/tmp/cybercure.txt', 'w')

    for line in data.splitlines():
        try:
            ips = line.split(',')
            for ip in ips:
                if ipaddress.ip_network(ip).version == 4:
                    iplist.append(str(ip))
                    f.write(str(ip)+'\n')
        except:
            continue        

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/cybercure.txt',
        'projectcaretaker',
        'ip/cybercure.txt',
        ExtraArgs = {
            'ContentType': "text/plain"
        }
    )

    iplist = list(set(iplist))
    print('BL: '+str(len(iplist)))

    matches = list(set(iplist).intersection(ndlist))
    print('Matches: '+str(len(matches)))

    for match in matches:
        feed.put_item(
            Item = {
                'pk': 'IP#',
                'sk': 'IP#'+str(match)+'#SOURCE#cybercure.ai',
                'ip': str(match),
                'source': 'cybercure.ai',
                'last': seen,
                'epoch': epoch
            }
        )
        verify.put_item(
            Item = {
                'pk': 'IP#',
                'sk': 'IP#'+str(match)+'#SOURCE#cybercure.ai',
                'ip': str(match),
                'source': 'cybercure.ai',
                'last': seen,
                'epoch': epoch
            }
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Check Cyber Cure Blocklist')
    }