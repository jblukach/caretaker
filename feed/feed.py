import boto3
import datetime
import hashlib
import json
import os
import requests
from boto3.dynamodb.conditions import Key

def hasher(filename):
    
    BLOCKSIZE = 65536
    sha256_hasher = hashlib.sha256()

    with open(filename,'rb') as h:
        buf = h.read(BLOCKSIZE)
        while len(buf) > 0:
            sha256_hasher.update(buf)
            buf = h.read(BLOCKSIZE)
    h.close()

    sha256 = sha256_hasher.hexdigest().upper()

    return sha256

def handler(event, context):

    dynamodb = boto3.resource('dynamodb')

    feed = dynamodb.Table('feed')

    output = {}
    output['name'] = 'Project Caretaker'
    output['description'] = 'Threat Feed for North Dakota'
    output['created'] = str(datetime.datetime.now())
    output['epoch'] = int(datetime.datetime.now().timestamp() * 1000)
    output['source'] = 'https://github.com/jblukach/caretaker/releases'

### DNS ###

    response = feed.query(
        KeyConditionExpression=Key('pk').eq('DNS#')
    )
    responsedata = response['Items']
    while 'LastEvaluatedKey' in response:
        response = feed.query(
            KeyConditionExpression=Key('pk').eq('DNS#'),
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        responsedata.extend(response['Items'])

    output['brand_count'] = len(responsedata)
    output['brand'] = []

    for item in responsedata:
        temp = {}
        temp['dns'] = item['dns']
        temp['source'] = item['source']
        temp['last'] = item['last']
        temp['epoch'] = int(item['epoch'])
        output['brand'].append(temp)

### IP ###

    response = feed.query(
        KeyConditionExpression=Key('pk').eq('IP#')
    )
    responsedata = response['Items']
    while 'LastEvaluatedKey' in response:
        response = feed.query(
            KeyConditionExpression=Key('pk').eq('IP#'),
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        responsedata.extend(response['Items'])

    output['reputation_count'] = len(responsedata)
    output['reputation'] = []

    for item in responsedata:
        temp = {}
        temp['ip'] = item['ip']
        temp['source'] = item['source']
        temp['last'] = item['last']
        temp['epoch'] = int(item['epoch'])
        output['reputation'].append(temp)

### OUTPUT ###

    f = open('/tmp/caretaker.json','w')
    f.write(json.dumps(output, indent = 4))
    f.close()

    ssm = boto3.client('ssm')

    status = ssm.get_parameter(
        Name = os.environ['SSM_PARAMETER_STATUS'],
        WithDecryption = False
    )

    sha256 = hasher('/tmp/caretaker.json')

    if status['Parameter']['Value'] != sha256:

        token = ssm.get_parameter(
            Name = os.environ['SSM_PARAMETER_GIT'], 
            WithDecryption = True
        )

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer '+token['Parameter']['Value'],
            'X-GitHub-Api-Version': '2022-11-28'
        }

        year = datetime.datetime.now().strftime('%Y')
        month = datetime.datetime.now().strftime('%m')
        day = datetime.datetime.now().strftime('%d')
        epoch = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

        data = '''{
            "tag_name":"v'''+str(year)+'''.'''+str(month)+str(day)+'''.'''+str(epoch)+'''",
            "target_commitish":"main",
            "name":"caretaker",
            "body":"The sha256 verification hash for the caretaker.json file is: '''+sha256+'''",
            "draft":false,
            "prerelease":false,
            "generate_release_notes":false
        }'''

        response = requests.post(
            'https://api.github.com/repos/jblukach/caretaker/releases',
            headers=headers,
            data=data
        )

        print(response.json())

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer '+token['Parameter']['Value'],
            'X-GitHub-Api-Version': '2022-11-28',
            'Content-Type': 'application/json'
        }

        params = {
            "name":"caretaker.json"
        }

        url = 'https://uploads.github.com/repos/jblukach/caretaker/releases/'+str(response.json()['id'])+'/assets'

        with open('/tmp/caretaker.json', 'rb') as f:
            data = f.read()
        f.close()

        response = requests.post(url, params=params, headers=headers, data=data)

        print(response.json())

        ssm.put_parameter(
            Name = os.environ['SSM_PARAMETER_STATUS'],
            Description = 'Caretaker Status Change',
            Value = sha256,
            Type = 'String',
            Overwrite = True
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Feed Generated')
    }