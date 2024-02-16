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
    aws_sns as _sns
)

from constructs import Construct

class CaretakerCyberCure(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account
        region = Stack.of(self).region

    ### LAMBDA LAYERS ###

        getpublicip = _lambda.LayerVersion.from_layer_version_arn(
            self, 'getpublicip',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:getpublicip:10'
        )

        requests = _lambda.LayerVersion.from_layer_version_arn(
            self, 'requests',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:requests:2'
        )

    ### TOPIC ###

        topic = _sns.Topic.from_topic_arn(
            self, 'topic',
            topic_arn = 'arn:aws:sns:'+region+':'+account+':monitor'
        )

    ### IAM ###

        role = _iam.Role(
            self, 'role',
            role_name = 'cybercure',
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
                    's3:GetObject'
                ],
                resources = [
                    '*'
                ]
            )
        )

    ### LAMBDA ###

        cybercure = _lambda.Function(
            self, 'cybercure',
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('sources/ip/cybercure'),
            timeout = Duration.seconds(900),
            handler = 'cybercure.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                FEED_TABLE = 'feed',
                VERIFY_TABLE = 'verify',
                S3_BUCKET = 'addresses.tundralabs.org'
            ),
            memory_size = 2048,
            retry_attempts = 0,
            role = role,
            layers = [
                getpublicip,
                requests
            ]
        )

        logs = _logs.LogGroup(
            self, 'logs',
            log_group_name = '/aws/lambda/'+cybercure.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        cybercurealarm = _cloudwatch.Alarm(
            self, 'cybercurealarm',
            comparison_operator = _cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold = 0,
            evaluation_periods = 1,
            metric = cybercure.metric_errors(
                period = Duration.minutes(1)
            )
        )

        cybercurealarm.add_alarm_action(
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
            _targets.LambdaFunction(cybercure)
        )

    ### LAMBDA ###

        cybercuredomain = _lambda.Function(
            self, 'cybercuredomain',
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('sources/dns/cybercure'),
            timeout = Duration.seconds(900),
            handler = 'cybercure.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                FEED_TABLE = 'feed',
                S3_BUCKET = 'certificates.tundralabs.org'
            ),
            memory_size = 512,
            retry_attempts = 0,
            role = role,
            layers = [
                getpublicip,
                requests
            ]
        )

        cybercuredomainlogs = _logs.LogGroup(
            self, 'cybercuredomainlogs',
            log_group_name = '/aws/lambda/'+cybercuredomain.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        cybercuredomainalarm = _cloudwatch.Alarm(
            self, 'cybercuredomainalarm',
            comparison_operator = _cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold = 0,
            evaluation_periods = 1,
            metric = cybercuredomain.metric_errors(
                period = Duration.minutes(1)
            )
        )

        cybercuredomainalarm.add_alarm_action(
            _actions.SnsAction(topic)
        )

        cybercuredomainevent = _events.Rule(
            self, 'cybercuredomainevent',
            schedule = _events.Schedule.cron(
                minute = '30',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        cybercuredomainevent.add_target(
            _targets.LambdaFunction(cybercuredomain)
        )
