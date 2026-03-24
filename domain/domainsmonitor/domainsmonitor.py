import boto3
import datetime
import gzip
import json
import os

def handler(event, context):

    count = 0

    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%m')
    day = datetime.datetime.now().strftime('%d')
    hour = datetime.datetime.now().strftime('%H')

    s3_client = boto3.client('s3')

    key = f'{year}-{month}-{day}-malware.csv'
    s3_client.download_file(os.environ['S3_TEMPORARY'], key, '/tmp/malware.csv')

    f = open('/tmp/malware.csv', 'r')
    data = f.read()
    f.close()

    datas = data.split('\n')

    fname = f'{year}-{month}-{day}-{hour}-domainsmonitor.csv'
    fpath = f'/tmp/{fname}'

    f = open(fpath, 'w')
    f.write('domain,attrib,ts\n')

    for data in datas:
        if data.strip() == '':
            continue
        f.write(f"{data},M,{year}-{month}-{day}-{hour}\n")
        count += 1

    f.close()

    print(f'{count} Domains')

    s3 = boto3.resource('s3')
    
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