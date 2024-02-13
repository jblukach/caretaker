import boto3
import json
import os

def handler(event, context):

    parameter = boto3.client('ssm')
        
    ssm = parameter.get_parameter(
        Name = os.environ['STEP_FUNCTION']
    )

    getobject = {}
    getobject['bucket'] = os.environ['S3_BUCKET']
    getobject['key'] = os.environ['S3_OBJECT']
    getobject['state'] = ssm['Parameter']['Value']
    getobject['table'] = os.environ['DYNAMODB_TABLE']
    getobject['offset'] = 0
    getobject['transitions'] = 0

    step = boto3.client('stepfunctions')
                
    step.start_execution(
        stateMachineArn = ssm['Parameter']['Value'],
        input = json.dumps(getobject),
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Start Step Function')
    }