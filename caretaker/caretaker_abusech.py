from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_logs_destinations as _destinations
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

    ### ERROR ###

        error = _lambda.Function.from_function_arn(
            self, 'error',
            'arn:aws:lambda:'+region+':'+account+':function:shipit-error'
        )

        timeout = _lambda.Function.from_function_arn(
            self, 'timeout',
            'arn:aws:lambda:'+region+':'+account+':function:shipit-timeout'
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
            memory_size = 2048,
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

        feodotrackersub = _logs.SubscriptionFilter(
            self, 'feodotrackersub',
            log_group = feodotrackerlogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        feodotrackertime = _logs.SubscriptionFilter(
            self, 'feodotrackertime',
            log_group = feodotrackerlogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
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
            memory_size = 2048,
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

        sslblsub = _logs.SubscriptionFilter(
            self, 'sslblsub',
            log_group = sslbllogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        sslbltime = _logs.SubscriptionFilter(
            self, 'sslbltime',
            log_group = sslbllogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
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

        threatfoxsub = _logs.SubscriptionFilter(
            self, 'threatfoxsub',
            log_group = threatfoxlogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        threatfoxtime = _logs.SubscriptionFilter(
            self, 'threatfoxtime',
            log_group = threatfoxlogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
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

        urlhaussub = _logs.SubscriptionFilter(
            self, 'urlhaussub',
            log_group = urlhauslogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        urlhaustime = _logs.SubscriptionFilter(
            self, 'urlhaustime',
            log_group = urlhauslogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
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
