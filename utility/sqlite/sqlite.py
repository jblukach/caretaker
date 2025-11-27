import boto3
import json
import os

def handler(event, context):

    addresses = []
    addresses.append({"id":"1","name":"binarydefense","url":"https://binarydefense.com"})
    addresses.append({"id":"2","name":"blocklistde","url":"https://www.blocklist.de"})
    addresses.append({"id":"3","name":"blocklistua","url":"https://blocklist.net.ua"})
    addresses.append({"id":"4","name":"botscout","url":"https://botscout.com"})
    addresses.append({"id":"5","name":"bruteforceblocker","url":"https://danger.rulez.sk"})
    addresses.append({"id":"6","name":"c2intelfeeds","url":"https://github.com/drb-ra/C2IntelFeeds"})
    addresses.append({"id":"7","name":"c2tracker","url":"https://github.com/montysecurity/C2-Tracker"})
    addresses.append({"id":"8","name":"cinsscore","url":"https://cinsscore.com"})
    addresses.append({"id":"9","name":"feodotracker","url":"https://feodotracker.abuse.ch"})
    addresses.append({"id":"10","name":"firehol","url":"https://iplists.firehol.org"})
    addresses.append({"id":"11","name":"freeproxylist","url":"https://free-proxy-list.net"})
    addresses.append({"id":"12","name":"greensnow","url":"https://www.greensnow.co"})
    addresses.append({"id":"13","name":"inversiondnsbl","url":"https://github.com/elliotwutingfeng/Inversion-DNSBL-Blocklists"})
    addresses.append({"id":"14","name":"ipsum","url":"https://github.com/stamparm/ipsum"})
    addresses.append({"id":"15","name":"jamesbrine","url":"https://jamesbrine.com.au"})
    addresses.append({"id":"16","name":"myipms","url":"https://myip.ms"})
    addresses.append({"id":"17","name":"nubinetwork","url":"https://www.nubi-network.com"})
    addresses.append({"id":"18","name":"proofpoint","url":"https://www.proofpoint.com"})
    addresses.append({"id":"19","name":"rutgers","url":"https://report.cs.rutgers.edu"})
    addresses.append({"id":"20","name":"sansisc","url":"https://isc.sans.edu"})
    addresses.append({"id":"21","name":"sblam","url":"https://sblam.com"})
    addresses.append({"id":"22","name":"stopforumspam","url":"https://stopforumspam.com"})
    addresses.append({"id":"23","name":"torexit","url":"https://www.torproject.org"})
    addresses.append({"id":"24","name":"torlist","url":"https://www.dan.me.uk"})
    addresses.append({"id":"25","name":"ultimatehosts","url":"https://github.com/Ultimate-Hosts-Blacklist/Ultimate.Hosts.Blacklist"})

    domains = []
    domains.append({"id":"A","name":"c2intelfeeds","url":"https://github.com/drb-ra/C2IntelFeeds"})
    domains.append({"id":"B","name":"certpl","url":"https://cert.pl"})
    domains.append({"id":"C","name":"disposableemails","url":"https://github.com/disposable-email-domains/disposable-email-domains"})
    domains.append({"id":"D","name":"inversiondnsbl","url":"https://github.com/elliotwutingfeng/Inversion-DNSBL-Blocklists"})
    domains.append({"id":"E","name":"oisd","url":"https://oisd.nl"})
    domains.append({"id":"F","name":"openphish","url":"https://openphish.com"})
    domains.append({"id":"G","name":"phishingarmy","url":"https://phishing.army"})
    domains.append({"id":"H","name":"phishtank","url":"https://phishtank.com"})
    domains.append({"id":"I","name":"threatfox","url":"https://threatfox.abuse.ch"})
    domains.append({"id":"J","name":"threatview","url":"https://threatview.io"})
    domains.append({"id":"K","name":"ultimatehosts","url":"https://github.com/Ultimate-Hosts-Blacklist/Ultimate.Hosts.Blacklist"})
    domains.append({"id":"L","name":"urlhaus","url":"https://urlhaus.abuse.ch"})

    s3 = boto3.client('s3')

    s3.download_file(os.environ['STAGED_S3'], 'domains.csv', '/tmp/domains.csv')
    s3.download_file(os.environ['STAGED_S3'], 'ipv4s.csv', '/tmp/ipv4s.csv')
    s3.download_file(os.environ['STAGED_S3'], 'ipv6s.csv', '/tmp/ipv6s.csv')

    for address in addresses:
        print(address)

    for domain in domains:
        print(domain)


    return {
        'statusCode': 200,
        'body': json.dumps('Completed!')
    }