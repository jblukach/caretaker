from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_certificatemanager as _acm,
    aws_cloudfront as _cloudfront,
    aws_cloudfront_origins as _origins,
    aws_cloudwatch as _cloudwatch,
    aws_cloudwatch_actions as _actions,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_route53 as _route53,
    aws_route53_targets as _r53targets,
    aws_s3 as _s3,
    aws_s3_deployment as _deployment,
    aws_sns as _sns,
    aws_ssm as _ssm
)

from constructs import Construct

class CaretakerVerify(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account
        region = Stack.of(self).region

    ### LAMBDA LAYERS ###

        extensions = _ssm.StringParameter.from_string_parameter_attributes(
            self, 'extensions',
            parameter_name = '/extensions/account'
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

    ### S3 BUCKET ###

        bucket = _s3.Bucket.from_bucket_name(
            self, 'bucket',
            bucket_name = 'caretakerbucket'
        )

        deployment = _deployment.BucketDeployment(
            self, 'deployment',
            sources = [_deployment.Source.asset('code')],
            destination_bucket = bucket,
            prune = False
        )

    ### IAM ###

        role = _iam.Role(
            self, 'role',
            role_name = 'verify',
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
                    'dynamodb:Query'
                ],
                resources = [
                    '*'
                ]
            )
        )

    ### LAMBDA ###

        verify = _lambda.Function(
            self, 'verify',
            function_name = 'verify',
            runtime = _lambda.Runtime.PYTHON_3_12,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('verify'),
            timeout = Duration.seconds(7),
            handler = 'verify.handler',
            environment = dict(
                AWS_ACCOUNT = account,
                S3_BUCKET = 'caretakerbucket',
                VERIFY_TABLE = 'verify'
            ),
            memory_size = 128,
            retry_attempts = 0,
            role = role,
            layers = [
                getpublicip
            ]
        )

        url = verify.add_function_url(
            auth_type = _lambda.FunctionUrlAuthType.NONE
        )

        logs = _logs.LogGroup(
            self, 'logs',
            log_group_name = '/aws/lambda/'+verify.function_name,
            retention = _logs.RetentionDays.THIRTEEN_MONTHS,
            removal_policy = RemovalPolicy.DESTROY
        )

        verifyalarm = _cloudwatch.Alarm(
            self, 'verifyalarm',
            comparison_operator = _cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold = 0,
            evaluation_periods = 1,
            metric = verify.metric_errors(
                period = Duration.minutes(1)
            )
        )

        verifyalarm.add_alarm_action(
            _actions.SnsAction(topic)
        )

    ### HOSTZONE ###

        hostzoneid = _ssm.StringParameter.from_string_parameter_attributes(
            self, 'hostzoneid',
            parameter_name = '/r53/tundralabs.org'
        )

        hostzone = _route53.HostedZone.from_hosted_zone_attributes(
             self, 'hostzone',
             hosted_zone_id = hostzoneid.string_value,
             zone_name = 'tundralabs.org'
        )   

    ### CLOUDFRONT LOGS ###

        caretakercloudfrontlogs = _s3.Bucket(
            self, 'caretakercloudfrontlogs',
            bucket_name = 'caretakercloudfrontlogs',
            encryption = _s3.BucketEncryption.S3_MANAGED,
            object_ownership = _s3.ObjectOwnership.OBJECT_WRITER,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = True,
            enforce_ssl = True,
            versioned = True
        )

        caretakercloudfrontlogs.add_lifecycle_rule(
            expiration = Duration.days(400),
            noncurrent_version_expiration = Duration.days(1)
        )

    ### ACM CERTIFICATE ###

        acm = _acm.Certificate(
            self, 'acm',
            domain_name = 'verify.tundralabs.org',
            validation = _acm.CertificateValidation.from_dns(hostzone)
        )

    ### CLOUDFRONT ###

        distribution = _cloudfront.Distribution(
            self, 'distribution',
            comment = 'verify.tundralabs.org',
            default_behavior = _cloudfront.BehaviorOptions(
                origin = _origins.FunctionUrlOrigin(url),
                viewer_protocol_policy = _cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                cache_policy = _cloudfront.CachePolicy.CACHING_DISABLED
            ),
            domain_names = [
                'verify.tundralabs.org'
            ],
            error_responses = [
                _cloudfront.ErrorResponse(
                    http_status = 404,
                    response_http_status = 200,
                    response_page_path = '/'
                )
            ],
            certificate = acm,
            log_bucket = caretakercloudfrontlogs,
            log_includes_cookies = True,
            minimum_protocol_version = _cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021,
            price_class = _cloudfront.PriceClass.PRICE_CLASS_100,
            http_version = _cloudfront.HttpVersion.HTTP2_AND_3,
            enable_ipv6 = True
        )

    ### DNS ENTRY ###

        verifyurl = _route53.ARecord(
            self, 'verifyurl',
            zone = hostzone,
            record_name = 'verify.tundralabs.org',
            target = _route53.RecordTarget.from_alias(_r53targets.CloudFrontTarget(distribution))
        )
