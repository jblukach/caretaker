import cdk_nag

from aws_cdk import (
    Aspects,
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

class CaretakerOpenPhish(Stack):

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
            role_name = 'openphish',
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
                    'dynamodb:Query',
                    's3:GetObject'
                ],
                resources = [
                    '*'
                ]
            )
        )

    ### LAMBDA ###

        openphish = _lambda.Function(
            self, 'openphish',
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('sources/dns/openphish'),
            timeout = Duration.seconds(900),
            handler = 'openphish.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                FEED_TABLE = 'feed',
                S3_BUCKET = 'certificates.tundralabs.org'
            ),
            memory_size = 512,
            role = role,
            layers = [
                getpublicip,
                requests
            ]
        )

        openphishlogs = _logs.LogGroup(
            self, 'openphishlogs',
            log_group_name = '/aws/lambda/'+openphish.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        openphishsub = _logs.SubscriptionFilter(
            self, 'openphishsub',
            log_group = openphishlogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        openphishtime = _logs.SubscriptionFilter(
            self, 'openphishtime',
            log_group = openphishlogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

        openphishevent = _events.Rule(
            self, 'openphishevent',
            schedule = _events.Schedule.cron(
                minute = '30',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        openphishevent.add_target(
            _targets.LambdaFunction(openphish)
        )
