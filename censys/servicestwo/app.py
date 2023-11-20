#!/usr/bin/env python3
import os

import aws_cdk as cdk

from servicestwo.servicestwo_stack import ServicestwoStack

app = cdk.App()

ServicestwoStack(
    app, 'ServicestwoStack',
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