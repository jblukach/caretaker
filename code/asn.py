import json
import os
import sqlite3

def handler(event, context):

    if not event['rawQueryString'].isdigit() or event['rawQueryString'] is None or event['rawQueryString'] == '':

        code = 404
        msg = 'ex. https://api.lukach.io/osint/asn?19530'

    else:

        asn = str(event['rawQueryString'])

        conn = sqlite3.connect('asn.sqlite3')
        c = conn.cursor()
        c.execute("SELECT asn.artifact FROM asn WHERE asn.asnid = ?", (asn,))
        items = c.fetchall()
        c.execute("SELECT updated FROM org")
        org_updated = c.fetchone()[0]
        c.execute("SELECT updated FROM city")
        city_updated = c.fetchone()[0]
        c.execute("SELECT updated FROM last")
        last_updated = c.fetchone()[0]
        conn.close()

        code = 200
        count = len(items)

        if len(json.dumps(items).encode("utf-8")) >= 2000000:
            items = []
            items.append('LARGE PAYLOAD - NOT DISPLAYED')

        msg = {
            'asn': asn,
            'count': count,
            'attribution': 'This product includes GeoLite2 data created by MaxMind, available from https://www.maxmind.com.',
            'geolite2-asn.mmdb': str(org_updated),
            'geolite2-city.mmdb': str(city_updated),
            'last-updated': str(last_updated),
            'region': os.environ['AWS_REGION'],
            'artifacts': items
        }

    return {
        'statusCode': code,
        'body': json.dumps(msg, indent = 4)
    }