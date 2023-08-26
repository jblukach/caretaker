#!/usr/bin/env python3
import os

import aws_cdk as cdk

from caretaker.caretaker_abusech import CaretakerAbuseCH
from caretaker.caretaker_alienvault import CaretakerAlienVault
from caretaker.caretaker_blocklist import CaretakerBlockList
from caretaker.caretaker_cinsscore import CaretakerCinsScore
from caretaker.caretaker_distillery import CaretakerDistillery
from caretaker.caretaker_proofpoint import CaretakerProofPoint
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