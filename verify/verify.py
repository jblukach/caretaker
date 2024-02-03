import boto3
import ipaddress
import os
import sqlite3
from boto3.dynamodb.conditions import Key

def handler(event, context):

    if event['rawPath'] == '/error':

        bg = 'Red'
        msg = 'Error Example'

    elif event['rawPath'] == '/monitor':

        bg = 'Yellow'
        msg = 'Not Monitored Example'

    elif event['rawPath'] == '/unknown':

        bg = 'LightGray'
        msg = 'Unknown Example'

    else:

        try:

            s3 = boto3.client('s3')
            s3.download_file(os.environ['S3_BUCKET'], 'allcidrs.sqlite3', '/tmp/allcidrs.sqlite3')

            if event['rawPath'] == '/suspect':
                ip = '137.22.34.8' # Random IP from Dataset
            else:
                ip = event['headers']['x-forwarded-for']

            if ipaddress.ip_network(ip).version == 4:
                intip = int(ipaddress.IPv4Address(ip))
            else:
                intip = int(ipaddress.IPv6Address(ip))

            conn = sqlite3.connect('/tmp/allcidrs.sqlite3')
            c = conn.cursor()
            c.execute("SELECT cidr FROM allcidrs WHERE firstip <= ? AND lastip >= ?", (str(intip), str(intip)))
            results = c.fetchall()
            conn.close()
        
            if len(results) > 0:

                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table(os.environ['VERIFY_TABLE'])

                response = table.query(
                    KeyConditionExpression = Key('pk').eq('IP#') & Key('sk').begins_with('IP#'+ip+'#')
                )
                responsedata = response['Items']
                while 'LastEvaluatedKey' in response:
                    response = table.query(
                        KeyConditionExpression = Key('pk').eq('IP#') & Key('sk').begins_with('IP#'+ip+'#'),
                        ExclusiveStartKey = response['LastEvaluatedKey']
                    )
                    responsedata.update(response['Items'])

                if len(responsedata) > 0:
                    
                    bg = 'Orange'

                    if event['rawPath'] == '/suspect':
                        msg = '<h3>'+ip+' Example</h3><ul>'
                    else:
                        msg = '<h3>'+ip+'</h3><ul>'

                    for item in responsedata:
                        msg += '<li><b>'+str(item['source'])+'</b> - '+str(item['last'])+'</li>'

                    msg = msg+'</ul>'

                else:

                    bg = 'LightGray'
                    msg = 'Unknown'

            else:

                bg = 'Yellow'
                msg = 'Not Monitored'

        except:

            bg = 'Red'
            msg = 'Error'

    html = '''<html><head><title>Project Caretaker</title></head><body bgcolor="'''+bg+'''">'''+msg+'''</body></html>'''

    return {
        'statusCode': 200,
        'body': html,
        'headers': {
            'Content-Type': 'text/html'
        }
    }