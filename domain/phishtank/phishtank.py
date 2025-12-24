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
    hour = datetime.datetime.now().strftime('%H')

    headers = {'User-Agent': 'Project Caretaker (https://github.com/jblukach/caretaker)'}
    response = requests.get('http://data.phishtank.com/data/online-valid.csv', headers=headers)
    print(f'HTTP Status Code: {response.status_code}')
    data = response.text

    fname = f'{year}-{month}-{day}-{hour}-phishtank.csv'
    fpath = f'/tmp/{fname}'

    domains = []

    for line in data.splitlines(True)[1:]:
        if line.startswith('#'):
            continue
        else:
            line = line.split(',')[1]
            line = line.split('/')[2]
            domains.append(f"{line},H,{year}-{month}-{day}-{hour}\n")
            count += 1

    domains = list(set(domains))

    f = open(fpath, 'w')
    f.write('domain,attrib,ts\n')

    for domain in domains:
        f.write(domain)

    f.close()

    print(f'{count} Domains')
    print(f'{len(domains)} Domains')

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        fpath,
        os.environ['S3_BUCKET'],
        'dns/'+fname,
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
        'dns/'+fname+'.gz',
        ExtraArgs = {
            'ContentType': "application/gzip"
        }
    )

    os.system('ls -lh /tmp')

    return {
        'statusCode': 200,
        'body': json.dumps('Completed!')
    }