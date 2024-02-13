import boto3
import json
import os
from censys.search import CensysHosts

def handler(event, context):

    ssm = boto3.client('ssm')

    api = ssm.get_parameter(Name='/censys/api', WithDecryption=True)['Parameter']['Value']
    key = ssm.get_parameter(Name='/censys/key', WithDecryption=True)['Parameter']['Value']

    os.environ['CENSYS_API_ID'] = api
    os.environ['CENSYS_API_SECRET'] = key

    h = CensysHosts()

    dns = []
    ips = []

### SMTP SERVICE ###

    query = h.search(
        '(location.province="North Dakota") and services.service_name=`SMTP`',
        per_page = 100,
        pages = 50,
        fields = [
            'dns.names',
            'ip'
        ]
    )

    for page in query:
        for address in page:
            ips.append(address['ip'])
            for name in address['dns']['names']:
                domain = name.split('.')
                if len(domain) > 2:
                    dns.append(domain[-2]+'.'+domain[-1])
                else:
                    dns.append(name)

### EMAIL LABEL ###

    query = h.search(
        '(location.province="North Dakota") and labels=`email`',
        per_page = 100,
        pages = 50,
        fields = [
            'dns.names',
            'ip'
        ]
    )

    for page in query:
        for address in page:
            ips.append(address['ip'])
            for name in address['dns']['names']:
                domain = name.split('.')
                if len(domain) > 2:
                    dns.append(domain[-2]+'.'+domain[-1])
                else:
                    dns.append(name)

    ### HOTEL DOMAINS ###

    count = 0
    s3 = boto3.client('s3')
    s3.download_file(os.environ['S3_CERTS'], 'hotels.txt', '/tmp/hotels.txt')

    with open('/tmp/hotels.txt') as f:
        for line in f:
            if line.startswith('www.'):
                continue
            else:
                dns.append(line.strip())
                count += 1
    f.close()

    print('Hotels: '+str(count))

### WRITE FILES ###

    dns = list(set(dns))
    ips = list(set(ips))
    
    print('DNS: '+str(len(dns)))
    print('IPs: '+str(len(ips)))

    with open('/tmp/dns.txt', 'w') as f:
        for item in dns:
            f.write("%s\n" % item)
    f.close()

    with open('/tmp/ips.txt', 'w') as f:
        for item in ips:
            f.write("%s\n" % item)
    f.close()

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/dns.txt',
        os.environ['S3_BUCKET'],
        'dns.txt',
        ExtraArgs = {
            'ContentType': "text/plain"
        }
    )

    s3.meta.client.upload_file(
        '/tmp/ips.txt',
        os.environ['S3_BUCKET'],
        'ips.txt',
        ExtraArgs = {
            'ContentType': "text/plain"
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Censys Hosts Email Search')
    }