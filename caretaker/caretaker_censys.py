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
    aws_logs_destinations as _destinations,
    aws_ssm as _ssm
)

from constructs import Construct

class CaretakerCensys(Stack):

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
                {"id":"AwsSolutions-DDB3","reason":"The DynamoDB table does not have Point-in-time Recovery enabled."},
                {"id":"AwsSolutions-IAM4","reason":"The IAM user, role, or group uses AWS managed policies."},
                {"id":"AwsSolutions-IAM5","reason":"The IAM entity contains wildcard permissions and does not have a cdk-nag rule suppression with evidence for those permission."},
            ]
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
            role_name = 'censys',
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
                    'dynamodb:Query'
                ],
                resources = [
                    '*'
                ]
            )
        )

    ### PARAMETER STORE ###

        apiparam = _ssm.StringParameter.from_string_parameter_attributes(
            self, 'apiparam',
            parameter_name = '/censys/api',
            version = 1
        ).string_value

        keyparam = _ssm.StringParameter.from_string_parameter_attributes(
            self, 'keyparam',
            parameter_name = '/censys/key',
            version = 1
        ).string_value

    ### LAMBDA CONTAINER ###

        censys = _lambda.DockerImageFunction(
            self, 'censys',
            code = _lambda.DockerImageCode.from_image_asset('censys'),
            timeout = Duration.seconds(900),
            environment = dict(
                AWS_ACCOUNT = account,
                CENSYS_API_ID = apiparam,
                CENSYS_API_SECRET = keyparam,
                VERIFY_TABLE = 'verify'
            ),
            memory_size = 512,
            role = role
        )

        logs = _logs.LogGroup(
            self, 'logs',
            log_group_name = '/aws/lambda/'+censys.function_name,
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

    ### EVENTS ###

        #vncevent = _events.Rule(
        #    self, 'vncevent',
        #    schedule = _events.Schedule.cron(
        #        minute = '15',
        #        hour = '0',
        #        month = '*',
        #        week_day = '*',
        #        year = '*'
        #    )
        #)

        #vncevent.add_target(
        #    _targets.LambdaFunction(
        #        censys,
        #        event = _events.RuleTargetInput.from_object(
        #            {
        #                "service": "VNC"
        #            }
        #        )
        #    )
        #)
