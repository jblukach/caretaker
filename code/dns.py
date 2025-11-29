import json

def handler(event, context):
    
    print(event)

    print(event['rawQueryString'])

    
    return {
        'statusCode': 200,
        'body': json.dumps('DNS!')
    }