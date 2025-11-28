import boto3
import json
import os
import zipfile

def handler(event, context):
    
    s3 = boto3.client('s3')

    s3.download_file(os.environ['STAGED_S3'], 'dns.py', '/tmp/dns.py')
    s3.download_file(os.environ['STAGED_S3'], 'dns.sqlite3', '/tmp/dns.sqlite3')

    with zipfile.ZipFile('/tmp/dns.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        zipf.write('/tmp/dns.py','dns.py')
        zipf.write('/tmp/dns.sqlite3','dns.sqlite3')
    zipf.close()

    s3.upload_file('/tmp/dns.zip',os.environ['STAGED_S3'],'dns.zip')

    s3.download_file(os.environ['STAGED_S3'], 'ipv4.py', '/tmp/ipv4.py')
    s3.download_file(os.environ['STAGED_S3'], 'ipv4.sqlite3', '/tmp/ipv4.sqlite3')

    with zipfile.ZipFile('/tmp/ipv4.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        zipf.write('/tmp/ipv4.py','ipv4.py')
        zipf.write('/tmp/ipv4.sqlite3','ipv4.sqlite3')
    zipf.close()

    s3.upload_file('/tmp/ipv4.zip',os.environ['STAGED_S3'],'ipv4.zip')

    s3.download_file(os.environ['STAGED_S3'], 'ipv6.py', '/tmp/ipv6.py')
    s3.download_file(os.environ['STAGED_S3'], 'ipv6.sqlite3', '/tmp/ipv6.sqlite3')

    with zipfile.ZipFile('/tmp/ipv6.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        zipf.write('/tmp/ipv6.py','ipv6.py')
        zipf.write('/tmp/ipv6.sqlite3','ipv6.sqlite3')
    zipf.close()

    s3.upload_file('/tmp/ipv6.zip',os.environ['STAGED_S3'],'ipv6.zip')

    s3.download_file(os.environ['STAGED_S3'], 'spf.py', '/tmp/spf.py')
    s3.download_file(os.environ['STAGED_S3'], 'unique_domains.csv', '/tmp/unique_domains.csv')
    s3.download_file(os.environ['STAGED_S3'], 'unique_ipv4s.csv', '/tmp/unique_ipv4s.csv')
    s3.download_file(os.environ['STAGED_S3'], 'unique_ipv6s.csv', '/tmp/unique_ipv6s.csv')

    with zipfile.ZipFile('/tmp/spf.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        zipf.write('/tmp/spf.py','spf.py')
        zipf.write('/tmp/unique_domains.csv','unique_domains.csv')
        zipf.write('/tmp/unique_ipv4s.csv','unique_ipv4s.csv')
        zipf.write('/tmp/unique_ipv6s.csv','unique_ipv6s.csv')
    zipf.close()

    s3.upload_file('/tmp/spf.zip',os.environ['STAGED_S3'],'spf.zip')

    s3.download_file(os.environ['STAGED_S3'], 'verify.py', '/tmp/verify.py')
    s3.download_file(os.environ['STAGED_S3'], 'verify.sqlite3', '/tmp/verify.sqlite3')

    with zipfile.ZipFile('/tmp/verify.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        zipf.write('/tmp/verify.py','verify.py')
        zipf.write('/tmp/verify.sqlite3','verify.sqlite3')
    zipf.close()
    
    s3.upload_file('/tmp/verify.zip',os.environ['STAGED_S3'],'verify.zip')
    
    client = boto3.client('lambda')

    client.update_function_code(
        FunctionName = 'dns',
        S3Bucket = os.environ['STAGED_S3'],
        S3Key = 'dns.zip'
    )

    client.update_function_code(
        FunctionName = 'ipv4',
        S3Bucket = os.environ['STAGED_S3'],
        S3Key = 'ipv4.zip'
    )

    client.update_function_code(
        FunctionName = 'ipv6',
        S3Bucket = os.environ['STAGED_S3'],
        S3Key = 'ipv6.zip'
    )

    client.update_function_code(
        FunctionName = 'spf',
        S3Bucket = os.environ['STAGED_S3'],
        S3Key = 'spf.zip'
    )

    client.update_function_code(
        FunctionName = 'verify',
        S3Bucket = os.environ['STAGED_S3'],
        S3Key = 'verify.zip'
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Completed!')
    }