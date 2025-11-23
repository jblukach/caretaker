#!/usr/bin/env python3
import os

import aws_cdk as cdk

from addresses.binarydefense import AddressesBinaryDefense
from addresses.blocklistde import AddressesBlocklistDe
from addresses.blocklistua import AddressesBlocklistUa
from addresses.botscout import AddressesBotScout
from addresses.bruteforceblocker import AddressesBruteForceBlocker
from addresses.c2intelfeeds import AddressesC2IntelFeeds
from addresses.c2tracker import AddressesC2Tracker
from addresses.cinsscore import AddressesCinsScore
from addresses.feodotracker import AddressesFeodoTracker
from addresses.firehol import AddressesFirehol
from addresses.freeproxylist import AddressesFreeProxyList
from addresses.greensnow import AddressesGreenSnow
from addresses.inversiondnsbl import AddressesInversionDnsbl
from addresses.ipsum import AddressesIpsum
from addresses.jamesbrine import AddressesJamesBrine
from addresses.myipms import AddressesMyIpms
from addresses.nubinetwork import AddressesNubiNetwork
from addresses.proofpoint import AddressesProofPoint
from addresses.rutgers import AddressesRutgers
from addresses.sansisc import AddressesSansIsc
from addresses.sblam import AddressesSblam
from addresses.stopforumspam import AddressesStopForumSpam
from addresses.torexit import AddressesTorExit
from addresses.torlist import AddressesTorList
from addresses.ultimatehosts import AddressesUltimateHosts
from caretaker.caretaker_stack import CaretakerStack
from domains.c2intelfeeds import DomainsC2IntelFeeds
from domains.certpl import DomainsCertPl
from domains.disposableemails import DomainsDisposableEmails
from domains.inversiondnsbl import DomainsInversionDnsbl
from domains.oisd import DomainsOisd
from domains.openphish import DomainsOpenPhish
from domains.phishingarmy import DomainsPhishingArmy
from domains.phishtank import DomainsPhishTank
from domains.threatfox import DomainsThreatFox
from domains.threatview import DomainsThreatView
from domains.ultimatehosts import DomainsUltimateHosts
from domains.urlhaus import DomainsUrlhaus

app = cdk.App()

AddressesBinaryDefense(
    app, 'AddressesBinaryDefense',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesBlocklistDe(
    app, 'AddressesBlocklistDe',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesBlocklistUa(
    app, 'AddressesBlocklistUa',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesBotScout(
    app, 'AddressesBotScout',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesBruteForceBlocker(
    app, 'AddressesBruteForceBlocker',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesC2IntelFeeds(
    app, 'AddressesC2IntelFeeds',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesC2Tracker(
    app, 'AddressesC2Tracker',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesCinsScore(
    app, 'AddressesCinsScore',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesFeodoTracker(
    app, 'AddressesFeodoTracker',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesFirehol(
    app, 'AddressesFirehol',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesFreeProxyList(
    app, 'AddressesFreeProxyList',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesGreenSnow(
    app, 'AddressesGreenSnow',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesInversionDnsbl(
    app, 'AddressesInversionDnsbl',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesIpsum(
    app, 'AddressesIpsum',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesJamesBrine(
    app, 'AddressesJamesBrine',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesMyIpms(
    app, 'AddressesMyIpms',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesNubiNetwork(
    app, 'AddressesNubiNetwork',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesProofPoint(
    app, 'AddressesProofPoint',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesRutgers(
    app, 'AddressesRutgers',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesSansIsc(
    app, 'AddressesSansIsc',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesSblam(
    app, 'AddressesSblam',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesStopForumSpam(
    app, 'AddressesStopForumSpam',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesTorExit(
    app, 'AddressesTorExit',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesTorList(
    app, 'AddressesTorList',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

AddressesUltimateHosts(
    app, 'AddressesUltimateHosts',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerStack(
    app, 'CaretakerStack',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DomainsC2IntelFeeds(
    app, 'DomainsC2IntelFeeds',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DomainsCertPl(
    app, 'DomainsCertPl',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DomainsDisposableEmails(
    app, 'DomainsDisposableEmails',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DomainsInversionDnsbl(
    app, 'DomainsInversionDnsbl',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DomainsOisd(
    app, 'DomainsOisd',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DomainsOpenPhish(
    app, 'DomainsOpenPhish',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DomainsPhishingArmy(
    app, 'DomainsPhishingArmy',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DomainsPhishTank(
    app, 'DomainsPhishTank',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DomainsThreatFox(
    app, 'DomainsThreatFox',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DomainsThreatView(
    app, 'DomainsThreatView',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DomainsUltimateHosts(
    app, 'DomainsUltimateHosts',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

DomainsUrlhaus(
    app, 'DomainsUrlhaus',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

cdk.Tags.of(app).add('Alias','4n6ir.com')
cdk.Tags.of(app).add('GitHub','https://github.com/jblukach/caretaker')

app.synth()