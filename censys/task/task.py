import boto3
import datetime
import json
import time
from censys.search import CensysHosts

def dateconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def search(service):

    time.sleep(1)

    query = h.search(
        '(autonomous_system.asn: {"14090","29744","14511","31758","26794","11138","63414","32809","14543","27539","18780","33339","36374","19530"}) and services.service_name=`'+service+'`',
        per_page = 100,
        pages = 20,
        fields = [
            'ip'
        ]
    )

    dynamodb = boto3.resource('dynamodb')
    verify = dynamodb.Table('verify')

    now = datetime.datetime.now()
    orig = datetime.datetime.utcfromtimestamp(0)
    epoch = int((now - orig).total_seconds() * 1000.0)
    seen = json.dumps(now, default=dateconverter)
    seen = seen.replace('"','')

    for page in query:
        for address in page:
            verify.put_item(
                Item = {
                    'pk': 'IP#',
                    'sk': 'IP#'+str(address['ip'])+'#SOURCE#'+service+'-censys.io',
                    'ip': str(address['ip']),
                    'source': service+'-censys.io',
                    'last': seen,
                    'epoch': epoch
                }
            )

h = CensysHosts()

search('ELASTICSEARCH')
search('FTP')
search('IMAP')
search('IPP')
search('KUBERNETES')
search('LDAP')
search('MEMCACHED')
search('MONGODB')
search('MSSQL')
search('MYSQL')
search('NETBIOS')
search('ORACLE')
search('PC_ANYWHERE')
search('POP3')
search('POSTGRES')
search('PPTP')
search('PROMETHEUS')
search('REDIS')
search('RDP')
search('SCCM')
search('SIP')
search('SLP')
search('SMB')
search('SNMP')
search('SSDP')
search('TELNET')
search('TFTP')
search('VNC')
search('X11')
