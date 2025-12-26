import boto3
import geoip2.database
import json
import os

def handler(event, context):

    s3_client = boto3.client('s3')

    print("Copying GeoLite2-ASN.mmdb")

    with open('/tmp/GeoLite2-ASN.mmdb', 'wb') as f:
        s3_client.download_fileobj(os.environ['STAGED_GEO'], 'GeoLite2-ASN.mmdb', f) 
    f.close()

    print("Copying GeoLite2-City.mmdb")

    with open('/tmp/GeoLite2-City.mmdb', 'wb') as f:
        s3_client.download_fileobj(os.environ['STAGED_GEO'], 'GeoLite2-City.mmdb', f) 
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

    asn_data = []
    country_data = []
    state_data = []
    
    asn_label = []
    country_label = []
    state_label = []

    with geoip2.database.Reader('/tmp/GeoLite2-ASN.mmdb') as reader2:
        with geoip2.database.Reader('/tmp/GeoLite2-City.mmdb') as reader:
    
            for ip in ipv4s + ipv6s:
    
                try:
                    response = reader.city(ip)
                    country_code = response.country.iso_code
                    country_name = response.country.name
                    state_code = response.subdivisions.most_specific.iso_code
                    state_name = response.subdivisions.most_specific.name
                except:
                    country_code = None
                    country_name = None
                    state_code = None
                    state_name = None

                try:
                    response2 = reader2.asn(ip)
                    asn = response2.autonomous_system_number
                    org = response2.autonomous_system_organization
                except:
                    asn = None
                    org = None
    
                if asn is not None and org is not None:

                    asn_data.append(str(asn)+','+ip)
                    asn_label.append(str(asn)+' - '+org)

                if country_code is not None and country_name is not None:

                    country_data.append(country_code+','+ip)
                    country_label.append(country_code+' - '+country_name)

                if state_code is not None and state_name is not None:

                    state_data.append(state_code+','+ip)
                    state_label.append(state_code+' - '+state_name)

    print("Deduplicating data")

    asn_data = list(set(asn_data))
    country_data = list(set(country_data))
    state_data = list(set(state_data))
    asn_label = list(set(asn_label))
    country_label = list(set(country_label))
    state_label = list(set(state_label))

    print("Sorting data")

    asn_data.sort()
    country_data.sort()
    state_data.sort()
    asn_label.sort()
    country_label.sort()
    state_label.sort()

    print(f'ASN Data: {len(asn_data)} entries')
    print(f'Country Data: {len(country_data)} entries')
    print(f'State Data: {len(state_data)} entries')
    print(f'ASN Labels: {len(asn_label)} entries')
    print(f'Country Labels: {len(country_label)} entries')
    print(f'State Labels: {len(state_label)} entries')

    print("Writing CSVs to /tmp/")

    with open('/tmp/asn_data.csv','w') as f:
        for asn in asn_data:
            f.write(asn+'\n')
    f.close()

    with open('/tmp/asn_label.csv','w') as f:
        for asn in asn_label:
            f.write(asn+'\n')
    f.close()

    with open('/tmp/country_data.csv','w') as f:
        for country in country_data:
            f.write(country+'\n')
    f.close()

    with open('/tmp/country_label.csv','w') as f:
        for country in country_label:
            f.write(country+'\n')
    f.close()

    with open('/tmp/state_data.csv','w') as f:
        for state in state_data:
            f.write(state+'\n')
    f.close()

    with open('/tmp/state_label.csv','w') as f:
        for state in state_label:
            f.write(state+'\n')
    f.close()

    print("Uploading CSVs to S3")

    s3 = boto3.resource('s3')

    s3.meta.client.upload_file(
        '/tmp/asn_data.csv',
        os.environ['STAGED_S3'],
        'asn_data.csv',
        ExtraArgs = {
            'ContentType': "text/csv"
        }
    )

    s3.meta.client.upload_file(
        '/tmp/asn_label.csv',
        os.environ['STAGED_S3'],
        'asn_label.csv',
        ExtraArgs = {
            'ContentType': "text/csv"
        }
    )

    s3.meta.client.upload_file(
        '/tmp/country_data.csv',
        os.environ['STAGED_S3'],
        'country_data.csv',
        ExtraArgs = {
            'ContentType': "text/csv"
        }
    )

    s3.meta.client.upload_file(
        '/tmp/country_label.csv',
        os.environ['STAGED_S3'],
        'country_label.csv',
        ExtraArgs = {
            'ContentType': "text/csv"
        }
    )

    s3.meta.client.upload_file(
        '/tmp/state_data.csv',
        os.environ['STAGED_S3'],
        'state_data.csv',
        ExtraArgs = {
            'ContentType': "text/csv"
        }
    )

    s3.meta.client.upload_file(
        '/tmp/state_label.csv',
        os.environ['STAGED_S3'],
        'state_label.csv',
        ExtraArgs = {
            'ContentType': "text/csv"
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Completed!')
    }