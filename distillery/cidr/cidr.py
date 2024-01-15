import boto3
import ipaddress
import json
import os
import requests
import time
from boto3.dynamodb.conditions import Key

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
    asns.append('14090') # North Dakota Telephone
    asns.append('29744') # United Telephone
    asns.append('14511') # Polar Communications
    asns.append('31758') # Griggs County Telephone
    asns.append('26794') # Dakota Carrier Network
    asns.append('11138') # BEK Communications
    asns.append('63414') # Dakota Central Telecommunications
    asns.append('32809') # Dickey Rural Networks
    asns.append('14543') # SRT Communications
    asns.append('27539') # West River Telecommunications
    asns.append('18780') # Reservation Telephone
    asns.append('33339') # Nemont Telecommunications
    asns.append('36374') # Red River Communications
    asns.append('19530') # State of North Dakota
    asns.append('400439') # Consolidated Telcom
    asns.append('15267') # 702 Communications
    asns.append('21730') # Halstad Telephone Company
    asns.append('12042') # Consolidated Communications
    asns.append('11232') # Midcontinent Communications
    asns.append('55105') # Northwest Communications Cooperative

    for asn in asns:

        time.sleep(1)

        headers = {'User-Agent': 'Project Caretaker (https://github.com/jblukach/caretaker)'}
        r = requests.get('https://api.bgpview.io/asn/'+asn+'/prefixes', headers=headers)
        print('AS'+asn+' Status Code: '+str(r.status_code))
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
                        'asn': asn
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
                        'asn': asn
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