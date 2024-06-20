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

### North Dakota ###

    query = c.search(
        'parsed.subject.province="North Dakota"',
        per_page = 100,
        pages = 400,
        fields = [
            'names',
            'labels',
            'modified_at',
            'fingerprint_sha1',
            'fingerprint_sha256',
            'parsed.issuer.organization',
            'parsed.serial_number',
            'parsed.validity_period.not_before',
            'parsed.validity_period.not_after'
        ]
    )

    northdakotacount = 0

    for page in query:
        for certificate in page:
            certificates.append(certificate)
            northdakotacount += 1
    
    print('North Dakota: ' + str(northdakotacount))

### Output ###

    with open('/tmp/certificates2.json', 'w') as outfile:
        json.dump(certificates, outfile)
    outfile.close()

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/certificates2.json',
        os.environ['S3_BUCKET'],
        'certificates2.json',
        ExtraArgs = {
            'ContentType': "application/json"
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Censys Certificates Search')
    }