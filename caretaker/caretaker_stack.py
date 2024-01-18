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
    aws_logs_destinations as _destinations,
    aws_s3 as _s3,
    aws_s3_deployment as _deployment,
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
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('maxmind'),
            timeout = Duration.seconds(900),
            handler = 'maxmind.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                MAP_TABLE = map.table_name
            ),
            memory_size = 512,
            retry_attempts = 0,
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

    ### S3 BUCKET ###

        bucket = _s3.Bucket.from_bucket_attributes(
            self, 'bucket',
            bucket_arn = 'arn:aws:s3:::stage.tundralabs.org'
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'feodotracker',
            sources = [
                _deployment.Source.asset('sources/ip/abusech/feodotracker')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'sslbl',
            sources = [
                _deployment.Source.asset('sources/ip/abusech/sslbl')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'alienvault',
            sources = [
                _deployment.Source.asset('sources/ip/alienvault')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'binarydefense',
            sources = [
                _deployment.Source.asset('sources/ip/binarydefense')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'blocklist',
            sources = [
                _deployment.Source.asset('sources/ip/blocklist')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'c2intelfeeds',
            sources = [
                _deployment.Source.asset('sources/ip/c2intelfeeds')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'c2tracker',
            sources = [
                _deployment.Source.asset('sources/ip/c2tracker')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'cinsscore',
            sources = [
                _deployment.Source.asset('sources/ip/cinsscore')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'cybercure',
            sources = [
                _deployment.Source.asset('sources/ip/cybercure')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'digitalside',
            sources = [
                _deployment.Source.asset('sources/ip/digitalside')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'elliotech',
            sources = [
                _deployment.Source.asset('sources/ip/elliotech')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'greensnow',
            sources = [
                _deployment.Source.asset('sources/ip/greensnow')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'ipsum',
            sources = [
                _deployment.Source.asset('sources/ip/ipsum')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'jamesbrine',
            sources = [
                _deployment.Source.asset('sources/ip/jamesbrine')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'miraisecurity',
            sources = [
                _deployment.Source.asset('sources/ip/miraisecurity')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'nubinetwork',
            sources = [
                _deployment.Source.asset('sources/ip/nubinetwork')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'proofpoint',
            sources = [
                _deployment.Source.asset('sources/ip/proofpoint')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'rescure',
            sources = [
                _deployment.Source.asset('sources/ip/rescure')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'rutgers',
            sources = [
                _deployment.Source.asset('sources/ip/rutgers')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'scorecard',
            sources = [
                _deployment.Source.asset('sources/ip/scorecard')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'spamhaus',
            sources = [
                _deployment.Source.asset('sources/ip/spamhaus')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'talosintelligence',
            sources = [
                _deployment.Source.asset('sources/ip/talosintelligence')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'tor',
            sources = [
                _deployment.Source.asset('sources/ip/tor')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'virtualfabric',
            sources = [
                _deployment.Source.asset('sources/ip/virtualfabric')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'zonefiles',
            sources = [
                _deployment.Source.asset('sources/ip/zonefiles')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'ip',
            prune = False
        )

    ### - ###

        copyfiles = _deployment.BucketDeployment(
            self, 'threatfox',
            sources = [
                _deployment.Source.asset('sources/dns/abusech/threatfox')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'dns',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'urlhaus',
            sources = [
                _deployment.Source.asset('sources/dns/abusech/urlhaus')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'dns',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'blackbook',
            sources = [
                _deployment.Source.asset('sources/dns/blackbook')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'dns',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'c2intelfeedsdns',
            sources = [
                _deployment.Source.asset('sources/dns/c2intelfeeds')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'dns',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'certpl',
            sources = [
                _deployment.Source.asset('sources/dns/certpl')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'dns',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'cybercuredns',
            sources = [
                _deployment.Source.asset('sources/dns/cybercure')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'dns',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'digitalsidedns',
            sources = [
                _deployment.Source.asset('sources/dns/digitalside')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'dns',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'openphish',
            sources = [
                _deployment.Source.asset('sources/dns/openphish')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'dns',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'phishingarmy',
            sources = [
                _deployment.Source.asset('sources/dns/phishingarmy')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'dns',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'phishtank',
            sources = [
                _deployment.Source.asset('sources/dns/phishtank')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'dns',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'rescuredns',
            sources = [
                _deployment.Source.asset('sources/dns/rescure')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'dns',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'urlabuse',
            sources = [
                _deployment.Source.asset('sources/dns/urlabuse')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'dns',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'virtualfabricdns',
            sources = [
                _deployment.Source.asset('sources/dns/virtualfabric')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'dns',
            prune = False
        )

        copyfiles = _deployment.BucketDeployment(
            self, 'zonefilesdns',
            sources = [
                _deployment.Source.asset('sources/dns/zonefiles')
            ],
            destination_bucket = bucket,
            destination_key_prefix = 'dns',
            prune = False
        )
