import boto3
import datetime
import json
import os
from censys.search import CensysHosts

def dateconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def handler(event, context):

    ssm = boto3.client('ssm')

    api = ssm.get_parameter(Name='/censys/api', WithDecryption=True)['Parameter']['Value']
    key = ssm.get_parameter(Name='/censys/key', WithDecryption=True)['Parameter']['Value']

    os.environ['CENSYS_API_ID'] = api
    os.environ['CENSYS_API_SECRET'] = key
    service = os.environ['CENSYS_SERVICE']

    h = CensysHosts()

    if service != 'CWMP' and service != 'SNMP':

        query = h.search(
            '(autonomous_system.asn: {"14090","29744","14511","31758","26794","11138","63414","32809","14543","27539","18780","33339","36374","19530","400439","15267","21730","12042","55105","11232"}) and services.service_name=`'+service+'`',
            per_page = 100,
            pages = 50,
            fields = [
                'ip'
            ]
        )

    else:

        query = h.search(
            '(autonomous_system.asn: {"14090","29744","14511","31758","26794","11138","63414","32809","14543","27539","18780","33339","36374","19530","400439","15267","21730","12042","55105"}) and services.service_name=`'+service+'`',
            per_page = 100,
            pages = 50,
            fields = [
                'ip'
            ]
        )

    dynamodb = boto3.resource('dynamodb')
    verify = dynamodb.Table('verify')

    now = datetime.datetime.now()
    orig = datetime.datetime.utcfromtimestamp(0)
    epoch = int((now - orig).total_seconds() * 1000.0)
    seen = json.dumps(now, default=dateconverter)
    seen = seen.replace('"','')

    for page in query:
        for address in page:
            verify.put_item(
                Item = {
                    'pk': 'IP#',
                    'sk': 'IP#'+str(address['ip'])+'#SOURCE#'+service+'-censys.io',
                    'ip': str(address['ip']),
                    'source': service+'-censys.io',
                    'last': seen,
                    'epoch': epoch
                }
            )

    query = h.search(
        '(((location.province="North Dakota")) and autonomous_system.asn: {"209","11492"}) and services.service_name=`'+service+'`',
        per_page = 100,
        pages = 50,
        fields = [
            'ip'
        ]
    )

    for page in query:
        for address in page:
            verify.put_item(
                Item = {
                    'pk': 'IP#',
                    'sk': 'IP#'+str(address['ip'])+'#SOURCE#'+service+'-censys.io',
                    'ip': str(address['ip']),
                    'source': service+'-censys.io',
                    'last': seen,
                    'epoch': epoch
                }
            )

    return {
        'statusCode': 200,
        'body': json.dumps('Censys Hosts Service Search')
    }