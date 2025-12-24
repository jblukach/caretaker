import ipaddress
import json
import sqlite3

def handler(event, context):

    try:
        ip = ipaddress.ip_address(event['rawQueryString'])
        ip = str(event['rawQueryString'])
    except ValueError:
        ip = ipaddress.ip_address(event['requestContext']['http']['sourceIp'])
        ip = str(event['requestContext']['http']['sourceIp'])

    conn = sqlite3.connect('ip.sqlite3')
    c = conn.cursor()
    c.execute("SELECT ip.artifact, desc.name, desc.url FROM ip JOIN desc ON ip.scrid = desc.scrid WHERE ip.artifact = ?", (ip,))
    items = c.fetchall()
    c.execute("SELECT updated FROM last")
    last_updated = c.fetchone()[0]
    conn.close()

    code = 200

    if len(items) == 0:

        msg = {
            'dns': ip,
            'status': 'unknown',
            'updated': str(last_updated)
        }

    else:

        msg = {
            'dns': ip,
            'status': 'suspect',
            'attribution':items,
            'updated': str(last_updated)
        }

    return {
        'statusCode': code,
        'body': json.dumps(msg, indent = 4)
    }