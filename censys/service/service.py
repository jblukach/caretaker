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

    if service != 'CWMP':

        query = h.search(
            '(autonomous_system.asn: {"14090","29744","14511","31758","26794","11138","63414","32809","14543","27539","18780","33339","36374","19530","15267","21730","55105","400439","11232"}) and services.service_name=`'+service+'`',
            per_page = 100,
            pages = 100,
            fields = [
                'ip'
            ]
        )

    else:

        query = h.search(
            '(autonomous_system.asn: {"14090","29744","14511","31758","26794","11138","63414","32809","14543","27539","18780","33339","36374","19530","15267","21730","55105","400439"}) and services.service_name=`'+service+'`',
            per_page = 100,
            pages = 100,
            fields = [
                'ip'
            ]
        )

    dynamodb = boto3.resource('dynamodb')
    verify = dynamodb.Table('verify')

    now = datetime.datetime.now()
    epoch = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    seen = json.dumps(now, default=dateconverter)
    seen = seen.replace('"','')

    primarycount = 0
    errorcount = 0

    for page in query:
        for address in page:
            try:
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
                primarycount += 1
            except Exception as e:
                print(e)
                print(address)
                errorcount += 1

    print(service + ': ' + str(primarycount))
    print('error: '+service + ': ' + str(errorcount))

    return {
        'statusCode': 200,
        'body': json.dumps('Censys Hosts Service Search')
    }