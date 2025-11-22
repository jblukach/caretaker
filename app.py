#!/usr/bin/env python3
import os

import aws_cdk as cdk

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