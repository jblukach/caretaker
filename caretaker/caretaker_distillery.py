from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_dynamodb as _dynamodb,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_logs_destinations as _destinations
)

from constructs import Construct

class CaretakerDistillery(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account
        region = Stack.of(self).region

    ### LAMBDA LAYERS ###

        censys = _lambda.LayerVersion.from_layer_version_arn(
            self, 'censys',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:censys:4'
        )

        getpublicip = _lambda.LayerVersion.from_layer_version_arn(
            self, 'getpublicip',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:getpublicip:10'
        )

        netaddr = _lambda.LayerVersion.from_layer_version_arn(
            self, 'netaddr',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:netaddr:4'
        )

        requests = _lambda.LayerVersion.from_layer_version_arn(
            self, 'requests',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:requests:2'
        )

    ### ERROR ###

        error = _lambda.Function.from_function_arn(
            self, 'error',
            'arn:aws:lambda:'+region+':'+account+':function:shipittoo-error'
        )

        timeout = _lambda.Function.from_function_arn(
            self, 'timeout',
            'arn:aws:lambda:'+region+':'+account+':function:shipittoo-timeout'
        )

    ### DYNAMODB ###

        table = _dynamodb.Table(
            self, 'distillerydb',
            table_name = 'distillery',
            partition_key = {
                'name': 'pk',
                'type': _dynamodb.AttributeType.STRING
            },
            sort_key = {
                'name': 'sk',
                'type': _dynamodb.AttributeType.STRING
            },
            billing_mode = _dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy = RemovalPolicy.DESTROY,
            point_in_time_recovery = True,
            deletion_protection = True   
        )

        table.add_global_secondary_index(
            index_name = 'firstip',
            partition_key = {
                'name': 'pk',
                'type': _dynamodb.AttributeType.STRING
            },
            sort_key = {
                'name': 'firstip',
                'type': _dynamodb.AttributeType.NUMBER
            },
            projection_type = _dynamodb.ProjectionType.INCLUDE,
            non_key_attributes = ['cidr']
        )

        table.add_global_secondary_index(
            index_name = 'lastip',
            partition_key = {
                'name': 'pk',
                'type': _dynamodb.AttributeType.STRING
            },
            sort_key = {
                'name': 'lastip',
                'type': _dynamodb.AttributeType.NUMBER
            },
            projection_type = _dynamodb.ProjectionType.INCLUDE,
            non_key_attributes = ['cidr']
        )

    ### IAM ###

        role = _iam.Role(
            self, 'role',
            role_name = 'distillery',
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
                    'dynamodb:DeleteItem',
                    'dynamodb:PutItem',
                    'dynamodb:Query',
                    's3:PutObject',
                    'ssm:GetParameter'
                ],
                resources = [
                    '*'
                ]
            )
        )

    ### LAMBDA ###

        distillery = _lambda.Function(
            self, 'distillery',
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('distillery/cidr'),
            timeout = Duration.seconds(900),
            handler = 'cidr.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                DYNAMODB_TABLE = table.table_name
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
            log_group_name = '/aws/lambda/'+distillery.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        sub = _logs.SubscriptionFilter(
            self, 'sub',
            log_group = logs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        time = _logs.SubscriptionFilter(
            self, 'time',
            log_group = logs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )
    
        event = _events.Rule(
            self, 'event',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '10',
                month = '*',
                week_day = 'MON',
                year = '*'
            )
        )

        event.add_target(
            _targets.LambdaFunction(distillery)
        )

    ### LAMBDA ###

        cidr = _lambda.Function(
            self, 'cidr',
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('censys/cidr'),
            timeout = Duration.seconds(900),
            handler = 'cidr.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                DYNAMODB_TABLE = table.table_name
            ),
            memory_size = 512,
            retry_attempts = 0,
            role = role,
            layers = [
                censys,
                getpublicip
            ]
        )

        cidrlogs = _logs.LogGroup(
            self, 'cidrlogs',
            log_group_name = '/aws/lambda/'+cidr.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        cidrsub = _logs.SubscriptionFilter(
            self, 'cidrsub',
            log_group = cidrlogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        cidrtime = _logs.SubscriptionFilter(
            self, 'cidrtime',
            log_group = cidrlogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )
    
        cidrevent = _events.Rule(
            self, 'cidrevent',
            schedule = _events.Schedule.cron(
                minute = '10',
                hour = '10',
                month = '*',
                week_day = 'MON',
                year = '*'
            )
        )

        cidrevent.add_target(
            _targets.LambdaFunction(cidr)
        )

    ### LAMBDA ###

        address = _lambda.Function(
            self, 'address',
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('distillery/address'),
            timeout = Duration.seconds(900),
            handler = 'address.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                DYNAMODB_TABLE = table.table_name,
                S3_BUCKET = 'addresses.tundralabs.org'
            ),
            memory_size = 2048,
            retry_attempts = 0,
            role = role,
            layers = [
                getpublicip,
                netaddr
            ]
        )

        addresslogs = _logs.LogGroup(
            self, 'addresslogs',
            log_group_name = '/aws/lambda/'+address.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        addresssub = _logs.SubscriptionFilter(
            self, 'addresssub',
            log_group = addresslogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        addresstime = _logs.SubscriptionFilter(
            self, 'addresstime',
            log_group = addresslogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )
    
        addressevent = _events.Rule(
            self, 'addressevent',
            schedule = _events.Schedule.cron(
                minute = '15',
                hour = '10',
                month = '*',
                week_day = 'MON',
                year = '*'
            )
        )

        addressevent.add_target(
            _targets.LambdaFunction(address)
        )

    ### LAMBDA ###

        ipv4 = _lambda.Function(
            self, 'ipv4',
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('distillery/ipv4'),
            timeout = Duration.seconds(900),
            handler = 'ipv4.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                DYNAMODB_TABLE = table.table_name,
                S3_BUCKET = 'addresses.tundralabs.org'
            ),
            memory_size = 512,
            retry_attempts = 0,
            role = role,
            layers = [
                getpublicip
            ]
        )

        ipv4logs = _logs.LogGroup(
            self, 'ipv4logs',
            log_group_name = '/aws/lambda/'+ipv4.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        ipv4sub = _logs.SubscriptionFilter(
            self, 'ipv4sub',
            log_group = ipv4logs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        ipv4time = _logs.SubscriptionFilter(
            self, 'ipv4time',
            log_group = ipv4logs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )
    
        ipv4event = _events.Rule(
            self, 'ipv4event',
            schedule = _events.Schedule.cron(
                minute = '15',
                hour = '10',
                month = '*',
                week_day = 'MON',
                year = '*'
            )
        )

        ipv4event.add_target(
            _targets.LambdaFunction(ipv4)
        )

    ### LAMBDA ###

        ipv6 = _lambda.Function(
            self, 'ipv6',
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('distillery/ipv6'),
            timeout = Duration.seconds(900),
            handler = 'ipv6.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                DYNAMODB_TABLE = table.table_name,
                S3_BUCKET = 'addresses.tundralabs.org'
            ),
            memory_size = 512,
            retry_attempts = 0,
            role = role,
            layers = [
                getpublicip
            ]
        )

        ipv6logs = _logs.LogGroup(
            self, 'ipv6logs',
            log_group_name = '/aws/lambda/'+ipv6.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        ipv6sub = _logs.SubscriptionFilter(
            self, 'ipv6sub',
            log_group = ipv6logs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        ipv6time = _logs.SubscriptionFilter(
            self, 'ipv6time',
            log_group = ipv6logs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )
    
        ipv6event = _events.Rule(
            self, 'ipv6event',
            schedule = _events.Schedule.cron(
                minute = '15',
                hour = '10',
                month = '*',
                week_day = 'MON',
                year = '*'
            )
        )

        ipv6event.add_target(
            _targets.LambdaFunction(ipv6)
        )

    ### LAMBDA ###

        ipv46 = _lambda.Function(
            self, 'ipv46',
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('distillery/ipv46'),
            timeout = Duration.seconds(900),
            handler = 'ipv46.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                DYNAMODB_TABLE = table.table_name,
                S3_BUCKET = 'addresses.tundralabs.org'
            ),
            memory_size = 512,
            retry_attempts = 0,
            role = role,
            layers = [
                getpublicip
            ]
        )

        ipv46logs = _logs.LogGroup(
            self, 'ipv46logs',
            log_group_name = '/aws/lambda/'+ipv46.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        ipv46sub = _logs.SubscriptionFilter(
            self, 'ipv46sub',
            log_group = ipv46logs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        ipv46time = _logs.SubscriptionFilter(
            self, 'ipv46time',
            log_group = ipv46logs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )
    
        ipv46event = _events.Rule(
            self, 'ipv46event',
            schedule = _events.Schedule.cron(
                minute = '15',
                hour = '10',
                month = '*',
                week_day = 'MON',
                year = '*'
            )
        )

        ipv46event.add_target(
            _targets.LambdaFunction(ipv46)
        )
