#!/usr/bin/env python3
import os

import aws_cdk as cdk

from services1.services1_stack import Services1Stack

app = cdk.App()

Services1Stack(
    app, 'Services1Stack',
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