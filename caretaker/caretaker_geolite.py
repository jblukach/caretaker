import datetime

from aws_cdk import (
    Duration,
    RemovalPolicy,
    Size,
    Stack,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_s3 as _s3
)

from constructs import Construct

class CaretakerGeolite(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account

        year = datetime.datetime.now().strftime('%Y')
        month = datetime.datetime.now().strftime('%m')
        day = datetime.datetime.now().strftime('%d')

    ### S3 BUCKETS ###

        bucket = _s3.Bucket.from_bucket_name(
            self, 'bucket',
            bucket_name = 'packages-use2-lukach-io'
        )

    ### LAMBDA LAYERS ###

        geoip2 = _lambda.LayerVersion(
            self, 'geoip2',
            layer_version_name = 'geoip2',
            description = str(year)+'-'+str(month)+'-'+str(day)+' deployment',
            code = _lambda.Code.from_bucket(
                bucket = bucket,
                key = 'geoip2.zip'
            ),
            compatible_architectures = [
                _lambda.Architecture.ARM_64
            ],
            compatible_runtimes = [
                _lambda.Runtime.PYTHON_3_13
            ],
            removal_policy = RemovalPolicy.DESTROY
        )

        maxminddb = _lambda.LayerVersion(
            self, 'maxminddb',
            layer_version_name = 'maxminddb',
            description = str(year)+'-'+str(month)+'-'+str(day)+' deployment',
            code = _lambda.Code.from_bucket(
                bucket = bucket,
                key = 'maxminddb.zip'
            ),
            compatible_architectures = [
                _lambda.Architecture.ARM_64
            ],
            compatible_runtimes = [
                _lambda.Runtime.PYTHON_3_13
            ],
            removal_policy = RemovalPolicy.DESTROY
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
                    'lambda:UpdateFunctionCode',
                    's3:GetObject',
                    's3:PutObject'
                ],
                resources = [
                    '*'
                ]
            )
        )

    ### LAMBDA FUNCTION ###

        compute = _lambda.Function(
            self, 'compute',
            runtime = _lambda.Runtime.PYTHON_3_13,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('utility/geolite'),
            timeout = Duration.seconds(900),
            handler = 'geolite.handler',
            environment = dict(
                STAGED_S3 = 'caretakerstaged',
                STAGED_S3_USE1 = 'caretakerstageduse1',
                STAGED_S3_USW2 = 'caretakerstagedusw2',
                STAGED_GEO = 'geolite-staged-lukach-io',
                LAMBDA_ASN_USE1 = 'arn:aws:lambda:us-east-1:'+str(account)+':function:asn',
                LAMBDA_ASN_USW2 = 'arn:aws:lambda:us-west-2:'+str(account)+':function:asn',
                LAMBDA_CO_USE1 = 'arn:aws:lambda:us-east-1:'+str(account)+':function:co',
                LAMBDA_CO_USW2 = 'arn:aws:lambda:us-west-2:'+str(account)+':function:co',
                LAMBDA_ST_USE1 = 'arn:aws:lambda:us-east-1:'+str(account)+':function:st',
                LAMBDA_ST_USW2 = 'arn:aws:lambda:us-west-2:'+str(account)+':function:st'
            ),
            ephemeral_storage_size = Size.gibibytes(2),
            memory_size = 3000,
            role = role,
            layers = [
                geoip2,
                maxminddb
            ]
        )

        logs = _logs.LogGroup(
            self, 'logs',
            log_group_name = '/aws/lambda/'+compute.function_name,
            retention = _logs.RetentionDays.ONE_WEEK,
            removal_policy = RemovalPolicy.DESTROY
        )

        event = _events.Rule(
            self, 'event',
            schedule = _events.Schedule.cron(
                minute = '10',
                hour = '11',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        event.add_target(
            _targets.LambdaFunction(compute)
        )
