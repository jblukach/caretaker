from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_logs_destinations as _destinations,
    aws_ssm as _ssm,
    aws_stepfunctions as _sfn,
    aws_stepfunctions_tasks as _tasks
)

from constructs import Construct

class CaretakerTundraLabs(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account
        region = Stack.of(self).region

    ### LAMBDA LAYERS ###

        dnspython = _lambda.LayerVersion.from_layer_version_arn(
            self, 'dnspython',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:dnspython:2'
        )

        getpublicip = _lambda.LayerVersion.from_layer_version_arn(
            self, 'getpublicip',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:getpublicip:10'
        )

        smartopen = _lambda.LayerVersion.from_layer_version_arn(
            self, 'smartopen',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:smartopen:1'
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

    ### IAM ROLE ###

        role = _iam.Role(
            self, 'role', 
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
                    's3:GetObject',
                    'ssm:GetParameter',
                    'states:StartExecution'
                ],
                resources = [
                    '*'
                ]
            )
        )

    ### START LAMBDA ###

        start = _lambda.Function(
            self, 'start',
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('sources/mx/start'),
            timeout = Duration.seconds(900),
            handler = 'start.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                DYNAMODB_TABLE = 'feed',
                S3_BUCKET = 'emails.tundralabs.org',
                S3_OBJECT = 'dns.txt',
                STEP_FUNCTION = '/caretaker/mx/step'
            ),
            memory_size = 256,
            retry_attempts = 0,
            role = role,
            layers = [
                getpublicip
            ]
        )

        startlogs = _logs.LogGroup(
            self, 'startlogs',
            log_group_name = '/aws/lambda/'+start.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        startsub = _logs.SubscriptionFilter(
            self, 'startsub',
            log_group = startlogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        starttime = _logs.SubscriptionFilter(
            self, 'starttime',
            log_group = startlogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

        startevent = _events.Rule(
            self, 'startevent',
            schedule = _events.Schedule.cron(
                minute = '30',
                hour = '10',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        startevent.add_target(
            _targets.LambdaFunction(
                start
            )
        )

    ### STEP LAMBDA ###

        step = _lambda.Function(
            self, 'step',
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('sources/mx/step'),
            timeout = Duration.seconds(3),
            handler = 'step.handler',
            environment = dict(
                AWS_ACCOUNT = account
            ),
            memory_size = 128,
            retry_attempts = 0,
            role = role,
            layers = [
                getpublicip
            ]
        )

        steplogs = _logs.LogGroup(
            self, 'steplogs',
            log_group_name = '/aws/lambda/'+step.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        stepsub = _logs.SubscriptionFilter(
            self, 'stepsub',
            log_group = steplogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        steptime = _logs.SubscriptionFilter(
            self, 'steptime',
            log_group = steplogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

    ### READ LAMBDA ###

        read = _lambda.Function(
            self, 'read',
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('sources/mx/read/tundralabs'),
            timeout = Duration.seconds(900),
            handler = 'read.handler',
            environment = dict(
                AWS_ACCOUNT = account
            ),
            memory_size = 512,
            retry_attempts = 0,
            role = role,
            layers = [
                dnspython,
                getpublicip,
                smartopen
            ]
        )

        readlogs = _logs.LogGroup(
            self, 'readlogs',
            log_group_name = '/aws/lambda/'+read.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        readsub = _logs.SubscriptionFilter(
            self, 'readsub',
            log_group = readlogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        readtime = _logs.SubscriptionFilter(
            self, 'readtime',
            log_group = readlogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

    ### STEP FUNCTION ###

        initial = _tasks.LambdaInvoke(
            self, 'initial',
            lambda_function = step,
            output_path = '$.Payload',
        )

        reader = _tasks.LambdaInvoke(
            self, 'reader',
            lambda_function = read,
            output_path = '$.Payload',
        )

        failed = _sfn.Fail(
            self, 'failed',
            cause = 'Failed',
            error = 'FAILED'
        )

        succeed = _sfn.Succeed(
            self, 'succeeded',
            comment = 'SUCCEEDED'
        )

        definition = initial.next(reader) \
            .next(_sfn.Choice(self, 'Completed?')
                .when(_sfn.Condition.string_equals('$.status', 'FAILED'), failed)
                .when(_sfn.Condition.string_equals('$.status', 'SUCCEEDED'), succeed)
                .otherwise(reader)
            )

        statelogs = _logs.LogGroup(
            self, 'statelogs',
            log_group_name = '/aws/state/tundralabs',
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        statelogssub = _logs.SubscriptionFilter(
            self, 'statelogssub',
            log_group = statelogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        statelogstime= _logs.SubscriptionFilter(
            self, 'statelogstime',
            log_group = statelogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

        state = _sfn.StateMachine(
            self, 'tundralabs',
            definition_body = _sfn.DefinitionBody.from_chainable(definition),
            logs = _sfn.LogOptions(
                destination = statelogs,
                level = _sfn.LogLevel.ALL
            )
        )

        parameter = _ssm.StringParameter(
            self, 'parameter',
            description = 'Tundra Labs Step Function',
            parameter_name = '/caretaker/mx/step',
            string_value = state.state_machine_arn,
            tier = _ssm.ParameterTier.STANDARD
        )
