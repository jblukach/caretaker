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
        'parsed.subject.province="ND"',
        per_page = 100,
        pages = 50,
        fields = [
            'names',
            'fingerprint_sha1'
        ]
    )

    for page in query:
        for certificate in page:
            certificates.append(certificate)

### North Dakota ###

    query = c.search(
        'parsed.subject.province="North Dakota"',
        per_page = 100,
        pages = 300,
        fields = [
            'names',
            'fingerprint_sha1'
        ]
    )

    for page in query:
        for certificate in page:
            certificates.append(certificate)

### Output ###

    with open('/tmp/certificates.json', 'w') as outfile:
        json.dump(certificates, outfile)

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