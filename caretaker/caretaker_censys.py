import cdk_nag

from aws_cdk import (
    Aspects,
    Duration,
    RemovalPolicy,
    Stack,
    aws_dynamodb as _dynamodb,
    aws_ec2 as _ec2,
    aws_ecs as _ecs,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_logs_destinations as _destinations
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
                {"id":"AwsSolutions-IAM4","reason":"The IAM user, role, or group uses AWS managed policies."},
                {"id":"AwsSolutions-IAM5","reason":"The IAM entity contains wildcard permissions and does not have a cdk-nag rule suppression with evidence for those permission."},
                {"id":"AwsSolutions-L1","reason":"The non-container Lambda function is not configured to use the latest runtime version."},
                {"id":"AwsSolutions-DDB3","reason":"The DynamoDB table does not have Point-in-time Recovery enabled."},
                {"id":"AwsSolutions-VPC7","reason":"The VPC does not have an associated Flow Log."},
                {"id":"AwsSolutions-EC23","reason":"The Security Group allows for 0.0.0.0/0 or ::/0 inbound access."},
                {"id":"AwsSolutions-EC27","reason":"The Security Group does not have a description."},
                {"id":"AwsSolutions-ECS4","reason":"The ECS Cluster has CloudWatch Container Insights disabled."},
                {"id":"AwsSolutions-ECS2","reason":"The ECS Task Definition includes a container definition that directly specifies environment variables."},
                {"id":"AwsSolutions-ECS7","reason":"One or more containers in the ECS Task Definition do not have container logging enabled."},
            ]
        )

    ### LAYERS ###

        layer = _lambda.LayerVersion.from_layer_version_arn(
            self, 'layer',
            layer_version_arn = 'arn:aws:lambda:'+region+':070176467818:layer:getpublicip:9'
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

    ### NETWORK ###

        vpc = _ec2.Vpc(
            self, 'vpc',
            ip_addresses = _ec2.IpAddresses.cidr('192.168.242.0/24'),
            max_azs = 1,
            nat_gateways = 0,
            enable_dns_hostnames = True,
            enable_dns_support = True,
            subnet_configuration = [
                _ec2.SubnetConfiguration(
                    subnet_type = _ec2.SubnetType.PUBLIC,
                    name = 'Public',
                    cidr_mask = 24
                )
            ],
            gateway_endpoints = {
                'DYNAMODB': _ec2.GatewayVpcEndpointOptions(
                    service = _ec2.GatewayVpcEndpointAwsService.DYNAMODB
                ),
                'S3': _ec2.GatewayVpcEndpointOptions(
                    service = _ec2.GatewayVpcEndpointAwsService.S3
                )
            }
        )

        subnet_ids = []

        for subnet in vpc.public_subnets:
            subnet_ids.append(subnet.subnet_id)

        sg = _ec2.SecurityGroup(
            self, 'sg',
            vpc = vpc,
            allow_all_outbound = True
        )

    ### TASK POLICY ###

        task_policy = _iam.PolicyStatement(
            effect = _iam.Effect.ALLOW, 
            actions = [
                'dynamodb:PutItem',
                'ecr:GetAuthorizationToken',
                'ecr:BatchCheckLayerAvailability',
                'ecr:GetDownloadUrlForLayer',
                'ecr:BatchGetImage',
                'logs:CreateLogStream',
                'logs:PutLogEvents'
            ],
            resources = [
                '*'
            ]
        )

    ### CLOUD WATCH ###

        logs = _logs.LogGroup(
            self, 'logs',
            log_group_name = '/aws/fargate',
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        logssub = _logs.SubscriptionFilter(
            self, 'logssub',
            log_group = logs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        logstime = _logs.SubscriptionFilter(
            self, 'logstime',
            log_group = logs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

        logging = _ecs.AwsLogDriver(
            stream_prefix = 'censys',
            log_group = logs
        )

    ### FARGATE ECS ###

        cluster = _ecs.Cluster(
            self, 'cluster',
            vpc = vpc
        )

        tasked = _ecs.TaskDefinition(
            self, 'tasked',
            cpu = '1024',
            memory_mib = '2048',
            compatibility = _ecs.Compatibility.FARGATE
        )

        tasked.add_to_task_role_policy(task_policy)

        task = tasked.add_container(
            'task',
            image = _ecs.ContainerImage.from_asset('censys/task'),
            logging = logging,
            environment = {
                'CENSYS_API_ID': '-',
                'CENSYS_API_SECRET': '-'
            }
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

        role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                'service-role/AWSLambdaRole'
            )
        )

        role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                'service-role/AWSLambdaVPCAccessExecutionRole'
            )
        )     

        role.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'ecs:RunTask',
                    'iam:PassRole',
                    'ssm:GetParameter'
                ],
                resources = [
                    '*'
                ]
            )
        )

    ### RUN TASK ###

        run = _lambda.Function(
            self, 'run',
            handler = 'run.handler',
            runtime = _lambda.Runtime.PYTHON_3_11,
            code = _lambda.Code.from_asset('censys/run'),
            architecture = _lambda.Architecture.ARM_64,
            environment = dict(
                AWS_ACCOUNT = account,
                CLUSTER_NAME = cluster.cluster_name,
                TASK_DEFINITION = tasked.task_definition_arn,
                SUBNET_ID = subnet_ids[0],
                CONTAINER_NAME = task.container_name,
                SECURITY_GROUP = sg.security_group_id
            ),
            timeout = Duration.seconds(30),
            memory_size = 128,
            role = role,
            layers = [
                layer
            ]
        )

        runlogs = _logs.LogGroup(
            self, 'runlogs',
            log_group_name = '/aws/lambda/'+run.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        runsub = _logs.SubscriptionFilter(
            self, 'runsub',
            log_group = runlogs,
            destination = _destinations.LambdaDestination(error),
            filter_pattern = _logs.FilterPattern.all_terms('ERROR')
        )

        runtime = _logs.SubscriptionFilter(
            self, 'runtime',
            log_group = runlogs,
            destination = _destinations.LambdaDestination(timeout),
            filter_pattern = _logs.FilterPattern.all_terms('Task','timed','out')
        )

    ### EVENT ###

        event = _events.Rule(
            self, 'event',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '11',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        event.add_target(
            _targets.LambdaFunction(
                run
            )
        )
