import boto3
import json
import os

def handler(event, context):

    ssm = boto3.client('ssm')

    api = ssm.get_parameter(Name='/censys/api', WithDecryption=True)['Parameter']['Value']
    key = ssm.get_parameter(Name='/censys/key', WithDecryption=True)['Parameter']['Value']

    subids = []
    subids.append(os.environ['SUBNET_ID'])

    sgids = []
    sgids.append(os.environ['SECURITY_GROUP'])

    client = boto3.client('ecs')

    response = client.run_task(
        cluster=os.environ['CLUSTER_NAME'],
        launchType = 'FARGATE',
        taskDefinition=os.environ['TASK_DEFINITION'],
        overrides={
            'containerOverrides': [
                {
                    'name': os.environ['CONTAINER_NAME'],
                    'environment': [
                        {
                            'name': 'CENSYS_API_ID',
                            'value': api
                        },
                        {
                            'name': 'CENSYS_API_SECRET',
                            'value': key
                        }                        
                    ]
                }
            ]
        },
        count = 1,
        platformVersion='LATEST',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': subids,
                'securityGroups': sgids,
                'assignPublicIp': 'ENABLED'
            }
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Run Fargate Task')
    }