import boto3
import datetime
import gzip
import json
import os
import requests

def handler(event, context):

    count = 0

    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%m')
    day = datetime.datetime.now().strftime('%d')

    feeds = []
    feeds.append('https://iplists.firehol.org/files/firehol_abusers_1d.netset')
    feeds.append('https://iplists.firehol.org/files/firehol_anonymous.netset')
    feeds.append('https://iplists.firehol.org/files/firehol_level1.netset')
    feeds.append('https://iplists.firehol.org/files/firehol_level2.netset')
    feeds.append('https://iplists.firehol.org/files/firehol_level3.netset')
    feeds.append('https://iplists.firehol.org/files/firehol_level4.netset')
    feeds.append('https://iplists.firehol.org/files/firehol_proxies.netset')
    feeds.append('https://iplists.firehol.org/files/firehol_webserver.netset')

    fname = f'{year}-{month}-{day}-firehol.csv'
    fpath = f'/tmp/{fname}'

    addresses = []

    for feed in feeds:

        headers = {'User-Agent': 'Project Caretaker (https://github.com/jblukach/caretaker)'}
        response = requests.get(feed, headers=headers)
        print(f'HTTP Status Code: {response.status_code}')
        data = response.text

        for line in data.splitlines():
            if line.startswith('#'):
                continue
            else:
                addresses.append(f"{line},10,{year}-{month}-{day}\n")
                count += 1

    addresses = list(set(addresses))

    f = open(fpath, 'w')
    f.write('address,attrib,ts\n')

    for address in addresses:
        f.write(address)

    f.close()

    print(f'{count} Addresses')
    print(f'{len(addresses)} Unique')

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        fpath,
        os.environ['S3_BUCKET'],
        'ips/'+fname,
        ExtraArgs = {
            'ContentType': "text/csv"
        }
    )
    
    with open(fpath, 'rb') as f_in:
        with gzip.open(fpath + '.gz', 'wb') as f_out:
            f_out.writelines(f_in)

    s3.meta.client.upload_file(
        fpath + '.gz',
        os.environ['S3_RESEARCH'],
        'ips/'+fname+'.gz',
        ExtraArgs = {
            'ContentType': "application/gzip"
        }
    )

    os.system('ls -lh /tmp')

    return {
        'statusCode': 200,
        'body': json.dumps('Completed!')
    }