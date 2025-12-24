import ipaddress
import sqlite3

def handler(event, context):

    print(event)

    try:
        ip = ipaddress.ip_address(event['rawQueryString'])
        ip = str(event['rawQueryString'])
    except ValueError:
        ip = ipaddress.ip_address(event['requestContext']['http']['sourceIp'])
        ip = str(event['requestContext']['http']['sourceIp'])

    conn = sqlite3.connect('verify.sqlite3')
    c = conn.cursor()
    c.execute("SELECT verify.artifact, desc.name, desc.url FROM verify JOIN desc ON verify.scrid = desc.scrid WHERE verify.artifact = ?", (ip,))
    items = c.fetchall()
    c.execute("SELECT updated FROM last")
    last_updated = c.fetchone()[0]
    conn.close()

    if len(items) == 0:

        bg = 'LightGray'
        msg = '<h3>'+ip+' - Unknown</h3>'
        msg = msg+'<br><i>Last Updated: '+str(last_updated)+'</i>'

    else:

        bg = 'Orange'
        msg = '<h3>'+ip+' - Suspect</h3>'
        msg = msg+'<ul>'

        for item in items:
            msg += '<li><b>'+str(item[1])+'</b> - '+str(item[2])+'</li>'

        msg = msg+'</ul>'
        msg = msg+'<br><i>Last Updated: '+str(last_updated)+'</i>'

    html = '''<html><head><title>Project Caretaker</title></head><body bgcolor="'''+bg+'''">'''+msg+'''</body></html>'''

    return {
        'statusCode': 200,
        'body': html,
        'headers': {
            'Content-Type': 'text/html'
        }
    }