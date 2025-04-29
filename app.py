#!/usr/bin/env python3
import os

import aws_cdk as cdk

from caretaker.caretaker_stack import CaretakerStack

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

cdk.Tags.of(app).add('Alias','4n6ir.com')
cdk.Tags.of(app).add('GitHub','https://github.com/jblukach/caretaker')

app.synth()