#!/usr/bin/env python3
import os

import aws_cdk as cdk

from caretaker.caretaker_abusech import CaretakerAbuseCH
from caretaker.caretaker_alienvault import CaretakerAlienVault
from caretaker.caretaker_binarydefense import CaretakerBinaryDefense
from caretaker.caretaker_blocklist import CaretakerBlockList
from caretaker.caretaker_c2intelfeeds import CaretakerC2IntelFeeds
from caretaker.caretaker_c2tracker import CaretakerC2Tracker
from caretaker.caretaker_censysservice1 import CaretakerCensysService1
from caretaker.caretaker_censysservice2 import CaretakerCensysService2
from caretaker.caretaker_censysservice3 import CaretakerCensysService3
from caretaker.caretaker_censysservice4 import CaretakerCensysService4
from caretaker.caretaker_censysservice5 import CaretakerCensysService5
from caretaker.caretaker_censysservice6 import CaretakerCensysService6
from caretaker.caretaker_censysservice7 import CaretakerCensysService7
from caretaker.caretaker_certificates import CaretakerCertificates
from caretaker.caretaker_certpl import CaretakerCertPl
from caretaker.caretaker_cinsscore import CaretakerCinsScore
from caretaker.caretaker_digitalside import CaretakerDigitalSide
from caretaker.caretaker_distillery import CaretakerDistillery
from caretaker.caretaker_feed import CaretakerFeed
from caretaker.caretaker_feedwalla import CaretakerFeedwalla
from caretaker.caretaker_greensnow import CaretakerGreenSnow
from caretaker.caretaker_inversiondnsbl import CaretakerInversionDnsbl
from caretaker.caretaker_ipsum import CaretakerIPSum
from caretaker.caretaker_jamesbrine import CaretakerJamesBrine
from caretaker.caretaker_nubinetwork import CaretakerNubiNetwork
from caretaker.caretaker_oisd import CaretakerOisd
from caretaker.caretaker_openphish import CaretakerOpenPhish
from caretaker.caretaker_phishingarmy import CaretakerPhishingArmy
from caretaker.caretaker_proofpoint import CaretakerProofPoint
from caretaker.caretaker_rutgers import CaretakerRutgers
from caretaker.caretaker_stack import CaretakerStack
from caretaker.caretaker_tor import CaretakerTor
from caretaker.caretaker_tundralabs import CaretakerTundraLabs
from caretaker.caretaker_ultimatehosts import CaretakerUltimateHosts
from caretaker.caretaker_urlabuse import CaretakerUrlAbuse
from caretaker.caretaker_verify import CaretakerVerify
from caretaker.caretaker_zonefiles import CaretakerZoneFiles

app = cdk.App()

CaretakerAbuseCH(
    app, 'CaretakerAbuseCH',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerAlienVault(
    app, 'CaretakerAlienVault',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerBinaryDefense(
    app, 'CaretakerBinaryDefense',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerBlockList(
    app, 'CaretakerBlockList',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerC2IntelFeeds(
    app, 'CaretakerC2IntelFeeds',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerC2Tracker(
    app, 'CaretakerC2Tracker',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerCensysService1(
    app, 'CaretakerCensysService1',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerCensysService2(
    app, 'CaretakerCensysService2',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerCensysService3(
    app, 'CaretakerCensysService3',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerCensysService4(
    app, 'CaretakerCensysService4',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerCensysService5(
    app, 'CaretakerCensysService5',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerCensysService6(
    app, 'CaretakerCensysService6',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerCensysService7(
    app, 'CaretakerCensysService7',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerCertificates(
    app, 'CaretakerCertificates',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerCertPl(
    app, 'CaretakerCertPl',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerCinsScore(
    app, 'CaretakerCinsScore',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerDigitalSide(
    app, 'CaretakerDigitalSide',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerDistillery(
    app, 'CaretakerDistillery',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerFeed(
    app, 'CaretakerFeed',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerFeedwalla(
    app, 'CaretakerFeedwalla',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerGreenSnow(
    app, 'CaretakerGreenSnow',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerInversionDnsbl(
    app, 'CaretakerInversionDnsbl',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerIPSum(
    app, 'CaretakerIPSum',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerJamesBrine(
    app, 'CaretakerJamesBrine',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerNubiNetwork(
    app, 'CaretakerNubiNetwork',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerOisd(
    app, 'CaretakerOisd',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerOpenPhish(
    app, 'CaretakerOpenPhish',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerPhishingArmy(
    app, 'CaretakerPhishingArmy',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerProofPoint(
    app, 'CaretakerProofPoint',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerRutgers(
    app, 'CaretakerRutgers',
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

CaretakerTor(
    app, 'CaretakerTor',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerTundraLabs(
    app, 'CaretakerTundraLabs',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerUltimateHosts(
    app, 'CaretakerUltimateHosts',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerUrlAbuse(
    app, 'CaretakerUrlAbuse',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerVerify(
    app, 'CaretakerVerify',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerZoneFiles(
    app, 'CaretakerZoneFiles',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

cdk.Tags.of(app).add('Alias','Caretaker')
cdk.Tags.of(app).add('GitHub','https://github.com/jblukach/caretaker')

app.synth()