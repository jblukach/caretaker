import boto3
import json
import os
import zipfile

def handler(event, context):
    
    s3 = boto3.client('s3')

    print("Downloading dns.py and dns.sqlite3")

    s3.download_file(os.environ['STAGED_S3'], 'dns.py', '/tmp/dns.py')
    s3.download_file(os.environ['STAGED_S3'], 'dns.sqlite3', '/tmp/dns.sqlite3')

    print("Packaging dns.zip")

    with zipfile.ZipFile('/tmp/dns.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        zipf.write('/tmp/dns.py','dns.py')
        zipf.write('/tmp/dns.sqlite3','dns.sqlite3')
    zipf.close()

    print("Uploading dns.zip")

    s3.upload_file('/tmp/dns.zip',os.environ['STAGED_S3'],'dns.zip')
    s3.upload_file('/tmp/dns.zip',os.environ['STAGED_S3_USE1'],'dns.zip')
    s3.upload_file('/tmp/dns.zip',os.environ['STAGED_S3_USW2'],'dns.zip')

    print("Downloading ip.py and ip.sqlite3")

    s3.download_file(os.environ['STAGED_S3'], 'ip.py', '/tmp/ip.py')
    s3.download_file(os.environ['STAGED_S3'], 'ip.sqlite3', '/tmp/ip.sqlite3')

    print("Packaging ip.zip")

    with zipfile.ZipFile('/tmp/ip.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        zipf.write('/tmp/ip.py','ip.py')
        zipf.write('/tmp/ip.sqlite3','ip.sqlite3')
    zipf.close()

    print("Uploading ip.zip")

    s3.upload_file('/tmp/ip.zip',os.environ['STAGED_S3'],'ip.zip')
    s3.upload_file('/tmp/ip.zip',os.environ['STAGED_S3_USE1'],'ip.zip')
    s3.upload_file('/tmp/ip.zip',os.environ['STAGED_S3_USW2'],'ip.zip')
    
    client = boto3.client('lambda', region_name = 'us-east-1')

    print("Updating "+os.environ['LAMBDA_DNS_USE1'])

    response = client.update_function_code(
        FunctionName = os.environ['LAMBDA_DNS_USE1'],
        S3Bucket = os.environ['STAGED_S3_USE1'],
        S3Key = 'dns.zip'
    )

    print("Updating "+os.environ['LAMBDA_IP_USE1'])

    response = client.update_function_code(
        FunctionName = os.environ['LAMBDA_IP_USE1'],
        S3Bucket = os.environ['STAGED_S3_USE1'],
        S3Key = 'ip.zip'
    )

    client = boto3.client('lambda', region_name = 'us-west-2')

    print("Updating "+os.environ['LAMBDA_DNS_USW2'])

    response = client.update_function_code(
        FunctionName = os.environ['LAMBDA_DNS_USW2'],
        S3Bucket = os.environ['STAGED_S3_USW2'],
        S3Key = 'dns.zip'
    )

    print("Updating "+os.environ['LAMBDA_IP_USW2'])

    response = client.update_function_code(
        FunctionName = os.environ['LAMBDA_IP_USW2'],
        S3Bucket = os.environ['STAGED_S3_USW2'],
        S3Key = 'ip.zip'
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Completed!')
    }