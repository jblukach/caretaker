import boto3
import datetime
import geoip2.database
import json
import os
import sqlite3
import zipfile

def handler(event, context):

    s3_client = boto3.client('s3')

    print("Copying asn.updated")

    with open('/tmp/asn.updated', 'wb') as f:
        s3_client.download_fileobj(os.environ['STAGED_GEO'], 'asn.updated', f) 
    f.close()

    print("Copying city.updated")

    with open('/tmp/city.updated', 'wb') as f:
        s3_client.download_fileobj(os.environ['STAGED_GEO'], 'city.updated', f) 
    f.close()

    print("Copying GeoLite2-ASN.mmdb")

    with open('/tmp/GeoLite2-ASN.mmdb', 'wb') as f:
        s3_client.download_fileobj(os.environ['STAGED_GEO'], 'GeoLite2-ASN.mmdb', f) 
    f.close()

    print("Copying GeoLite2-City.mmdb")

    with open('/tmp/GeoLite2-City.mmdb', 'wb') as f:
        s3_client.download_fileobj(os.environ['STAGED_GEO'], 'GeoLite2-City.mmdb', f) 
    f.close()

    print("Copying asn.py")

    with open('/tmp/asn.py', 'wb') as f:
        s3_client.download_fileobj(os.environ['STAGED_S3'], 'asn.py', f)
    f.close()

    print("Copying co.py")

    with open('/tmp/co.py', 'wb') as f:
        s3_client.download_fileobj(os.environ['STAGED_S3'], 'co.py', f)
    f.close()

    print("Copying st.py")

    with open('/tmp/st.py', 'wb') as f:
        s3_client.download_fileobj(os.environ['STAGED_S3'], 'st.py', f)
    f.close()

    print("Copying unique_ipv4s.csv")

    with open('/tmp/unique_ipv4s.csv', 'wb') as f:
        s3_client.download_fileobj(os.environ['STAGED_S3'], 'unique_ipv4s.csv', f) 
    f.close()

    print("Reading unique_ipv4s.csv")

    with open('/tmp/unique_ipv4s.csv', 'r') as f:
        ipv4s = f.read().splitlines()
    f.close()

    print("Total unique IPv4s: {}".format(len(ipv4s)))

    print("Copying unique_ipv6s.csv")

    with open('/tmp/unique_ipv6s.csv', 'wb') as f:
        s3_client.download_fileobj(os.environ['STAGED_S3'], 'unique_ipv6s.csv', f) 
    f.close()

    print("Reading unique_ipv6s.csv")

    with open('/tmp/unique_ipv6s.csv', 'r') as f:
        ipv6s = f.read().splitlines()
    f.close()

    print("Total unique IPv6s: {}".format(len(ipv6s)))

    print("Starting GeoLite2 lookups")

    asn = []
    co = []
    st = []

    with geoip2.database.Reader('/tmp/GeoLite2-ASN.mmdb') as reader2:
        with geoip2.database.Reader('/tmp/GeoLite2-City.mmdb') as reader:
    
            for ip in ipv4s + ipv6s:
    
                try:
                    response = reader.city(ip)
                    country = response.country.iso_code
                    if country is None:
                        country = 'UNKN'
                    state = response.subdivisions.most_specific.iso_code
                    if state is None:
                        state = 'UNKN'
                except:
                    country = 'UNKN'
                    state = 'UNKN'

                try:
                    response2 = reader2.asn(ip)
                    id = response2.autonomous_system_number
                    if id is None:
                        id = 'UNKN'
                except:
                    id = 'UNKN'

                asn.append(str(id)+','+ip)
                co.append(country+','+ip)
                if country == 'US':
                    st.append(state+','+ip)

    print("Deduplicating data")

    asn = list(set(asn))
    co = list(set(co))
    st = list(set(st))

    print("Sorting data")

    asn.sort()
    co.sort()
    st.sort()

    print(f'ASN Data: {len(asn)} entries')
    print(f'Country Data: {len(co)} entries')
    print(f'State Data: {len(st)} entries')

    print("Writing CSVs to /tmp/")

    with open('/tmp/asn.csv','w') as f:
        for line in asn:
            f.write(line+'\n')
    f.close()

    with open('/tmp/co.csv','w') as f:
        for line in co:
            f.write(line+'\n')
    f.close()

    with open('/tmp/st.csv','w') as f:
        for line in st:
            f.write(line+'\n')
    f.close()

    print("Uploading CSVs to S3")

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/asn.csv',
        os.environ['STAGED_S3'],
        'asn.csv',
        ExtraArgs = {
            'ContentType': "text/csv"
        }
    )

    s3.meta.client.upload_file(
        '/tmp/co.csv',
        os.environ['STAGED_S3'],
        'co.csv',
        ExtraArgs = {
            'ContentType': "text/csv"
        }
    )
 
    s3.meta.client.upload_file(
        '/tmp/st.csv',
        os.environ['STAGED_S3'],
        'st.csv',
        ExtraArgs = {
            'ContentType': "text/csv"
        }
    )

    print("Building SQLite database")

    now = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')

    if os.path.exists('/tmp/asn.sqlite3'):
        os.remove('/tmp/asn.sqlite3')

    asn = sqlite3.connect('/tmp/asn.sqlite3')
    asn.execute('CREATE TABLE IF NOT EXISTS asn (pk INTEGER PRIMARY KEY, asnid TEXT, artifact TEXT)')
    asn.execute('CREATE INDEX asn_index ON asn (asnid)')
    asn.execute('CREATE TABLE IF NOT EXISTS org (pk INTEGER PRIMARY KEY, updated TEXT)')
    asn.execute('CREATE TABLE IF NOT EXISTS city (pk INTEGER PRIMARY KEY, updated TEXT)')
    asn.execute('CREATE TABLE IF NOT EXISTS last (pk INTEGER PRIMARY KEY, updated TEXT)')
    asn.execute('INSERT INTO last (updated) VALUES (?)', (now,))

    if os.path.exists('/tmp/co.sqlite3'):
        os.remove('/tmp/co.sqlite3')

    co = sqlite3.connect('/tmp/co.sqlite3')
    co.execute('CREATE TABLE IF NOT EXISTS co (pk INTEGER PRIMARY KEY, coid TEXT, artifact TEXT)')
    co.execute('CREATE INDEX co_index ON co (coid)')
    co.execute('CREATE TABLE IF NOT EXISTS org (pk INTEGER PRIMARY KEY, updated TEXT)')
    co.execute('CREATE TABLE IF NOT EXISTS city (pk INTEGER PRIMARY KEY, updated TEXT)')
    co.execute('CREATE TABLE IF NOT EXISTS last (pk INTEGER PRIMARY KEY, updated TEXT)')
    co.execute('INSERT INTO last (updated) VALUES (?)', (now,))

    if os.path.exists('/tmp/st.sqlite3'):
        os.remove('/tmp/st.sqlite3')

    st = sqlite3.connect('/tmp/st.sqlite3')
    st.execute('CREATE TABLE IF NOT EXISTS st (pk INTEGER PRIMARY KEY, stid TEXT, artifact TEXT)')
    st.execute('CREATE INDEX st_index ON st (stid)')
    st.execute('CREATE TABLE IF NOT EXISTS org (pk INTEGER PRIMARY KEY, updated TEXT)')
    st.execute('CREATE TABLE IF NOT EXISTS city (pk INTEGER PRIMARY KEY, updated TEXT)')
    st.execute('CREATE TABLE IF NOT EXISTS last (pk INTEGER PRIMARY KEY, updated TEXT)')
    st.execute('INSERT INTO last (updated) VALUES (?)', (now,))

    with open('/tmp/asn.updated', 'r') as f:
        updated = f.read().strip()
    f.close()
    asn.execute('INSERT INTO org (updated) VALUES (?)', (updated,))
    co.execute('INSERT INTO org (updated) VALUES (?)', (updated,))
    st.execute('INSERT INTO org (updated) VALUES (?)', (updated,))

    with open('/tmp/city.updated', 'r') as f:
        updated = f.read().strip()
    f.close()
    asn.execute('INSERT INTO city (updated) VALUES (?)', (updated,))
    co.execute('INSERT INTO city (updated) VALUES (?)', (updated,))
    st.execute('INSERT INTO city (updated) VALUES (?)', (updated,))

    with open('/tmp/asn.csv', 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            asn.execute('INSERT INTO asn (asnid, artifact) VALUES (?, ?)', (parts[0], parts[1]))
    f.close()

    with open('/tmp/co.csv', 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            co.execute('INSERT INTO co (coid, artifact) VALUES (?, ?)', (parts[0], parts[1]))
    f.close()

    with open('/tmp/st.csv', 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            st.execute('INSERT INTO st (stid, artifact) VALUES (?, ?)', (parts[0], parts[1]))
    f.close()

    asn.commit()
    asn.close()
    co.commit()
    co.close()
    st.commit()
    st.close()

    print("Uploading SQLite databases to S3")

    s3.meta.client.upload_file(
        '/tmp/asn.sqlite3',
        os.environ['STAGED_S3'],
        'asn.sqlite3',
        ExtraArgs = {
            'ContentType': "application/x-sqlite3"
        }
    )

    s3.meta.client.upload_file(
        '/tmp/co.sqlite3',
        os.environ['STAGED_S3'],
        'co.sqlite3',
        ExtraArgs = {
            'ContentType': "application/x-sqlite3"
        }
    )

    s3.meta.client.upload_file(
        '/tmp/st.sqlite3',
        os.environ['STAGED_S3'],
        'st.sqlite3',
        ExtraArgs = {
            'ContentType': "application/x-sqlite3"
        }
    )

    print("Packaging asn.zip")

    with zipfile.ZipFile('/tmp/asn.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        zipf.write('/tmp/asn.py','asn.py')
        zipf.write('/tmp/asn.sqlite3','asn.sqlite3')
    zipf.close()

    print("Packaging co.zip")

    with zipfile.ZipFile('/tmp/co.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        zipf.write('/tmp/co.py','co.py')
        zipf.write('/tmp/co.sqlite3','co.sqlite3')
    zipf.close()

    print("Packaging st.zip")

    with zipfile.ZipFile('/tmp/st.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        zipf.write('/tmp/st.py','st.py')
        zipf.write('/tmp/st.sqlite3','st.sqlite3')
    zipf.close()

    print("Uploading asn.zip")

    s3_client.upload_file('/tmp/asn.zip',os.environ['STAGED_S3'],'asn.zip')
    s3_client.upload_file('/tmp/asn.zip',os.environ['STAGED_S3_USE1'],'asn.zip')
    s3_client.upload_file('/tmp/asn.zip',os.environ['STAGED_S3_USW2'],'asn.zip')

    print("Uploading co.zip")

    s3_client.upload_file('/tmp/co.zip',os.environ['STAGED_S3'],'co.zip')
    s3_client.upload_file('/tmp/co.zip',os.environ['STAGED_S3_USE1'],'co.zip')
    s3_client.upload_file('/tmp/co.zip',os.environ['STAGED_S3_USW2'],'co.zip')

    print("Uploading st.zip")

    s3_client.upload_file('/tmp/st.zip',os.environ['STAGED_S3'],'st.zip')
    s3_client.upload_file('/tmp/st.zip',os.environ['STAGED_S3_USE1'],'st.zip')
    s3_client.upload_file('/tmp/st.zip',os.environ['STAGED_S3_USW2'],'st.zip')

    client = boto3.client('lambda', region_name = 'us-east-1')

    print("Updating "+os.environ['LAMBDA_ASN_USE1'])

    response = client.update_function_code(
        FunctionName = os.environ['LAMBDA_ASN_USE1'],
        S3Bucket = os.environ['STAGED_S3_USE1'],
        S3Key = 'asn.zip'
    )

    print("Updating "+os.environ['LAMBDA_CO_USE1'])

    response = client.update_function_code(
        FunctionName = os.environ['LAMBDA_CO_USE1'],
        S3Bucket = os.environ['STAGED_S3_USE1'],
        S3Key = 'co.zip'
    )

    print("Updating "+os.environ['LAMBDA_ST_USE1'])

    response = client.update_function_code(
        FunctionName = os.environ['LAMBDA_ST_USE1'],
        S3Bucket = os.environ['STAGED_S3_USE1'],
        S3Key = 'st.zip'
    )

    client = boto3.client('lambda', region_name = 'us-west-2')

    print("Updating "+os.environ['LAMBDA_ASN_USW2'])

    response = client.update_function_code(
        FunctionName = os.environ['LAMBDA_ASN_USW2'],
        S3Bucket = os.environ['STAGED_S3_USW2'],
        S3Key = 'asn.zip'
    )

    print("Updating "+os.environ['LAMBDA_CO_USW2'])

    response = client.update_function_code(
        FunctionName = os.environ['LAMBDA_CO_USW2'],
        S3Bucket = os.environ['STAGED_S3_USW2'],
        S3Key = 'co.zip'
    )

    print("Updating "+os.environ['LAMBDA_ST_USW2'])

    response = client.update_function_code(
        FunctionName = os.environ['LAMBDA_ST_USW2'],
        S3Bucket = os.environ['STAGED_S3_USW2'],
        S3Key = 'st.zip'
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Completed!')
    }