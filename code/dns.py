import json
import sqlite3

def handler(event, context):

    if '.' in event['rawQueryString']:

        dns = str(event['rawQueryString'])

        conn = sqlite3.connect('dns.sqlite3')
        c = conn.cursor()
        c.execute("SELECT desc.name, desc.url FROM dns JOIN desc ON dns.scrid = desc.scrid WHERE dns.artifact = ?", (dns,))
        items = c.fetchall()
        c.execute("SELECT updated FROM last")
        last_updated = c.fetchone()[0]
        conn.close()

        code = 200

        if len(items) == 0:

            msg = {
                'dns': dns,
                'status': 'unknown',
                'updated': str(last_updated)
            }

        else:

            msg = {
                'dns': dns,
                'status': 'suspect',
                'attribution':items,
                'updated': str(last_updated)
            }

    else:

        code = 404
        msg = 'ex. https://api.lukach.io/osint/dns?4n6ir.com'

    return {
        'statusCode': code,
        'body': json.dumps(msg, indent = 4)
    }