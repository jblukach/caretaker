from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
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

        extensions = _ssm.StringParameter.from_string_parameter_attributes(
            self, 'extensions',
            parameter_name = '/extensions/account'
        )

        dnspython = _lambda.LayerVersion.from_layer_version_arn(
            self, 'dnspython',
            layer_version_arn = 'arn:aws:lambda:'+region+':'+extensions.string_value+':layer:dnspython:6'
        )

        getpublicip = _lambda.LayerVersion.from_layer_version_arn(
            self, 'getpublicip',
            layer_version_arn = 'arn:aws:lambda:'+region+':'+extensions.string_value+':layer:getpublicip:14'
        )

        requests = _lambda.LayerVersion.from_layer_version_arn(
            self, 'requests',
            layer_version_arn = 'arn:aws:lambda:'+region+':'+extensions.string_value+':layer:requests:7'
        )

        smartopen = _lambda.LayerVersion.from_layer_version_arn(
            self, 'smartopen',
            layer_version_arn = 'arn:aws:lambda:'+region+':'+extensions.string_value+':layer:smartopen:6'
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
            runtime = _lambda.Runtime.PYTHON_3_13,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('sources/mx/start'),
            timeout = Duration.seconds(900),
            handler = 'start.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                DYNAMODB_TABLE = 'feed',
                S3_BUCKET = 'caretakerbucket',
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
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        startevent = _events.Rule(
            self, 'startevent',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '15',
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
            runtime = _lambda.Runtime.PYTHON_3_13,
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
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

    ### READ LAMBDA ###

        read = _lambda.Function(
            self, 'read',
            runtime = _lambda.Runtime.PYTHON_3_13,
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
                requests,
                smartopen
            ]
        )

        readlogs = _logs.LogGroup(
            self, 'readlogs',
            log_group_name = '/aws/lambda/'+read.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
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
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
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
