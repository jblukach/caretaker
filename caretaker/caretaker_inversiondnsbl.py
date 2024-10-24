from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_cloudwatch as _cloudwatch,
    aws_cloudwatch_actions as _actions,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_sns as _sns,
    aws_ssm as _ssm
)

from constructs import Construct

class CaretakerInversionDnsbl(Stack):

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
            layer_version_arn = 'arn:aws:lambda:'+region+':'+extensions.string_value+':layer:getpublicip:13'
        )

        requests = _lambda.LayerVersion.from_layer_version_arn(
            self, 'requests',
            layer_version_arn = 'arn:aws:lambda:'+region+':'+extensions.string_value+':layer:requests:6'
        )

    ### TOPIC ###

        topic = _sns.Topic.from_topic_arn(
            self, 'topic',
            topic_arn = 'arn:aws:sns:'+region+':'+account+':caretaker'
        )

    ### IAM ###

        role = _iam.Role(
            self, 'role',
            role_name = 'inversiondnsbl',
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

        inversiondnsbl = _lambda.Function(
            self, 'inversiondnsbl',
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('sources/ip/inversiondnsbl'),
            timeout = Duration.seconds(900),
            handler = 'inversiondnsbl.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                FEED_TABLE = 'feed',
                VERIFY_TABLE = 'verify',
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

        logs = _logs.LogGroup(
            self, 'logs',
            log_group_name = '/aws/lambda/'+inversiondnsbl.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        inversiondnsblalarm = _cloudwatch.Alarm(
            self, 'inversiondnsblalarm',
            comparison_operator = _cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold = 0,
            evaluation_periods = 1,
            metric = inversiondnsbl.metric_errors(
                period = Duration.minutes(1)
            )
        )

        inversiondnsblalarm.add_alarm_action(
            _actions.SnsAction(topic)
        )

        event = _events.Rule(
            self, 'event',
            schedule = _events.Schedule.cron(
                minute = '30',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        event.add_target(
            _targets.LambdaFunction(inversiondnsbl)
        )

    ### LAMBDA ###

        inversiondnsbldomain = _lambda.Function(
            self, 'inversiondnsbldomain',
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('sources/dns/inversiondnsbl'),
            timeout = Duration.seconds(900),
            handler = 'inversiondnsbl.handler',
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

        inversiondnsbldomainlogs = _logs.LogGroup(
            self, 'inversiondnsbldomainlogs',
            log_group_name = '/aws/lambda/'+inversiondnsbldomain.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        inversiondnsbldomainalarm = _cloudwatch.Alarm(
            self, 'inversiondnsbldomainalarm',
            comparison_operator = _cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold = 0,
            evaluation_periods = 1,
            metric = inversiondnsbldomain.metric_errors(
                period = Duration.minutes(1)
            )
        )

        inversiondnsbldomainalarm.add_alarm_action(
            _actions.SnsAction(topic)
        )

        inversiondnsbldomainevent = _events.Rule(
            self, 'inversiondnsbldomainevent',
            schedule = _events.Schedule.cron(
                minute = '30',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        inversiondnsbldomainevent.add_target(
            _targets.LambdaFunction(inversiondnsbldomain)
        )
