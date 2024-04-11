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

    headers = {'User-Agent': 'Project Caretaker (https://github.com/jblukach/caretaker)'}
    response = requests.get('http://data.phishtank.com/data/online-valid.csv', headers=headers)
    data = response.text

    now = datetime.datetime.now()
    epoch = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    ttl = epoch+2592000 # plus 30 days
    seen = json.dumps(now, default=dateconverter)
    seen = seen.replace('"','')

    domains = []
    f = open('/tmp/phishtank.txt', 'w')

    try: # PhishTank Returns Image Binary Sporadically

        for line in data.splitlines(True)[1:]:
            if line.startswith('#'):
                continue
            else:
                line = line.split(',')[1]
                line = line.split('/')[2]
                domains.append(line)
                f.write(str(line)+'\n')

    except Exception as e:

        print(str(e))

        return {
            'statusCode': 500,
            'body': json.dumps('PhishTank Returns Image Binary Sporadically')
        }

    f.close()

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/phishtank.txt',
        'projectcaretaker',
        'dns/phishtank.txt',
        ExtraArgs = {
            'ContentType': "text/plain"
        }
    )

    domains = list(set(domains))
    print('Domains: '+str(len(domains)))

    s3 = boto3.client('s3')
    s3.download_file(os.environ['S3_BUCKET'], 'domains.txt', '/tmp/domains.txt')

    nddns = []

    with open('/tmp/domains.txt', 'r') as f:
        for item in f.readlines():
            nddns.append(item[:-1])
    
    nddns = list(set(nddns))
    print('ND DNS: '+str(len(nddns)))

    matches = list(set(domains).intersection(nddns))
    print('Matches: '+str(len(matches)))

    for match in matches:
        feed.put_item(
            Item = {
                'pk': 'DNS#',
                'sk': 'DNS#'+str(match)+'#SOURCE#phishtank.com',
                'dns': str(match),
                'source': 'phishtank.com',
                'last': seen,
                'epoch': epoch,
                'ttl': ttl
            }
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Check Phish Tank Blocklist')
    }