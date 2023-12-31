import boto3
import datetime
import hashlib
import ipaddress
import netaddr
import json
import os
import requests
from boto3.dynamodb.conditions import Key

def dateconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    feed = dynamodb.Table(os.environ['FEED_TABLE'])
    verify = dynamodb.Table(os.environ['VERIFY_TABLE'])

    iplist = []
    ndlist = []

    response = table.query(
        KeyConditionExpression=Key('pk').eq('ASN#') & Key('sk').begins_with('ASN#IPv4#')
    )
    responsedata = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.query(
            KeyConditionExpression=Key('pk').eq('ASN#') & Key('sk').begins_with('ASN#IPv4#'),
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        responsedata.update(response['Items'])

    for item in responsedata:   
        network = netaddr.IPNetwork(item['cidr'])
        for addr in network:
            ndlist.append(str(addr))

    ndlist = list(set(ndlist))
    print('ND: '+str(len(ndlist)))

    headers = {'User-Agent': 'Project Caretaker (https://github.com/jblukach/caretaker)'}
    response = requests.get('https://lists.blocklist.de/lists/all.txt.md5', headers=headers)
    md5 = response.text

    headers = {'User-Agent': 'Project Caretaker (https://github.com/jblukach/caretaker)'}
    response = requests.get('https://lists.blocklist.de/lists/all.txt', headers=headers)
    data = response.text

    now = datetime.datetime.now()
    orig = datetime.datetime.utcfromtimestamp(0)
    epoch = int((now - orig).total_seconds() * 1000.0)
    seen = json.dumps(now, default=dateconverter)
    seen = seen.replace('"','')

    if hashlib.md5(data.encode('utf-8')).hexdigest() == md5:
        for line in data.splitlines():
            if ipaddress.ip_network(line).version == 4:
                iplist.append(line)
            else:
                intip = int(ipaddress.IPv6Address(line))

                firstlist = []
                first = table.query(
                    IndexName = 'firstip',
                    KeyConditionExpression = Key('pk').eq('ASN#') & Key('firstip').lte(intip)
                )
                firstdata = first['Items']
                while 'LastEvaluatedKey' in first:
                    first = table.query(
                        IndexName = 'firstip',
                        KeyConditionExpression = Key('pk').eq('ASN#') & Key('firstip').lte(intip),
                        ExclusiveStartKey = first['LastEvaluatedKey']
                    )
                    firstdata.extend(first['Items'])
                for item in firstdata:
                    firstlist.append(item['cidr'])

                lastlist = []
                last = table.query(
                    IndexName = 'lastip',
                    KeyConditionExpression = Key('pk').eq('ASN#') & Key('lastip').gte(intip)
                )
                lastdata = last['Items']
                while 'LastEvaluatedKey' in last:
                    last = table.query(
                        IndexName = 'lastip',
                        KeyConditionExpression = Key('pk').eq('ASN#') & Key('lastip').gte(intip),
                        ExclusiveStartKey = last['LastEvaluatedKey']
                    )
                    lastdata.extend(last['Items'])
                for item in lastdata:
                    lastlist.append(item['cidr'])

                matches = set(firstlist) & set(lastlist)
    
                if len(matches) > 0:
                    feed.put_item(
                        Item = {
                            'pk': 'IP#',
                            'sk': 'IP#'+str(line)+'#SOURCE#blocklist.de',
                            'ip': str(line),
                            'source': 'blocklist.de',
                            'last': seen,
                            'epoch': epoch
                        }
                    )
                    verify.put_item(
                        Item = {
                            'pk': 'IP#',
                            'sk': 'IP#'+str(line)+'#SOURCE#blocklist.de',
                            'ip': str(line),
                            'source': 'blocklist.de',
                            'last': seen,
                            'epoch': epoch
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
                'sk': 'IP#'+str(match)+'#SOURCE#blocklist.de',
                'ip': str(match),
                'source': 'blocklist.de',
                'last': seen,
                'epoch': epoch
            }
        )
        verify.put_item(
            Item = {
                'pk': 'IP#',
                'sk': 'IP#'+str(match)+'#SOURCE#blocklist.de',
                'ip': str(match),
                'source': 'blocklist.de',
                'last': seen,
                'epoch': epoch
            }
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Check Fail2Ban Blocklist')
    }