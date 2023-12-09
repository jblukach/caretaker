import cdk_nag

from aws_cdk import (
    Aspects,
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

class CaretakerCertificates(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account
        region = Stack.of(self).region

    ### CDK NAG ###

        Aspects.of(self).add(
            cdk_nag.AwsSolutionsChecks(
                log_ignores = True,
                verbose = True
            )
        )

        cdk_nag.NagSuppressions.add_stack_suppressions(
            self, suppressions = [
                {"id":"AwsSolutions-IAM4","reason":"The IAM user, role, or group uses AWS managed policies."},
                {"id":"AwsSolutions-IAM5","reason":"The IAM entity contains wildcard permissions and does not have a cdk-nag rule suppression with evidence for those permission."},
                {"id":"AwsSolutions-L1","reason":"The non-container Lambda function is not configured to use the latest runtime version."},
                {"id":"AwsSolutions-DDB3","reason":"The DynamoDB table does not have Point-in-time Recovery enabled."},
            ]
        )

    ### LAMBDA LAYERS ###

        censys = _lambda.LayerVersion.from_layer_version_arn(
            self, 'censys',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:censys:1'
        )

        getpublicip = _lambda.LayerVersion.from_layer_version_arn(
            self, 'getpublicip',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:getpublicip:9'
        )

        requests = _lambda.LayerVersion.from_layer_version_arn(
            self, 'requests',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:requests:1'
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

    ### DATABASE ###

        tlddb = _dynamodb.Table(
            self, 'tlddb',
            table_name = 'tld',
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
            point_in_time_recovery = True
        )

    ### IAM ###

        role = _iam.Role(
            self, 'role',
            role_name = 'certificate',
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
                    's3:GetObject',
                    's3:PutObject',
                    'ssm:GetParameter'
                ],
                resources = [
                    '*'
                ]
            )
        )

    ### CERTIFICATE ###

        certificate = _lambda.Function(
            self, 'certificate',
            runtime = _lambda.Runtime.PYTHON_3_11,
            code = _lambda.Code.from_asset('censys/certificate'),
            timeout = Duration.seconds(900),
            handler = 'certificate.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                S3_BUCKET = 'certificates.tundralabs.org'
            ),
            memory_size = 2048,
            role = role,
            layers = [
                censys,
                getpublicip
            ]
        )

        logs = _logs.LogGroup(
            self, 'logs',
            log_group_name = '/aws/lambda/'+certificate.function_name,
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
            _targets.LambdaFunction(certificate)
        )

    ### DOMAIN ###

        domain = _lambda.Function(
            self, 'domain',
            runtime = _lambda.Runtime.PYTHON_3_11,
            code = _lambda.Code.from_asset('censys/domain'),
            timeout = Duration.seconds(900),
            handler = 'domain.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                S3_BUCKET = 'certificates.tundralabs.org',
                TLD_TABLE = tlddb.table_name
            ),
            memory_size = 512,
            role = role,
            layers = [
                getpublicip
            ]
        )

        domainlogs = _logs.LogGroup(
            self, 'domainlogs',
            log_group_name = '/aws/lambda/'+domain.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        domainsub = _logs.SubscriptionFilter(
            self, 'domainsub',
            log_group = domainlogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        domaintime = _logs.SubscriptionFilter(
            self, 'domaintime',
            log_group = domainlogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

        domainevent = _events.Rule(
            self, 'domainevent',
            schedule = _events.Schedule.cron(
                minute = '15',
                hour = '10',
                month = '*',
                week_day = 'MON',
                year = '*'
            )
        )

        domainevent.add_target(
            _targets.LambdaFunction(domain)
        )

    ### TLD ###

        tld = _lambda.Function(
            self, 'tld',
            runtime = _lambda.Runtime.PYTHON_3_11,
            code = _lambda.Code.from_asset('sources/tld/iana'),
            timeout = Duration.seconds(900),
            handler = 'iana.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                TLD_TABLE = tlddb.table_name
            ),
            memory_size = 256,
            role = role,
            layers = [
                getpublicip,
                requests
            ]
        )

        tldlogs = _logs.LogGroup(
            self, 'tldlogs',
            log_group_name = '/aws/lambda/'+tld.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        tldsub = _logs.SubscriptionFilter(
            self, 'tldsub',
            log_group = tldlogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        tldtime = _logs.SubscriptionFilter(
            self, 'tldtime',
            log_group = tldlogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

        tldevent = _events.Rule(
            self, 'tldevent',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '10',
                month = '*',
                week_day = 'MON',
                year = '*'
            )
        )

        tldevent.add_target(
            _targets.LambdaFunction(tld)
        )
