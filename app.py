#!/usr/bin/env python3
import os

import aws_cdk as cdk

from caretaker.caretaker_abusech import CaretakerAbuseCH
from caretaker.caretaker_alienvault import CaretakerAlienVault
from caretaker.caretaker_binarydefense import CaretakerBinaryDefense
from caretaker.caretaker_blocklist import CaretakerBlockList
from caretaker.caretaker_cinsscore import CaretakerCinsScore
from caretaker.caretaker_digitalside import CaretakerDigitalSide
from caretaker.caretaker_distillery import CaretakerDistillery
from caretaker.caretaker_ipsum import CaretakerIPSum
from caretaker.caretaker_jamesbrine import CaretakerJamesBrine
from caretaker.caretaker_nubinetwork import CaretakerNubiNetwork
from caretaker.caretaker_proofpoint import CaretakerProofPoint
from caretaker.caretaker_rescure import CaretakerRescure
from caretaker.caretaker_rutgers import CaretakerRutgers
from caretaker.caretaker_scorecard import CaretakerScoreCard
from caretaker.caretaker_spamhaus import CaretakerSpamhaus
from caretaker.caretaker_stack import CaretakerStack
from caretaker.caretaker_tor import CaretakerTor
from caretaker.caretaker_verify import CaretakerVerify

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

CaretakerRescure(
    app, 'CaretakerRescure',
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

CaretakerScoreCard(
    app, 'CaretakerScoreCard',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

CaretakerSpamhaus(
    app, 'CaretakerSpamhaus',
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

cdk.Tags.of(app).add('Alias','Caretaker')
cdk.Tags.of(app).add('GitHub','https://github.com/jblukach/caretaker')

app.synth()