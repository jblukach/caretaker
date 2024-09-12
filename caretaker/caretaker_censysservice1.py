from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_cloudwatch as _cloudwatch,
    aws_cloudwatch_actions as _actions,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_sns as _sns,
    aws_ssm as _ssm
)

from constructs import Construct

class CaretakerCensysService1(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account
        region = Stack.of(self).region

    ### LAYERS ###

        extensions = _ssm.StringParameter.from_string_parameter_attributes(
            self, 'extensions',
            parameter_name = '/extensions/account'
        )

        censys = _lambda.LayerVersion.from_layer_version_arn(
            self, 'censys',
            layer_version_arn = 'arn:aws:lambda:'+region+':'+extensions.string_value+':layer:censys:9'
        )

        getpublicip = _lambda.LayerVersion.from_layer_version_arn(
            self, 'getpublicip',
            layer_version_arn = 'arn:aws:lambda:'+region+':'+extensions.string_value+':layer:getpublicip:12'
        )

    ### TOPIC ###

        topic = _sns.Topic.from_topic_arn(
            self, 'topic',
            topic_arn = 'arn:aws:sns:'+region+':'+account+':caretaker'
        )

    ### IAM ###

        role = _iam.Role(
            self, 'role',
            role_name = 'censysservice1',
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
                    'ssm:GetParameter'
                ],
                resources = [
                    '*'
                ]
            )
        )

    ### LAMBDA ###

        searches = []
        searches.append('ELASTICSEARCH')
        searches.append('FTP')
        searches.append('IMAP')
        searches.append('KUBERNETES')
        searches.append('LDAP')
        searches.append('MONGODB')
        searches.append('MSSQL')
        searches.append('MYSQL')
        searches.append('NETBIOS')
        searches.append('ORACLE')
        searches.append('POP3')
        searches.append('ROCKETMQ')

        for search in searches:

            service = _lambda.Function(
                self, 'censys'+search,
                runtime = _lambda.Runtime.PYTHON_3_12,
                architecture = _lambda.Architecture.ARM_64,
                code = _lambda.Code.from_asset('censys/service'),
                timeout = Duration.seconds(900),
                handler = 'service.handler',
                environment = dict(
                    AWS_ACCOUNT = account,
                    CENSYS_API_ID = '-',
                    CENSYS_API_SECRET = '-',
                    CENSYS_SERVICE = search
                ),
                memory_size = 512,
                retry_attempts = 0,
                role = role,
                layers = [
                    censys,
                    getpublicip
                ]
            )

            logs = _logs.LogGroup(
                self, 'censyslogs'+search,
                log_group_name = '/aws/lambda/'+service.function_name,
                retention = _logs.RetentionDays.ONE_DAY,
                removal_policy = RemovalPolicy.DESTROY
            )

            alarm = _cloudwatch.Alarm(
                self, 'censysalarm'+search,
                comparison_operator = _cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
                threshold = 0,
                evaluation_periods = 1,
                metric = service.metric_errors(
                    period = Duration.minutes(1)
                )
            )

            alarm.add_alarm_action(
                _actions.SnsAction(topic)
            )

            event = _events.Rule(
                self, 'censysevent'+search,
                schedule = _events.Schedule.cron(
                    minute = str(searches.index(search)*5),
                    hour = '15',
                    month = '*',
                    week_day = '*',
                    year = '*'
                )
            )

            event.add_target(
                _targets.LambdaFunction(
                    service
                )
            )
