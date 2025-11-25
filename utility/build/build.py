import boto3
import json
import os

def handler(event, context):

    domains = []
    ipv4s = []
    ipv6s = []

    s3 = boto3.client('s3')

    objects = s3.list_objects(
        Bucket = os.environ['S3_BUCKET'],
        Prefix = 'ips'
    )

    for key in objects['Contents']:

        s3.download_file(os.environ['S3_BUCKET'], key['Key'], '/tmp/'+key['Key'].split('/')[-1])

        with open('/tmp/'+key['Key'].split('/')[-1], 'r') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split(',')
                if parts[0] != 'address':
                    if '.' in parts[0]:
                        ipv4s.append(str(parts[0])+','+str(parts[1]))
                    if ':' in parts[0]:
                        ipv6s.append(str(parts[0])+','+str(parts[1]))
        f.close()

    print(f'IPv4s: {len(ipv4s)}')
    ipv4s = list(set(ipv4s))
    print(f'Deduplicated: {len(ipv4s)}')

    print(f'IPv6s: {len(ipv6s)}')
    ipv6s = list(set(ipv6s))
    print(f'Deduplicated: {len(ipv6s)}')

    objects = s3.list_objects(
        Bucket = os.environ['S3_BUCKET'],
        Prefix = 'dns'
    )

    for key in objects['Contents']:

        s3.download_file(os.environ['S3_BUCKET'], key['Key'], '/tmp/'+key['Key'].split('/')[-1])

        with open('/tmp/'+key['Key'].split('/')[-1], 'r') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split(',')
                if parts[0] != 'domain' and '.' in parts[0]:
                    domains.append(str(parts[0])+','+str(parts[1]))
        f.close()

    print(f'Domains: {len(domains)}')
    domains = list(set(domains))
    print(f'Deduplicated: {len(domains)}')

    with open('/tmp/domains.csv','w') as f:
        for domain in domains:
            f.write(domain+'\n')
    f.close()

    with open('/tmp/ipv4s.csv','w') as f:
        for ipv4 in ipv4s:
            f.write(ipv4+'\n')
    f.close()

    with open('/tmp/ipv6s.csv','w') as f:
        for ipv6 in ipv6s:
            f.write(ipv6+'\n')
    f.close()

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/domains.csv',
        os.environ['STAGED_S3'],
        'domains.csv',
        ExtraArgs = {
            'ContentType': "text/csv"
        }
    )

    s3.meta.client.upload_file(
        '/tmp/ipv4s.csv',
        os.environ['STAGED_S3'],
        'ipv4s.csv',
        ExtraArgs = {
            'ContentType': "text/csv"
        }
    )

    s3.meta.client.upload_file(
        '/tmp/ipv6s.csv',
        os.environ['STAGED_S3'],
        'ipv6s.csv',
        ExtraArgs = {
            'ContentType': "text/csv"
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Completed!')
    }