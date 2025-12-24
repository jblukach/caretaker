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
    response = requests.get('https://raw.githubusercontent.com/elliotwutingfeng/Inversion-DNSBL-Blocklists/main/Google_ipv4.txt', headers=headers)
    print(f'HTTP Status Code: {response.status_code}')
    data = response.text

    fname = f'{year}-{month}-{day}-{hour}-inversiondnsbl.csv'
    fpath = f'/tmp/{fname}'

    f = open(fpath, 'w')
    f.write('address,attrib,ts\n')

    for line in data.splitlines():
        if line.startswith('#'):
            continue
        else:
            f.write(f"{line},13,{year}-{month}-{day}-{hour}\n")
            count += 1

    f.close()

    print(f'{count} Addresses')

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