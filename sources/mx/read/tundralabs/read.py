import boto3
import datetime
import dns.resolver
import json
import time
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from smart_open import open

def dateconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def handler(event, context):

    bucket = event['event']['bucket']
    key = event['event']['key']
    state = event['event']['state']
    table = event['event']['table']
    offset = event['event']['offset']
    transitions = event['event']['transitions']

    dynamodb = boto3.resource('dynamodb')
    feed = dynamodb.Table(table)

    now = datetime.datetime.now()
    epoch = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    ttl = epoch+2592000 # plus 30 days
    seen = json.dumps(now, default=dateconverter)
    seen = seen.replace('"','')

    limit = 'NO'

    with open('s3://'+bucket+'/'+key, 'rb') as f:
        f.seek(offset)
        line = f.readline()
    f.close()

    offset = offset + len(line)
    output = line[:-1].decode()
    transitions += 1

    try:

        answers = dns.resolver.query(output, 'MX')
        mx_records = [str(rdata.exchange) for rdata in answers]

        if len(mx_records) != 0:

            try:
                spf = 'NO'
                answers = dns.resolver.query(output, 'TXT')
                for rdata in answers:
                    if 'v=spf1' in str(rdata):
                        spf = 'YES'

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

                        headers = {'User-Agent': 'Project Caretaker (https://github.com/jblukach/caretaker)'}
                        response = http.get('https://spf.tundralabs.net/'+output, headers=headers)

                        data = response.text
                        data = json.loads(data)

                        count = data['suspect_dns'] + data['suspect_ipv4'] + data['suspect_ipv6']
                        if count > 0:
                            feed.put_item(
                                Item = {
                                    'pk': 'DNS#',
                                    'sk': 'DNS#'+str(output)+'#SOURCE#suspect.spf.tundralabs.org',
                                    'dns': str(output),
                                    'source': 'suspect.spf.tundralabs.org',
                                    'last': seen,
                                    'epoch': epoch,
                                    'ttl': ttl
                                }
                            )
                        time.sleep(1)
            except:
                spf = 'NO'
                pass

            if spf == 'NO':
                feed.put_item(
                    Item = {
                        'pk': 'DNS#',
                        'sk': 'DNS#'+str(output)+'#SOURCE#no.spf.tundralabs.org',
                        'dns': str(output),
                        'source': 'no.spf.tundralabs.org',
                        'last': seen,
                        'epoch': epoch,
                        'ttl': ttl
                    }
                )

            try:
                dmarc = 'NO'
                answers = dns.resolver.query('_dmarc.' + output, 'TXT')
                for rdata in answers:
                    if 'v=DMARC1' in str(rdata):
                        dmarc = 'YES'
            except:
                dmarc = 'NO'
                pass

            if dmarc == 'NO':
                feed.put_item(
                    Item = {
                        'pk': 'DNS#',
                        'sk': 'DNS#'+str(output)+'#SOURCE#no.dmarc.tundralabs.org',
                        'dns': str(output),
                        'source': 'no.dmarc.tundralabs.org',
                        'last': seen,
                        'epoch': epoch,
                        'ttl': ttl
                    }
                )

    except:
        pass

    if len(line) > 0:
        status = 'CONTINUE'
    else:
        status = 'SUCCEEDED'

    if transitions == 2500:
        limit = 'YES'
        transitions = 0

    getobject = {}
    getobject['bucket'] = bucket
    getobject['key'] = key
    getobject['state'] = state
    getobject['table'] = table
    getobject['offset'] = offset
    getobject['transitions'] = transitions

    if limit == 'YES':

        step = boto3.client('stepfunctions')

        step.start_execution(
            stateMachineArn = state,
            input = json.dumps(getobject),
        )

        status = 'SUCCEEDED'

    return {
        'event': getobject,
        'status': status,
    }