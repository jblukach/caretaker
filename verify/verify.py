def handler(event, context):

    print(event)

    return {
        'statusCode': 200,
        'body': event['headers']['x-forwarded-for'],
        'headers': {
            'Content-Type': 'text/plain'
        }
    }