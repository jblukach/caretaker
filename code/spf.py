import dns.resolver
import json
import ipaddress
import netaddr

def handler(event, context):
    
    print(event)
    
    if '.' in event['rawQueryString']:

        url = str(event['rawQueryString'])

        try:

            domain = []
            ipv4 = []
            count = 0

            f = open('unique_ipv6s.csv', 'r')
            data = f.read()
            f.close()

            data = data.split('\n')

            suspect = []
            for line in data:
                if len(line) > 2:
                    suspect.append(int(ipaddress.ip_address(line)))

            ipv6_matches = []

            answers = dns.resolver.resolve(url, 'TXT')

            for rdata in answers:
                if 'v=spf1' in str(rdata):
                    data = rdata.to_text()
                    data = data.replace('"', '')
                    for d in data.split(' '):
                        if d.startswith('include:'):
                            domain.append(d.split('include:')[1])
                        elif d.startswith('ip4:'):
                            network = netaddr.IPNetwork(d.split('ip4:')[1])
                            for addr in network:
                                ipv4.append(str(addr))
                        elif d.startswith('ip6:'):
                            netrange = ipaddress.IPv6Network(d.split('ip6:')[1])
                            first, last = netrange[0], netrange[-1]
                            firstip = int(ipaddress.IPv6Address(first))
                            lastip = int(ipaddress.IPv6Address(last))
                            count = (lastip - firstip) + count
                            for ip in suspect:
                                if ip >= firstip and ip <= lastip:
                                    ipv6_matches.append(str(ipaddress.ip_address(ip)))

            f = open('unique_ipv4s.csv', 'r')
            data = f.read()
            f.close()

            suspect = []
            suspect = data.split('\n')

            ipv4_matches = list(set(ipv4).intersection(suspect))

            f = open('unique_domains.csv', 'r')
            data = f.read()
            f.close()

            suspect = []
            suspect = data.split('\n')

            dns_matches = list(set(domain).intersection(suspect))

            code = 200
            msg = {
                'domain':url,
                'suspect_dns':len(dns_matches),
                'suspect_ipv4':len(ipv4_matches),
                'suspect_ipv6':len(ipv6_matches),
                'total_dns':len(domain),
                'total_ipv4':len(ipv4),
                'total_ipv6':count,
                'dns_matches':dns_matches,
                'ipv4_matches':ipv4_matches,
                'ipv6_matches':ipv6_matches
            }

        except:

            code = 404
            msg = 'Resolver Error'

    else:

        code = 404
        msg = 'Invalid Domain'

    return {
        'statusCode': code,
        'body': json.dumps(msg, indent = 4)
    }