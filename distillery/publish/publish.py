import boto3
import json
import os
import zipfile

def handler(event, context):

    function = boto3.client('lambda')
    s3 = boto3.client('s3')
    ssm = boto3.client('ssm')

    ### DOWNLOAD ###

    s3.download_file(
        os.environ['DNS_BUCKET'],
        'domains.txt',
        '/tmp/domains.txt'
    )

    s3.download_file(
        os.environ['IP_BUCKET'],
        'addresses.txt',
        '/tmp/addresses.txt'
    )

    s3.download_file(
        os.environ['IP_BUCKET'],
        'distillery.sqlite3',
        '/tmp/distillery.sqlite3'
    )

    ### IP ###

    files = s3.list_objects(
        Bucket = os.environ['STAGE_BUCKET'],
        Prefix = 'ip'
    )['Contents']

    for file in files:

        fname = file['Key'].split('/')[1]
        name = fname.split('.')[0]

        s3.download_file(
            os.environ['STAGE_BUCKET'],
            file['Key'],
            '/tmp/'+fname
        )

        with zipfile.ZipFile('/tmp/'+name+'.zip', 'w') as zipf:

            zipf.write('/tmp/'+fname,fname)
            zipf.write('/tmp/addresses.txt','addresses.txt')
            zipf.write('/tmp/distillery.sqlite3','distillery.sqlite3')

        s3.upload_file(
            '/tmp/'+name+'.zip',
            os.environ['STAGE_BUCKET'],
            'ipcode/'+name+'.zip'
        )

        os.remove('/tmp/'+fname)
        os.remove('/tmp/'+name+'.zip')

        value = ssm.get_parameter(
            Name = '/caretaker/ip/'+name,
        )
        print(value['Parameter']['Value'])

        function.update_function_code(
            FunctionName = value['Parameter']['Value'],
            S3Bucket = os.environ['STAGE_BUCKET'],
            S3Key = 'ipcode/'+name+'.zip'
        )

        break

    ### DNS ###

    files = s3.list_objects(
        Bucket = os.environ['STAGE_BUCKET'],
        Prefix = 'dns'
    )['Contents']

    for file in files:

        fname = file['Key'].split('/')[1]
        name = fname.split('.')[0]

        s3.download_file(
            os.environ['STAGE_BUCKET'],
            file['Key'],
            '/tmp/'+fname
        )

        with zipfile.ZipFile('/tmp/'+name+'.zip', 'w') as zipf:

            zipf.write('/tmp/'+fname,fname)
            zipf.write('/tmp/domains.txt','domains.txt')

        s3.upload_file(
            '/tmp/'+name+'.zip',
            os.environ['STAGE_BUCKET'],
            'dnscode/'+name+'.zip'
        )

        os.remove('/tmp/'+fname)
        os.remove('/tmp/'+name+'.zip')

        value = ssm.get_parameter(
            Name = '/caretaker/dns/'+name,
        )
        print(value['Parameter']['Value'])

        function.update_function_code(
            FunctionName = value['Parameter']['Value'],
            S3Bucket = os.environ['STAGE_BUCKET'],
            S3Key = 'dnscode/'+name+'.zip'
        )

        break

    return {
        'statusCode': 200,
        'body': json.dumps('Publish Distillery')
    }