import boto3
import datetime
import dns.resolver
import json
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
    orig = datetime.datetime.utcfromtimestamp(0)
    epoch = int((now - orig).total_seconds() * 1000.0)
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
                        'epoch': epoch
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
                        'epoch': epoch
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