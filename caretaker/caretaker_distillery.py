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
    aws_ssm as _ssm
)

from constructs import Construct

class CaretakerDistillery(Stack):

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

        netaddr = _lambda.LayerVersion.from_layer_version_arn(
            self, 'netaddr',
            layer_version_arn = 'arn:aws:lambda:'+region+':'+extensions.string_value+':layer:netaddr:8'
        )

        requests = _lambda.LayerVersion.from_layer_version_arn(
            self, 'requests',
            layer_version_arn = 'arn:aws:lambda:'+region+':'+extensions.string_value+':layer:requests:7'
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
                    'lambda:UpdateFunctionCode',
                    's3:GetObject',
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
            runtime = _lambda.Runtime.PYTHON_3_13,
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
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )
    
        event = _events.Rule(
            self, 'event',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '14',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        event.add_target(
            _targets.LambdaFunction(distillery)
        )

    ### LAMBDA ###

        address = _lambda.Function(
            self, 'address',
            runtime = _lambda.Runtime.PYTHON_3_13,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('distillery/address'),
            timeout = Duration.seconds(900),
            handler = 'address.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                DYNAMODB_TABLE = table.table_name,
                S3_BUCKET = 'caretakerbucket'
            ),
            memory_size = 512,
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
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )
    
        addressevent = _events.Rule(
            self, 'addressevent',
            schedule = _events.Schedule.cron(
                minute = '15',
                hour = '14',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        addressevent.add_target(
            _targets.LambdaFunction(address)
        )

    ### LAMBDA ###

        ipv6 = _lambda.Function(
            self, 'ipv6',
            runtime = _lambda.Runtime.PYTHON_3_13,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('distillery/ipv6'),
            timeout = Duration.seconds(900),
            handler = 'ipv6.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                DYNAMODB_TABLE = table.table_name,
                S3_BUCKET = 'caretakerbucket'
            ),
            memory_size = 256,
            retry_attempts = 0,
            role = role,
            layers = [
                getpublicip
            ]
        )

        ipv6logs = _logs.LogGroup(
            self, 'ipv6logs',
            log_group_name = '/aws/lambda/'+ipv6.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )
    
        ipv6event = _events.Rule(
            self, 'ipv6event',
            schedule = _events.Schedule.cron(
                minute = '15',
                hour = '14',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        ipv6event.add_target(
            _targets.LambdaFunction(ipv6)
        )

    ### LAMBDA ###

        ipv46 = _lambda.Function(
            self, 'ipv46',
            runtime = _lambda.Runtime.PYTHON_3_13,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('distillery/ipv46'),
            timeout = Duration.seconds(900),
            handler = 'ipv46.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                DYNAMODB_TABLE = table.table_name,
                S3_BUCKET = 'caretakerbucket'
            ),
            memory_size = 256,
            retry_attempts = 0,
            role = role,
            layers = [
                getpublicip
            ]
        )

        ipv46logs = _logs.LogGroup(
            self, 'ipv46logs',
            log_group_name = '/aws/lambda/'+ipv46.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )
    
        ipv46event = _events.Rule(
            self, 'ipv46event',
            schedule = _events.Schedule.cron(
                minute = '15',
                hour = '14',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        ipv46event.add_target(
            _targets.LambdaFunction(ipv46)
        )
