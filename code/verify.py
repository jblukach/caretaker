import boto3
import ipaddress
import os
import sqlite3
from boto3.dynamodb.conditions import Key

def handler(event, context):

    print(event)

    if event['rawPath'] == '/error':

        bg = 'Red'
        msg = '<h3>Error Example</h3>'

    elif event['rawPath'] == '/monitor':

        bg = 'Yellow'
        msg = '<h3>Not Monitored Example</h3>'

    elif event['rawPath'] == '/unknown':

        bg = 'LightGray'
        msg = '<h3>Unknown Example</h3>'

    else:

        try:

            if event['rawPath'] == '/suspect':
                ip = '137.22.34.8' # Random IP from Dataset
            else:
                ip = event['headers']['x-forwarded-for']

            intip = str(int(ipaddress.ip_address(ip)))

            conn = sqlite3.connect('allcidrs.sqlite3')
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
                    msg = '<h3>Unknown</h3>'

            else:

                bg = 'Yellow'
                msg = '<h3>Not Monitored</h3>'

        except:

            bg = 'Red'
            msg = '<h3>Error</h3>'

    html = '''<html><head><title>Project Caretaker</title></head><body bgcolor="'''+bg+'''">'''+msg+'''</body></html>'''

    return {
        'statusCode': 200,
        'body': html,
        'headers': {
            'Content-Type': 'text/html'
        }
    }