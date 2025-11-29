import ipaddress
import json
import sqlite3

def handler(event, context):
    
    print(event)

    try:

        ip = ipaddress.ip_address(event['rawQueryString'])
        ip = str(event['rawQueryString'])

        conn = sqlite3.connect('ipv4.sqlite3')
        c = conn.cursor()
        c.execute("SELECT desc.name, desc.url FROM ipv4 JOIN desc ON ipv4.scrid = desc.scrid WHERE ipv4.artifact = ?", (ip,))
        items = c.fetchall()
        c.execute("SELECT updated FROM last")
        last_updated = c.fetchone()[0]
        conn.close()

        code = 200

        if len(items) == 0:

            msg = {
                'ip': ip,
                'status': 'unknown',
                'updated': str(last_updated)
            }

        else:

            msg = {
                'ip': ip,
                'status': 'suspect',
                'attribution':items,
                'updated': str(last_updated)
            }

    except ValueError:
        code = 404
        msg = 'Invalid IP Address'

    return {
        'statusCode': code,
        'body': json.dumps(msg, indent = 4)
    }