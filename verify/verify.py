import boto3
import ipaddress
import os
from boto3.dynamodb.conditions import Key

def handler(event, context):

    if event['rawPath'] == '/suspect':

        bg = 'Orange'
        msg = 'Suspect Example'

    elif event['rawPath'] == '/unknown':

        bg = 'LightGray'
        msg = 'Unknown Example'

    else:

        try:

            ip = event['headers']['x-forwarded-for']
            iptype = ipaddress.ip_address(ip)

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

                for item in responsedata:
                    del item['pk']
                    del item['sk']

                bg = 'Orange'
                msg = responsedata

            else:

                bg = 'LightGray'
                msg = 'Unknown'

        except:

            bg = 'LightGray'
            msg = 'Unknown'

    html = '''<html><head><title>Project Caretaker</title></head><body bgcolor="'''+bg+'''">'''+str(msg)+'''</body></html>'''

    return {
        'statusCode': 200,
        'body': html,
        'headers': {
            'Content-Type': 'text/html'
        }
    }