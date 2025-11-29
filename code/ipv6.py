import ipaddress
import json
import sqlite3

def handler(event, context):
    
    print(event)

    try:

        ip = ipaddress.ip_address(event['rawQueryString'])
        ip = str(event['rawQueryString'])

        conn = sqlite3.connect('ipv6.sqlite3')
        c = conn.cursor()
        c.execute("SELECT desc.name, desc.url FROM ipv6 JOIN desc ON ipv6.scrid = desc.scrid WHERE ipv6.artifact = ?", (ip,))
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
        pass

    return {
        'statusCode': code,
        'body': json.dumps(msg, indent = 4)
    }