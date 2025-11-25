from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_apigatewayv2 as _api,
    aws_apigatewayv2_integrations as _integrations,
    aws_certificatemanager as _acm,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_route53 as _route53,
    aws_route53_targets as _r53targets,
    aws_ssm as _ssm
)

from constructs import Construct

class CaretakerIpv4(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
