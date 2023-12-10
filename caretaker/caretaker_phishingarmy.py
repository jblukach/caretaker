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

class CaretakerPhishingArmy(Stack):

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

    ### IAM ###

        role = _iam.Role(
            self, 'role',
            role_name = 'phishingarmy',
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

        phishingarmy = _lambda.Function(
            self, 'phishingarmy',
            runtime = _lambda.Runtime.PYTHON_3_11,
            code = _lambda.Code.from_asset('sources/dns/phishingarmy'),
            timeout = Duration.seconds(900),
            handler = 'phishingarmy.handler',
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

        phishingarmylogs = _logs.LogGroup(
            self, 'phishingarmylogs',
            log_group_name = '/aws/lambda/'+phishingarmy.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        phishingarmysub = _logs.SubscriptionFilter(
            self, 'phishingarmysub',
            log_group = phishingarmylogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        phishingarmytime = _logs.SubscriptionFilter(
            self, 'phishingarmytime',
            log_group = phishingarmylogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

        phishingarmyevent = _events.Rule(
            self, 'phishingarmyevent',
            schedule = _events.Schedule.cron(
                minute = '30',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        #phishingarmyevent.add_target(
        #    _targets.LambdaFunction(phishingarmy)
        #)
