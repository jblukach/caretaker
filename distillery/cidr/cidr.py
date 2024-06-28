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
    asns.append({"num":14090,"desc":"North Dakota Telephone"})
    asns.append({"num":29744,"desc":"United Telephone"})
    asns.append({"num":14511,"desc":"Polar Communications"})
    asns.append({"num":31758,"desc":"Griggs County Telephone"})
    asns.append({"num":26794,"desc":"Dakota Carrier Network"})
    asns.append({"num":11138,"desc":"BEK Communications"})
    asns.append({"num":63414,"desc":"Dakota Central Telecommunications"})
    asns.append({"num":32809,"desc":"Dickey Rural Networks"})
    asns.append({"num":14543,"desc":"SRT Communications"})
    asns.append({"num":27539,"desc":"West River Telecommunications"})
    asns.append({"num":18780,"desc":"Reservation Telephone"})
    asns.append({"num":33339,"desc":"Nemont Telecommunications"})
    asns.append({"num":36374,"desc":"Red River Communications"})
    asns.append({"num":19530,"desc":"State of North Dakota"})
    asns.append({"num":15267,"desc":"702 Communications"})
    asns.append({"num":21730,"desc":"Halstad Telephone Company"})
    asns.append({"num":12042,"desc":"Consolidated Communications"})
    asns.append({"num":11232,"desc":"Midcontinent Communications"})

    for asn in asns:

        time.sleep(random.randint(3, 7))

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

        headers = {'User-Agent': 'Project Caretaker (https://github.com/jblukach/caretaker) '+str(uuid.uuid1())}
        r = requests.get('https://rdap.arin.net/registry/arin_originas0_networksbyoriginas/'+str(asn['num']), headers=headers)
        print('AS'+str(asn['num'])+' Status Code: '+str(r.status_code))
        output = r.json()

        for item in output['arin_originas0_networkSearchResults']:

            if item['ipVersion'] == 'v4':

                value = item['cidr0_cidrs'][0]['v4prefix']+'/'+str(item['cidr0_cidrs'][0]['length'])

                netrange = ipaddress.IPv4Network(value)
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv4Address(first))
                lastip = int(ipaddress.IPv4Address(last))

                cidrlist.append(value)

                if value not in existing:

                    print('Add: '+value)

                    table.put_item(
                        Item = {
                            'pk': 'ASN#',
                            'sk': 'ASN#IPv4#'+value,
                            'name': 'AS'+str(asn['num']),
                            'description': asn['desc'],
                            'cidr': value,
                            'firstip': firstip,
                            'lastip': lastip,
                            'asn': asn['num']
                        }
                    )

            elif item['ipVersion'] == 'v6':

                value = item['cidr0_cidrs'][0]['v6prefix']+'/'+str(item['cidr0_cidrs'][0]['length'])

                netrange = ipaddress.IPv6Network(value)
                first, last = netrange[0], netrange[-1]
                firstip = int(ipaddress.IPv6Address(first))
                lastip = int(ipaddress.IPv6Address(last))

                cidrlist.append(value)

                if value not in existing:

                    print('Add: '+value)

                    table.put_item(
                        Item = {
                            'pk': 'ASN#',
                            'sk': 'ASN#IPv6#'+value,
                            'name': 'AS'+str(asn['num']),
                            'description': asn['desc'],
                            'cidr': value,
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