import boto3
import datetime
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

    response = requests.get('https://osint.digitalside.it/Threat-Intel/lists/latestips.txt')
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
            if ipaddress.ip_network(line).version == 4:
                iplist.append(str(line))
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
                'sk': 'IP#'+str(match)+'#SOURCE#osint.digitalside.it',
                'ip': str(match),
                'source': 'osint.digitalside.it',
                'last': seen,
                'epoch': epoch
            }
        )
        verify.put_item(
            Item = {
                'pk': 'IP#',
                'sk': 'IP#'+str(match)+'#SOURCE#osint.digitalside.it',
                'ip': str(match),
                'source': 'osint.digitalside.it',
                'last': seen,
                'epoch': epoch
            }
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Check Digital Side Blocklist')
    }