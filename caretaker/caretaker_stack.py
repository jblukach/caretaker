import cdk_nag

from aws_cdk import (
    Aspects,
    Duration,
    RemovalPolicy,
    Stack,
    aws_dynamodb as _dynamodb,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_lambda_event_sources as _sources,
    aws_logs as _logs,
    aws_logs_destinations as _destinations
)

from constructs import Construct

class CaretakerStack(Stack):

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
                {"id":"AwsSolutions-DDB3","reason":"The DynamoDB table does not have Point-in-time Recovery enabled."},
                {"id":"AwsSolutions-L1","reason":"The non-container Lambda function is not configured to use the latest runtime version."},
                {"id":"AwsSolutions-VPC7","reason":"The VPC does not have an associated Flow Log."},
                {"id":"AwsSolutions-EC23","reason":"The Security Group allows for 0.0.0.0/0 or ::/0 inbound access."},
                {"id":"AwsSolutions-EC27","reason":"The Security Group does not have a description."},
                {"id":"AwsSolutions-ECS4","reason":"The ECS Cluster has CloudWatch Container Insights disabled."},
                {"id":"AwsSolutions-ECS2","reason":"The ECS Task Definition includes a container definition that directly specifies environment variables."},
                {"id":"AwsSolutions-ECS7","reason":"One or more containers in the ECS Task Definition do not have container logging enabled."},
            ]
        )

    ### LAMBDA LAYERS ###

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

    ### DYNAMODB ###

        feed = _dynamodb.Table(
            self, 'feeddb',
            table_name = 'feed',
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

        map = _dynamodb.Table(
            self, 'mapdb',
            table_name = 'map',
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

        verify = _dynamodb.Table(
            self, 'verifydb',
            table_name = 'verify',
            partition_key = {
                'name': 'pk',
                'type': _dynamodb.AttributeType.STRING
            },
            sort_key = {
                'name': 'sk',
                'type': _dynamodb.AttributeType.STRING
            },
            billing_mode = _dynamodb.BillingMode.PAY_PER_REQUEST,
            stream = _dynamodb.StreamViewType.NEW_AND_OLD_IMAGES,
            removal_policy = RemovalPolicy.DESTROY,
            point_in_time_recovery = True,
            deletion_protection = True
        )

    ### IAM ###

        role = _iam.Role(
            self, 'role',
            role_name = 'maxmind',
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
                    'dynamodb:PutItem'
                ],
                resources = [
                    '*'
                ]
            )
        )

    ### LAMBDA ###

        maxmind = _lambda.Function(
            self, 'maxmind',
            runtime = _lambda.Runtime.PYTHON_3_11,
            code = _lambda.Code.from_asset('maxmind'),
            timeout = Duration.seconds(900),
            handler = 'maxmind.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                MAP_TABLE = map.table_name
            ),
            memory_size = 512,
            role = role,
            layers = [
                getpublicip,
                requests
            ]
        )

        logs = _logs.LogGroup(
            self, 'logs',
            log_group_name = '/aws/lambda/'+maxmind.function_name,
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

        maxmind.add_event_source(
            _sources.DynamoEventSource(
                table = verify,
                starting_position = _lambda.StartingPosition.LATEST
            )
        )
