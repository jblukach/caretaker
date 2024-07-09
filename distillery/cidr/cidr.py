import boto3
import ipaddress
import json
import os
import random
import requests
import time
import uuid
from boto3.dynamodb.conditions import Key
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    cidrlist = []
    existing = []

    response = table.query(KeyConditionExpression=Key('pk').eq('ASN#'))
    responsedata = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.query(
            KeyConditionExpression=Key('pk').eq('ASN#'),
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        responsedata.update(response['Items'])

    for item in responsedata:
        existing.append(item['cidr'])

    asns = []
    asns.append({"num":11138,"desc":"BEK Communications Cooperative","handle":"BCC-141"})
    asns.append({"num":11232,"desc":"Midcontinent Communications","handle":"MIDCO-1"})
    asns.append({"num":14090,"desc":"North Dakota Telephone Company","handle":"GONDT"})
    asns.append({"num":14511,"desc":"Polar Communications","handle":"PLAR"})
    asns.append({"num":14543,"desc":"SRT Communications, Inc.","handle":"SRTC"})
    asns.append({"num":15267,"desc":"702 Communications","handle":"702COM"})
    asns.append({"num":18780,"desc":"Reservation Telephone Coop.","handle":"RTC-81"})
    asns.append({"num":19530,"desc":"State of North Dakota, ITD","handle":"SNDI-1"})
    asns.append({"num":21730,"desc":"Halstad Telephone Company","handle":"HALSTA"})
    asns.append({"num":26794,"desc":"Dakota Carrier Network","handle":"DCN-38"})
    asns.append({"num":27539,"desc":"West River Telecommunications Cooperative","handle":"WRVR"})
    asns.append({"num":29744,"desc":"United Telephone Mutual Aid Corporation","handle":"UNITED-190"})
    asns.append({"num":31758,"desc":"Griggs County Telephone Co.","handle":"GCT-43"})
    asns.append({"num":32809,"desc":"Dickey Rural Networks","handle":"DRN-3"})
    asns.append({"num":33339,"desc":"Nemont Telecommunications","handle":"NEMON-2"})
    asns.append({"num":36374,"desc":"Stellar Association, LLC","handle":"SAL-65"})
    asns.append({"num":55105,"desc":"Northwest Communications Cooperative","handle":"NCC-115"})
    asns.append({"num":63414,"desc":"Dakota Central Telecommunications Cooperative","handle":"DAKTE"})
    asns.append({"num":400439,"desc":"Consolidated Telecommunications","handle":"CONSO-10"})

    for asn in asns:

        time.sleep(1)

        headers = {'User-Agent': 'Project Caretaker (https://github.com/jblukach/caretaker)'}
        r = requests.get('https://api.bgpview.io/asn/'+str(asn['num'])+'/prefixes', headers=headers)
        print('AS'+str(asn['num'])+' Status Code: '+str(r.status_code))
        output = r.json()

        for entry in output['data']['ipv4_prefixes']:

            hostmask = entry['prefix'].split('/')
            iptype = ipaddress.ip_address(hostmask[0])
            netrange = ipaddress.IPv4Network(entry['prefix'])
            first, last = netrange[0], netrange[-1]
            firstip = int(ipaddress.IPv4Address(first))
            lastip = int(ipaddress.IPv4Address(last))

            cidrlist.append(entry['prefix'])

            if entry['prefix'] not in existing:

                print('Add: '+entry['prefix'])

                table.put_item(
                    Item = {
                        'pk': 'ASN#',
                        'sk': 'ASN#IPv'+str(iptype.version)+'#'+entry['prefix'],
                        'name': entry['name'],
                        'description': entry['description'],
                        'cidr': entry['prefix'],
                        'firstip': firstip,
                        'lastip': lastip,
                        'asn': asn['num']
                    }
                )

        for entry in output['data']['ipv6_prefixes']:

            hostmask = entry['prefix'].split('/')
            iptype = ipaddress.ip_address(hostmask[0])
            netrange = ipaddress.IPv6Network(entry['prefix'])
            first, last = netrange[0], netrange[-1]
            firstip = int(ipaddress.IPv6Address(first))
            lastip = int(ipaddress.IPv6Address(last))

            cidrlist.append(entry['prefix'])

            if entry['prefix'] not in existing:

                print('Add: '+entry['prefix'])

                table.put_item(
                    Item = {
                        'pk': 'ASN#',
                        'sk': 'ASN#IPv'+str(iptype.version)+'#'+entry['prefix'],
                        'name': entry['name'],
                        'description': entry['description'],
                        'cidr': entry['prefix'],
                        'firstip': firstip,
                        'lastip': lastip,
                        'asn': asn['num']
                    }
                )

    for cidr in existing:

        if cidr not in cidrlist:

            hostmask = cidr.split('/')
            iptype = ipaddress.ip_address(hostmask[0])

            response = table.delete_item(Key={'pk': 'ASN#', 'sk': 'ASN#IPv'+str(iptype.version)+'#'+cidr})

            print('Delete: '+cidr)

    return {
        'statusCode': 200,
        'body': json.dumps('Download ASN Ranges')
    }