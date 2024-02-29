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

class CaretakerAbuseCH(Stack):

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
            role_name = 'abusech',
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

        feodotracker = _lambda.Function(
            self, 'feodotracker',
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('sources/ip/abusech/feodotracker'),
            timeout = Duration.seconds(900),
            handler = 'feodotracker.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                FEED_TABLE = 'feed',
                VERIFY_TABLE = 'verify',
                S3_BUCKET = 'addresses.tundralabs.org'
            ),
            memory_size = 4096,
            retry_attempts = 0,
            role = role,
            layers = [
                getpublicip,
                requests
            ]
        )

        feodotrackerlogs = _logs.LogGroup(
            self, 'feodotrackerlogs',
            log_group_name = '/aws/lambda/'+feodotracker.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        feodotrackeralarm = _cloudwatch.Alarm(
            self, 'feodotrackeralarm',
            comparison_operator = _cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold = 0,
            evaluation_periods = 1,
            metric = feodotracker.metric_errors(
                period = Duration.minutes(1)
            )
        )

        feodotrackeralarm.add_alarm_action(
            _actions.SnsAction(topic)
        )

        feodotrackerevent = _events.Rule(
            self, 'feodotrackerevent',
            schedule = _events.Schedule.cron(
                minute = '30',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        feodotrackerevent.add_target(
            _targets.LambdaFunction(feodotracker)
        )

    ### LAMBDA ###

        sslbl = _lambda.Function(
            self, 'sslbl',
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('sources/ip/abusech/sslbl'),
            timeout = Duration.seconds(900),
            handler = 'sslbl.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                FEED_TABLE = 'feed',
                VERIFY_TABLE = 'verify',
                S3_BUCKET = 'addresses.tundralabs.org'
            ),
            memory_size = 4096,
            retry_attempts = 0,
            role = role,
            layers = [
                getpublicip,
                requests
            ]
        )

        sslbllogs = _logs.LogGroup(
            self, 'sslbllogs',
            log_group_name = '/aws/lambda/'+sslbl.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        sslblalarm = _cloudwatch.Alarm(
            self, 'sslblalarm',
            comparison_operator = _cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold = 0,
            evaluation_periods = 1,
            metric = sslbl.metric_errors(
                period = Duration.minutes(1)
            )
        )

        sslblalarm.add_alarm_action(
            _actions.SnsAction(topic)
        )

        sslblevent = _events.Rule(
            self, 'sslblevent',
            schedule = _events.Schedule.cron(
                minute = '30',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        sslblevent.add_target(
            _targets.LambdaFunction(sslbl)
        )

    ### LAMBDA ###

        threatfox = _lambda.Function(
            self, 'threatfox',
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('sources/dns/abusech/threatfox'),
            timeout = Duration.seconds(900),
            handler = 'threatfox.handler',
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

        threatfoxlogs = _logs.LogGroup(
            self, 'threatfoxlogs',
            log_group_name = '/aws/lambda/'+threatfox.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        threatfoxalarm = _cloudwatch.Alarm(
            self, 'threatfoxalarm',
            comparison_operator = _cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold = 0,
            evaluation_periods = 1,
            metric = threatfox.metric_errors(
                period = Duration.minutes(1)
            )
        )

        threatfoxalarm.add_alarm_action(
            _actions.SnsAction(topic)
        )

        threatfoxevent = _events.Rule(
            self, 'threatfoxevent',
            schedule = _events.Schedule.cron(
                minute = '30',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        threatfoxevent.add_target(
            _targets.LambdaFunction(threatfox)
        )

    ### LAMBDA ###

        urlhaus = _lambda.Function(
            self, 'urlhaus',
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('sources/dns/abusech/urlhaus'),
            timeout = Duration.seconds(900),
            handler = 'urlhaus.handler',
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

        urlhauslogs = _logs.LogGroup(
            self, 'urlhauslogs',
            log_group_name = '/aws/lambda/'+urlhaus.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        urlhausalarm = _cloudwatch.Alarm(
            self, 'urlhausalarm',
            comparison_operator = _cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold = 0,
            evaluation_periods = 1,
            metric = urlhaus.metric_errors(
                period = Duration.minutes(1)
            )
        )

        urlhausalarm.add_alarm_action(
            _actions.SnsAction(topic)
        )

        urlhausevent = _events.Rule(
            self, 'urlhausevent',
            schedule = _events.Schedule.cron(
                minute = '30',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        urlhausevent.add_target(
            _targets.LambdaFunction(urlhaus)
        )
