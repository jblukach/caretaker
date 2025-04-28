:construction: :construction: :construction: :construction: :construction:

![Project Caretaker](images/caretaker.png)

Reputation is the most critical asset available when using the Internet, as it helps us decide which services we feel safe using. It can also impact an end-users ability to use the web if the connection had previous suspect behavior. Project Caretaker aims to provide a Threat Feed for North Dakota so that anyone can verify Internet reputation.

Every day at 14:00 UTC, the Internet addresses for the Broadband Association of North Dakota (BAND) members, North Dakota Univesity System (NDUS), and the State of North Dakota (ITD) get updated from Security Trails, a Recorded Future company.

- https://bgpview.io
- https://broadbandnd.com
- https://ndit.nd.gov

I added additional Internet Service Providers (ISPs) to improve state coverage. :earth_americas:

### Autonomous System Numbers (ASN)

* 11138 - BEK Communications Cooperative (BCC-141)
* 11232 - Midcontinent Communications (MIDCO-1)
* 14090 - North Dakota Telephone Company (GONDT)
* 14511 - Polar Communications (PLAR)
* 14543 - SRT Communications, Inc. (SRTC)
* 15267 - 702 Communications (702COM)
* 18780 - Reservation Telephone Coop. (RTC-81)
* 19530 - State of North Dakota, ITD (SNDI-1)
* 21730 - Halstad Telephone Company (HALSTA)
* 26794 - Dakota Carrier Network (DCN-38)
* 27539 - West River Telecommunications Cooperative (WRVR)
* 29744 - United Telephone Mutual Aid Corporation (UNITED-190)
* 31758 - Griggs County Telephone Co. (GCT-43)
* 32809 - Dickey Rural Networks (DRN-3)
* 33339 - Nemont Telecommunications (NEMON-2)
* 36374 - Stellar Association, LLC (SAL-65)
* 55105 - Northwest Communications Cooperative (NCC-115)
* 63414 - Dakota Central Telecommunications Cooperative (DAKTE)
* 400439 - Consolidated Telecommunications (CONSO-10)

It results in **1,295,104** IPv4 addresses and **31** IPv6 cidr allocations to monitor for reputation. 

A /32 subnet of IPv6 has 65,536 /48 subnets, each with 65,536 /64 subnets with 18,446,744,073,709,551,616 addresses, making a vast number. IPv6 addresses get converted to integers to determine if they fall into any of the monitored ranges.

### Brand Monitoring

Every day at 14:00 UTC, queries run against **Censys** for trusted certificates with the province of either **North Dakota** or the abbreviation **ND** to collect **8,232** domain names for ```apex``` and ```www``` brand monitoring.

Thank you to **Censys** for providing research access that makes this possible!

- https://search.censys.io

Certificate Transparency (CT) is a security standard for monitoring and auditing the issuance of digital certificates. Chrome, Firefox, Safari, etc., web browsers require certificates to be listed to be trusted when surfing the Internet.

- https://certificate.transparency.dev

The domain names from the certificates are normalized to guarantee valid top-level domains with wild cards removed.

- https://www.iana.org

### Email Security

Every day at 15:00 UTC, domains are checked for Mail Exchange (**MX**) records to determine if an email server is present; once identified, verification of Domain-based Message Authentication, Reporting & Conformance (**DMARC**), and Sender Policy Framework (**SPF**) records occurs.

Sender Policy Framework is an email authentication standard that determines the addresses and domains that can send emails that require reputation monitoring.

### Misconfiguration

Every day starting at 15:00 UTC, queries run against **Censys** for misconfigurations that expose insecure services to the Internet. 

Thanks again to **Censys** for providing research access that makes this possible!

- https://search.censys.io

### Monitored Services

|     |     |     |     |
|:---:|:---:|:---:|:---:|
| ACTIVEMQ | AFP | AMQP | APPLE_AIRPORT_ADMIN | 
| BACNET | COAP | COBALT_STRIKE | CWMP **+** |
| DARKGATE | DCERPC | DHCPDISCOVER | DNP3 | 
| ECHO | ELASTICSEARCH | EPMD | ETHEREUM | 
| FINGERD | FOX | FTP | IMAP |
| IPMI | IPP | ISCSI | IOTA |
| KRPC | KUBERNETES | LDAP | MDNS |
| MEMCACHED | MMS | MODBUS | MONERO_P2P |
| MONGODB | MQTT | MSSQL | MYSQL |
| NBD | NETBIOS | NNTP | OPC_UA |
| ORACLE | PC_ANYWHERE | PCOM | PGBOUNCER |
| POP3 | PORTMAP | POSTGRES | PPTP |
| PROMETHEUS | REDIS | RLOGIN | ROCKETMQ |
| RDP | RTSP | S7 | SCCM | 
| SIP | SKINNY | SMB | SNMP | 
| SPICE | SSDP | TACACS_PLUS | TEAM_VIEWER |
| TELNET | TFTP | TPLINK_KASA | UPNP |
| VNC | WHOIS | WINRM | X11 |
| ZEROMQ |

- https://search.censys.io/search/definitions

**+** CWMP prevalence required exclusion from Midcontinent results.

### Reputation

The following threat feeds pull at thirty minutes past the hour to determine if any addresses from North Dakota exist on the lists. 

If there are others that you would like added, please open an issue on the repository?

I appreciate all the work that goes into maintaining these lists - thank you!

- https://cert.pl
- https://cinsscore.com
- https://feodotracker.abuse.ch
- https://github.com/drb-ra
- https://github.com/elliotwutingfeng
- https://github.com/jblukach
- https://github.com/montysecurity
- https://github.com/stamparm
- https://github.com/Ultimate-Hosts-Blacklist
- https://greensnow.co
- https://jamesbrine.com.au
- https://oisd.nl
- https://openphish.com
- https://osint.digitalside.it
- https://otx.alienvault.com
- https://phishing.army
- https://report.cs.rutgers.edu
- https://sslbl.abuse.ch
- https://urlabuse.com
- https://zonefiles.io
- https://www.binarydefense.com
- https://www.blocklist.de
- https://www.dan.me.uk
- https://www.nubi-network.com
- https://www.proofpoint.com

The critical part is making the results usable by anyone with just a website visit!

The lookup completes using the Internet address your connection originates from to protect the potential sensitivity of the returned results.

We don't want to tip the hand like playing cards, losing the advantage!

- https://verify.tundralabs.org

If the website returns **gray**, it means there is no data currently available, but that does not mean there still could not be a problem. 

![Project Caretaker Unknown Alert](images/unknown.png)

When the website returns **orange**, it will list sources and last-seen timestamps of potential reputation concerns.

![Project Caretaker Suspect Alert](images/suspect.png)

When the website returns **yellow**, monitoring is not occurring.

![Project Caretaker Suspect Alert](images/monitor.png)

When the website returns **red**, please try again or check back later.

![Project Caretaker Error Alert](images/error.png)

You may require additional assistance to resolve the issue outside of this project; at least the awareness to start asking questions will exist.
