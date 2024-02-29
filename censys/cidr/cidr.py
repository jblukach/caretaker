import boto3
import ipaddress
import json
import os
from censys.search import CensysHosts

def handler(event, context):

    ssm = boto3.client('ssm')

    api = ssm.get_parameter(Name='/censys/api', WithDecryption=True)['Parameter']['Value']
    key = ssm.get_parameter(Name='/censys/key', WithDecryption=True)['Parameter']['Value']

    os.environ['CENSYS_API_ID'] = api
    os.environ['CENSYS_API_SECRET'] = key

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    h = CensysHosts()

### CableOne ###

    query = h.search(
        '(((location.province="North Dakota")) and autonomous_system.asn: {"11492"}) and services.service_name=`HTTP`',
        per_page = 100,
        pages = 150,
        fields = [
            'autonomous_system.bgp_prefix'
        ]
    )

    cidrs = []

    for page in query:
        for address in page:
            cidrs.append(address['autonomous_system']['bgp_prefix'])

    cidrs = list(set(cidrs))
    print(str(11492)+': '+str(len(cidrs)))

    for cidr in cidrs:

        hostmask = cidr.split('/')
        iptype = ipaddress.ip_address(hostmask[0])
        netrange = ipaddress.IPv4Network(cidr)
        first, last = netrange[0], netrange[-1]
        firstip = int(ipaddress.IPv4Address(first))
        lastip = int(ipaddress.IPv4Address(last))

        table.put_item(
            Item = {
                'pk': 'ASN#',
                'sk': 'ASN#IPv'+str(iptype.version)+'#'+cidr,
                'name': 'CABLEONE',
                'description': 'CABLE ONE, INC.',
                'cidr': cidr,
                'firstip': firstip,
                'lastip': lastip,
                'asn': 11492
            }
        )

### CenturyLink ###

    query = h.search(
        '(((location.province="North Dakota")) and autonomous_system.asn: {"209"}) and services.service_name=`HTTP`',
        per_page = 100,
        pages = 150,
        fields = [
            'autonomous_system.bgp_prefix'
        ]
    )

    cidrs = []

    for page in query:
        for address in page:
            cidrs.append(address['autonomous_system']['bgp_prefix'])

    cidrs = list(set(cidrs))
    print(str(209)+': '+str(len(cidrs)))

    for cidr in cidrs:

        hostmask = cidr.split('/')
        iptype = ipaddress.ip_address(hostmask[0])
        netrange = ipaddress.IPv4Network(cidr)
        first, last = netrange[0], netrange[-1]
        firstip = int(ipaddress.IPv4Address(first))
        lastip = int(ipaddress.IPv4Address(last))

        table.put_item(
            Item = {
                'pk': 'ASN#',
                'sk': 'ASN#IPv'+str(iptype.version)+'#'+cidr,
                'name': 'CenturyLink',
                'description': 'CENTURYLINK-US-LEGACY-QWEST',
                'cidr': cidr,
                'firstip': firstip,
                'lastip': lastip,
                'asn': 209
            }
        )

### VerizonBusiness ###

    query = h.search(
        '(((location.province="North Dakota")) and autonomous_system.asn: {"6167"}) and services.service_name=`HTTP`',
        per_page = 100,
        pages = 150,
        fields = [
            'autonomous_system.bgp_prefix'
        ]
    )

    cidrs = []

    for page in query:
        for address in page:
            cidrs.append(address['autonomous_system']['bgp_prefix'])

    cidrs = list(set(cidrs))
    print(str(6167)+': '+str(len(cidrs)))

    for cidr in cidrs:

        hostmask = cidr.split('/')
        iptype = ipaddress.ip_address(hostmask[0])
        netrange = ipaddress.IPv4Network(cidr)
        first, last = netrange[0], netrange[-1]
        firstip = int(ipaddress.IPv4Address(first))
        lastip = int(ipaddress.IPv4Address(last))

        table.put_item(
            Item = {
                'pk': 'ASN#',
                'sk': 'ASN#IPv'+str(iptype.version)+'#'+cidr,
                'name': 'VerizonBusiness',
                'description': 'Verizon Business',
                'cidr': cidr,
                'firstip': firstip,
                'lastip': lastip,
                'asn': 6167
            }
        )

### ATTServices ###

    query = h.search(
        '(((location.province="North Dakota")) and autonomous_system.asn: {"7018"}) and services.service_name=`HTTP`',
        per_page = 100,
        pages = 150,
        fields = [
            'autonomous_system.bgp_prefix'
        ]
    )

    cidrs = []

    for page in query:
        for address in page:
            cidrs.append(address['autonomous_system']['bgp_prefix'])

    cidrs = list(set(cidrs))
    print(str(7018)+': '+str(len(cidrs)))

    for cidr in cidrs:

        hostmask = cidr.split('/')
        iptype = ipaddress.ip_address(hostmask[0])
        netrange = ipaddress.IPv4Network(cidr)
        first, last = netrange[0], netrange[-1]
        firstip = int(ipaddress.IPv4Address(first))
        lastip = int(ipaddress.IPv4Address(last))

        table.put_item(
            Item = {
                'pk': 'ASN#',
                'sk': 'ASN#IPv'+str(iptype.version)+'#'+cidr,
                'name': 'ATTServices',
                'description': 'AT&T Services, Inc.',
                'cidr': cidr,
                'firstip': firstip,
                'lastip': lastip,
                'asn': 7018
            }
        )

### TMobile ###

    query = h.search(
        '(((location.province="North Dakota")) and autonomous_system.asn: {"21928"}) and services.service_name=`HTTP`',
        per_page = 100,
        pages = 150,
        fields = [
            'autonomous_system.bgp_prefix'
        ]
    )

    cidrs = []

    for page in query:
        for address in page:
            cidrs.append(address['autonomous_system']['bgp_prefix'])

    cidrs = list(set(cidrs))
    print(str(21928)+': '+str(len(cidrs)))

    for cidr in cidrs:

        hostmask = cidr.split('/')
        iptype = ipaddress.ip_address(hostmask[0])
        netrange = ipaddress.IPv4Network(cidr)
        first, last = netrange[0], netrange[-1]
        firstip = int(ipaddress.IPv4Address(first))
        lastip = int(ipaddress.IPv4Address(last))

        table.put_item(
            Item = {
                'pk': 'ASN#',
                'sk': 'ASN#IPv'+str(iptype.version)+'#'+cidr,
                'name': 'TMobile',
                'description': 'T-Mobile USA, Inc.',
                'cidr': cidr,
                'firstip': firstip,
                'lastip': lastip,
                'asn': 21928
            }
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Censys Hosts CIDR Search')
    }