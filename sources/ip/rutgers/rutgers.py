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
    response = requests.get('https://report.cs.rutgers.edu/DROP/attackers', headers=headers)
    data = response.text

    now = datetime.datetime.now()
    epoch = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    ttl = epoch+2592000 # plus 30 days
    seen = json.dumps(now, default=dateconverter)
    seen = seen.replace('"','')

    f = open('/tmp/rutgers4.txt', 'w')

    for line in data.splitlines():
        if line.startswith('#'):
            continue
        else:
            if ipaddress.ip_network(line).version == 4:
                iplist.append(str(line))
                f.write(str(line)+'\n')
            else:
                continue

    f.close()

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/rutgers4.txt',
        os.environ['S3_BUCKET'],
        'ipv4/rutgers.txt',
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
                'sk': 'IP#'+str(match)+'#SOURCE#rutgers.edu',
                'ip': str(match),
                'source': 'rutgers.edu',
                'last': seen,
                'epoch': epoch,
                'ttl': ttl
            }
        )
        verify.put_item(
            Item = {
                'pk': 'IP#',
                'sk': 'IP#'+str(match)+'#SOURCE#rutgers.edu',
                'ip': str(match),
                'source': 'rutgers.edu',
                'last': seen,
                'epoch': epoch
            }
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Check Rutgers Blocklist')
    }