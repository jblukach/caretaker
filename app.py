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
from caretaker.caretaker_asnuse1 import CaretakerAsnUse1
from caretaker.caretaker_asnusw2 import CaretakerAsnUsw2
from caretaker.caretaker_build import CaretakerBuild
from caretaker.caretaker_couse1 import CaretakerCoUse1
from caretaker.caretaker_cousw2 import CaretakerCoUsw2
from caretaker.caretaker_deploy import CaretakerDeploy
from caretaker.caretaker_dnsuse1 import CaretakerDnsUse1
from caretaker.caretaker_dnsusw2 import CaretakerDnsUsw2
from caretaker.caretaker_ipuse1 import CaretakerIpUse1
from caretaker.caretaker_ipusw2 import CaretakerIpUsw2
from caretaker.caretaker_sqlite import CaretakerSqlite
from caretaker.caretaker_stackuse1 import CaretakerStackUse1
from caretaker.caretaker_stackuse2 import CaretakerStackUse2
from caretaker.caretaker_stackusw2 import CaretakerStackUsw2
from caretaker.caretaker_stuse1 import CaretakerStUse1
from caretaker.caretaker_stusw2 import CaretakerStUsw2
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
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesBlocklistDe(
    app, 'AddressesBlocklistDe',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesBlocklistUa(
    app, 'AddressesBlocklistUa',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesBotScout(
    app, 'AddressesBotScout',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesBruteForceBlocker(
    app, 'AddressesBruteForceBlocker',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesC2IntelFeeds(
    app, 'AddressesC2IntelFeeds',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesC2Tracker(
    app, 'AddressesC2Tracker',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesCinsScore(
    app, 'AddressesCinsScore',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesFeodoTracker(
    app, 'AddressesFeodoTracker',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesFirehol(
    app, 'AddressesFirehol',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesFreeProxyList(
    app, 'AddressesFreeProxyList',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesGreenSnow(
    app, 'AddressesGreenSnow',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesInversionDnsbl(
    app, 'AddressesInversionDnsbl',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesIpsum(
    app, 'AddressesIpsum',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesJamesBrine(
    app, 'AddressesJamesBrine',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesMyIpms(
    app, 'AddressesMyIpms',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesNubiNetwork(
    app, 'AddressesNubiNetwork',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesProofPoint(
    app, 'AddressesProofPoint',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesRutgers(
    app, 'AddressesRutgers',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesSansIsc(
    app, 'AddressesSansIsc',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesSblam(
    app, 'AddressesSblam',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesStopForumSpam(
    app, 'AddressesStopForumSpam',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesTorExit(
    app, 'AddressesTorExit',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesTorList(
    app, 'AddressesTorList',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

AddressesUltimateHosts(
    app, 'AddressesUltimateHosts',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

CaretakerAsnUse1(
    app, 'CaretakerAsnUse1',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

CaretakerAsnUsw2(
    app, 'CaretakerAsnUsw2',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-west-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

CaretakerBuild(
    app, 'CaretakerBuild',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

CaretakerCoUse1(
    app, 'CaretakerCoUse1',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

CaretakerCoUsw2(
    app, 'CaretakerCoUsw2',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-west-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

CaretakerDeploy(
    app, 'CaretakerDeploy',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

CaretakerDnsUse1(
    app, 'CaretakerDnsUse1',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

CaretakerDnsUsw2(
    app, 'CaretakerDnsUsw2',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-west-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

CaretakerIpUse1(
    app, 'CaretakerIpUse1',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

CaretakerIpUsw2(
    app, 'CaretakerIpUsw2',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-west-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

CaretakerSqlite(
    app, 'CaretakerSqlite',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

CaretakerStackUse1(
    app, 'CaretakerStackUse1',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

CaretakerStackUse2(
    app, 'CaretakerStackUse2',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

CaretakerStackUsw2(
    app, 'CaretakerStackUsw2',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-west-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

CaretakerStUse1(
    app, 'CaretakerStUse1',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

CaretakerStUsw2(
    app, 'CaretakerStUsw2',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-west-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DomainsC2IntelFeeds(
    app, 'DomainsC2IntelFeeds',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DomainsCertPl(
    app, 'DomainsCertPl',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DomainsDisposableEmails(
    app, 'DomainsDisposableEmails',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DomainsInversionDnsbl(
    app, 'DomainsInversionDnsbl',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DomainsOisd(
    app, 'DomainsOisd',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DomainsOpenPhish(
    app, 'DomainsOpenPhish',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DomainsPhishingArmy(
    app, 'DomainsPhishingArmy',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DomainsPhishTank(
    app, 'DomainsPhishTank',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DomainsThreatFox(
    app, 'DomainsThreatFox',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DomainsThreatView(
    app, 'DomainsThreatView',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DomainsUltimateHosts(
    app, 'DomainsUltimateHosts',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

DomainsUrlhaus(
    app, 'DomainsUrlhaus',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

cdk.Tags.of(app).add('Alias','caretaker')
cdk.Tags.of(app).add('GitHub','https://github.com/jblukach/caretaker')
cdk.Tags.of(app).add('Org','lukach.io')

app.synth()