from aws_cdk import (
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

class CaretakerCensysService2(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account
        region = Stack.of(self).region

    ### LAYERS ###

        censys = _lambda.LayerVersion.from_layer_version_arn(
            self, 'censys',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:censys:5'
        )

        getpublicip = _lambda.LayerVersion.from_layer_version_arn(
            self, 'getpublicip',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:getpublicip:10'
        )

    ### ERROR ###

        error = _lambda.Function.from_function_arn(
            self, 'error',
            'arn:aws:lambda:'+region+':'+account+':function:shipittwo-error'
        )

        timeout = _lambda.Function.from_function_arn(
            self, 'timeout',
            'arn:aws:lambda:'+region+':'+account+':function:shipittwo-timeout'
        )

    ### IAM ###

        role = _iam.Role(
            self, 'role',
            role_name = 'censysservice2',
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
        searches.append('ACTIVEMQ')
        searches.append('AMQP')
        searches.append('BACNET')
        searches.append('COAP')
        searches.append('COBALT_STRIKE')
        searches.append('CWMP')
        searches.append('DARKGATE')
        searches.append('DHCPDISCOVER')
        searches.append('DNP3')
        searches.append('EPMD')
        searches.append('ETHEREUM')
        searches.append('FOX')
        searches.append('IPMI')
        searches.append('IPP')
        searches.append('KRPC')
        searches.append('MEMCACHED')
        searches.append('MMS')
        searches.append('MODBUS')
        searches.append('MONERO_P2P')
        searches.append('MQTT')
        searches.append('OPC_UA')
        searches.append('PC_ANYWHERE')
        searches.append('REDIS')
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
                retention = _logs.RetentionDays.ONE_MONTH,
                removal_policy = RemovalPolicy.DESTROY
            )

            sub = _logs.SubscriptionFilter(
                self, 'censyssub'+search,
                log_group = logs,
                destination = _destinations.LambdaDestination(error),
                filter_pattern = _logs.FilterPattern.all_terms('ERROR')
            )

            time = _logs.SubscriptionFilter(
                self, 'censystime'+search,
                log_group = logs,
                destination = _destinations.LambdaDestination(timeout),
                filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
            )

            event = _events.Rule(
                self, 'censysevent'+search,
                schedule = _events.Schedule.cron(
                    minute = str(searches.index(search)*2),
                    hour = '11',
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
