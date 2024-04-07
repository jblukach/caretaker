from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_cloudwatch as _cloudwatch,
    aws_cloudwatch_actions as _actions,
    aws_dynamodb as _dynamodb,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_sns as _sns
)

from constructs import Construct

class CaretakerCertificates(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account
        region = Stack.of(self).region

    ### LAMBDA LAYERS ###

        censys = _lambda.LayerVersion.from_layer_version_arn(
            self, 'censys',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:censys:6'
        )

        getpublicip = _lambda.LayerVersion.from_layer_version_arn(
            self, 'getpublicip',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:getpublicip:11'
        )

        requests = _lambda.LayerVersion.from_layer_version_arn(
            self, 'requests',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:requests:3'
        )

    ### TOPIC ###

        topic = _sns.Topic.from_topic_arn(
            self, 'topic',
            topic_arn = 'arn:aws:sns:'+region+':'+account+':monitor'
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
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('censys/certificate'),
            timeout = Duration.seconds(900),
            handler = 'certificate.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                S3_BUCKET = 'certificates.tundralabs.org'
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
            self, 'logs',
            log_group_name = '/aws/lambda/'+certificate.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        certificatealarm = _cloudwatch.Alarm(
            self, 'certificatealarm',
            comparison_operator = _cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold = 0,
            evaluation_periods = 1,
            metric = certificate.metric_errors(
                period = Duration.minutes(1)
            )
        )

        certificatealarm.add_alarm_action(
            _actions.SnsAction(topic)
        )

        event = _events.Rule(
            self, 'event',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '9',
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
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('censys/domain'),
            timeout = Duration.seconds(900),
            handler = 'domain.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                S3_BUCKET = 'certificates.tundralabs.org',
                TLD_TABLE = tlddb.table_name
            ),
            memory_size = 512,
            retry_attempts = 0,
            role = role,
            layers = [
                getpublicip
            ]
        )

        domainlogs = _logs.LogGroup(
            self, 'domainlogs',
            log_group_name = '/aws/lambda/'+domain.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        domainalarm = _cloudwatch.Alarm(
            self, 'domainalarm',
            comparison_operator = _cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold = 0,
            evaluation_periods = 1,
            metric = domain.metric_errors(
                period = Duration.minutes(1)
            )
        )

        domainalarm.add_alarm_action(
            _actions.SnsAction(topic)
        )

        domainevent = _events.Rule(
            self, 'domainevent',
            schedule = _events.Schedule.cron(
                minute = '15',
                hour = '9',
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
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('sources/tld/iana'),
            timeout = Duration.seconds(900),
            handler = 'iana.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                TLD_TABLE = tlddb.table_name
            ),
            memory_size = 256,
            retry_attempts = 0,
            role = role,
            layers = [
                getpublicip,
                requests
            ]
        )

        tldlogs = _logs.LogGroup(
            self, 'tldlogs',
            log_group_name = '/aws/lambda/'+tld.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        tldalarm = _cloudwatch.Alarm(
            self, 'tldalarm',
            comparison_operator = _cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold = 0,
            evaluation_periods = 1,
            metric = tld.metric_errors(
                period = Duration.minutes(1)
            )
        )

        tldalarm.add_alarm_action(
            _actions.SnsAction(topic)
        )

        tldevent = _events.Rule(
            self, 'tldevent',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '9',
                month = '*',
                week_day = 'MON',
                year = '*'
            )
        )

        tldevent.add_target(
            _targets.LambdaFunction(tld)
        )

    ### MAIL ###

        mail = _lambda.Function(
            self, 'mail',
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('censys/mail'),
            timeout = Duration.seconds(900),
            handler = 'mail.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                S3_BUCKET = 'emails.tundralabs.org'
            ),
            memory_size = 512,
            retry_attempts = 0,
            role = role,
            layers = [
                censys,
                getpublicip
            ]
        )

        maillogs = _logs.LogGroup(
            self, 'maillogs',
            log_group_name = '/aws/lambda/'+mail.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        mailalarm = _cloudwatch.Alarm(
            self, 'mailalarm',
            comparison_operator = _cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold = 0,
            evaluation_periods = 1,
            metric = mail.metric_errors(
                period = Duration.minutes(1)
            )
        )

        mailalarm.add_alarm_action(
            _actions.SnsAction(topic)
        )

        mailevent = _events.Rule(
            self, 'mailevent',
            schedule = _events.Schedule.cron(
                minute = '30',
                hour = '9',
                month = '*',
                week_day = 'MON',
                year = '*'
            )
        )

        mailevent.add_target(
            _targets.LambdaFunction(mail)
        )
