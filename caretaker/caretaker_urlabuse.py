from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_ssm as _ssm
)

from constructs import Construct

class CaretakerUrlAbuse(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account
        region = Stack.of(self).region

    ### LAMBDA LAYERS ###

        extensions = _ssm.StringParameter.from_string_parameter_attributes(
            self, 'extensions',
            parameter_name = '/extensions/account'
        )

        getpublicip = _lambda.LayerVersion.from_layer_version_arn(
            self, 'getpublicip',
            layer_version_arn = 'arn:aws:lambda:'+region+':'+extensions.string_value+':layer:getpublicip:14'
        )

        requests = _lambda.LayerVersion.from_layer_version_arn(
            self, 'requests',
            layer_version_arn = 'arn:aws:lambda:'+region+':'+extensions.string_value+':layer:requests:7'
        )

    ### IAM ###

        role = _iam.Role(
            self, 'role',
            role_name = 'urlabuse',
            assumed_by = _iam.ServicePrincipal(
                'lambda.amazonaws.com'
            )
        )

        role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                'service-role/AWSLambdaBasicExecutionRole'
            )
        )

        role.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'dynamodb:PutItem',
                    's3:GetObject',
                    's3:PutObject'
                ],
                resources = [
                    '*'
                ]
            )
        )

    ### LAMBDA ###

        urlabuse = _lambda.Function(
            self, 'urlabuse',
            runtime = _lambda.Runtime.PYTHON_3_13,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('sources/dns/urlabuse'),
            timeout = Duration.seconds(900),
            handler = 'urlabuse.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                FEED_TABLE = 'feed',
                S3_BUCKET = 'caretakerbucket'
            ),
            memory_size = 512,
            retry_attempts = 0,
            role = role,
            layers = [
                getpublicip,
                requests
            ]
        )

        urlabuselogs = _logs.LogGroup(
            self, 'urlabuselogs',
            log_group_name = '/aws/lambda/'+urlabuse.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        urlabuseevent = _events.Rule(
            self, 'urlabuseevent',
            schedule = _events.Schedule.cron(
                minute = '30',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        urlabuseevent.add_target(
            _targets.LambdaFunction(urlabuse)
        )
