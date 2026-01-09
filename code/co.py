import json
import os
import sqlite3

def handler(event, context):

    if not event['rawQueryString'].isalpha() or len(event['rawQueryString']) != 2 or event['rawQueryString'] is None or event['rawQueryString'] == '':

        code = 404
        msg = 'ex. https://api.lukach.io/osint/co?US'

    else:

        co = str(event['rawQueryString']).upper()

        conn = sqlite3.connect('co.sqlite3')
        c = conn.cursor()
        c.execute("SELECT co.artifact FROM co WHERE co.coid = ?", (co,))
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
            'co': co,
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