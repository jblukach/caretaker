import boto3
import json
import os
from censys.search import CensysCerts

def handler(event, context):

    ssm = boto3.client('ssm')

    api = ssm.get_parameter(Name='/censys/api', WithDecryption=True)['Parameter']['Value']
    key = ssm.get_parameter(Name='/censys/key', WithDecryption=True)['Parameter']['Value']

    os.environ['CENSYS_API_ID'] = api
    os.environ['CENSYS_API_SECRET'] = key

    certificates = []

    c = CensysCerts()

### ND ###

    query = c.search(
        '((parsed.subject.province="North Dakota") or parsed.subject.province="ND") and labels=`trusted`',
        per_page = 100,
        pages = 100,
        fields = [
            'names'
        ]
    )

    ndcount = 0
    nderror = 0

    for page in query:
        for certificate in page:
            try:
                certificates.append(certificate)
                ndcount += 1
            except Exception as e:
                print(e)
                print(certificate)
                nderror += 1

    print('ND: ' + str(ndcount))
    print('ERROR: ' + str(nderror))

### Output ###

    with open('/tmp/certificates.json', 'w') as outfile:
        json.dump(certificates, outfile)
    outfile.close()

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/certificates.json',
        os.environ['S3_BUCKET'],
        'certificates.json',
        ExtraArgs = {
            'ContentType': "application/json"
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Censys Certificates Search')
    }