import boto3
import datetime
import ipaddress
import json
import os
import requests
import sqlite3

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
    s3.download_file(os.environ['S3_BUCKET'], 'distillery.sqlite3', '/tmp/distillery.sqlite3')
    s3.download_file(os.environ['S3_BUCKET'], 'addresses.txt', '/tmp/addresses.txt')

    with open('/tmp/addresses.txt', 'r') as f:
        for item in f.readlines():
            ndlist.append(str(item[:-1]))

    ndlist = list(set(ndlist))
    print('ND: '+str(len(ndlist)))

    headers = {'User-Agent': 'Project Caretaker (https://github.com/jblukach/caretaker)'}
    response = requests.get('https://www.dan.me.uk/torlist/', headers=headers)
    data = response.text

    now = datetime.datetime.now()
    epoch = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    ttl = epoch+2592000 # plus 30 days
    seen = json.dumps(now, default=dateconverter)
    seen = seen.replace('"','')

    f = open('/tmp/tor4.txt', 'w')
    g = open('/tmp/tor6.txt', 'w')

    for line in data.splitlines():

        value = line.split('#')
        line = value[0]

        if ipaddress.ip_network(line).version == 4:
            iplist.append(line)
            f.write(str(line)+'\n')
        else:
            intip = int(ipaddress.IPv6Address(line))
            g.write(str(line)+'\n')

            conn = sqlite3.connect('/tmp/distillery.sqlite3')
            c = conn.cursor()
            c.execute("SELECT cidr FROM distillery WHERE firstip <= ? AND lastip >= ?", (str(intip), str(intip)))
            results = c.fetchall()
            conn.close()
    
            if len(results) > 0:
                feed.put_item(
                    Item = {
                        'pk': 'IP#',
                        'sk': 'IP#'+str(line)+'#SOURCE#dan.me.uk',
                        'ip': str(line),
                        'source': 'dan.me.uk',
                        'last': seen,
                        'epoch': epoch,
                        'ttl': ttl
                    }
                )
                verify.put_item(
                    Item = {
                        'pk': 'IP#',
                        'sk': 'IP#'+str(line)+'#SOURCE#dan.me.uk',
                        'ip': str(line),
                        'source': 'dan.me.uk',
                        'last': seen,
                        'epoch': epoch
                    }
                )

    f.close()
    g.close()

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/tor4.txt',
        os.environ['S3_BUCKET'],
        'ipv4/tor.txt',
        ExtraArgs = {
            'ContentType': "text/plain"
        }
    )

    s3.meta.client.upload_file(
        '/tmp/tor6.txt',
        os.environ['S3_BUCKET'],
        'ipv6/tor.txt',
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
                'sk': 'IP#'+str(match)+'#SOURCE#dan.me.uk',
                'ip': str(match),
                'source': 'dan.me.uk',
                'last': seen,
                'epoch': epoch,
                'ttl': ttl
            }
        )
        verify.put_item(
            Item = {
                'pk': 'IP#',
                'sk': 'IP#'+str(match)+'#SOURCE#dan.me.uk',
                'ip': str(match),
                'source': 'dan.me.uk',
                'last': seen,
                'epoch': epoch
            }
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Identify Tor Onion Network')
    }