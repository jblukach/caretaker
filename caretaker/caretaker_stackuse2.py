import datetime

from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_glue_alpha as _glue,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_s3 as _s3,
    aws_s3_deployment as _deployment,
    aws_ssm as _ssm
)

from constructs import Construct

class CaretakerStackUse2(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account

        year = datetime.datetime.now().strftime('%Y')
        month = datetime.datetime.now().strftime('%m')
        day = datetime.datetime.now().strftime('%d')

    ### PARAMETER ###

        organization = _ssm.StringParameter.from_string_parameter_attributes(
            self, 'organization',
            parameter_name = '/organization/id'
        )

    ### LAMBDA LAYER ###

        packages = _s3.Bucket.from_bucket_name(
            self, 'packages',
            bucket_name = 'packages-use2-lukach-io'
        )

        requests = _lambda.LayerVersion(
            self, 'requests',
            layer_version_name = 'requests',
            description = str(year)+'-'+str(month)+'-'+str(day)+' deployment',
            code = _lambda.Code.from_bucket(
                bucket = packages,
                key = 'requests.zip'
            ),
            compatible_architectures = [
                _lambda.Architecture.ARM_64
            ],
            compatible_runtimes = [
                _lambda.Runtime.PYTHON_3_13
            ],
            removal_policy = RemovalPolicy.DESTROY
        )

        parameter = _ssm.StringParameter(
            self, 'parameter',
            parameter_name = '/layer/requests',
            string_value = requests.layer_version_arn,
            description = 'Requests Lambda Layer ARN',
            tier = _ssm.ParameterTier.STANDARD
        )

    ### S3 BUCKET ###

        bucket = _s3.Bucket(
            self, 'bucket',
            bucket_name = 'caretakerbucket',
            encryption = _s3.BucketEncryption.S3_MANAGED,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = True,
            enforce_ssl = True,
            versioned = False
        )

        bucket.add_lifecycle_rule(
            expiration = Duration.days(1),
            noncurrent_version_expiration = Duration.days(1)
        )

        output = _s3.Bucket(
            self, 'output',
            bucket_name = 'caretakeroutput',
            encryption = _s3.BucketEncryption.S3_MANAGED,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = True,
            enforce_ssl = True,
            versioned = False
        )

        output.add_lifecycle_rule(
            expiration = Duration.days(1),
            noncurrent_version_expiration = Duration.days(1)
        )

        research = _s3.Bucket(
            self, 'research',
            bucket_name = 'caretakerresearch',
            encryption = _s3.BucketEncryption.S3_MANAGED,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = False,
            enforce_ssl = True,
            versioned = False
        )

        staged = _s3.Bucket(
            self, 'staged',
            bucket_name = 'caretakerstaged',
            encryption = _s3.BucketEncryption.S3_MANAGED,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = True,
            enforce_ssl = True,
            versioned = False
        )

        deployment = _deployment.BucketDeployment(
            self, 'deployment',
            sources = [_deployment.Source.asset('code')],
            destination_bucket = staged,
            prune = False
        )

        bucket_policy = _iam.PolicyStatement(
            effect = _iam.Effect(
                'ALLOW'
            ),
            principals = [
                _iam.AnyPrincipal()
            ],
            actions = [
                's3:ListBucket'
            ],
            resources = [
                staged.bucket_arn
            ],
            conditions = {"StringEquals": {"aws:PrincipalOrgID": organization.string_value}}
        )

        staged.add_to_resource_policy(bucket_policy)

        object_policy = _iam.PolicyStatement(
            effect = _iam.Effect(
                'ALLOW'
            ),
            principals = [
                _iam.AnyPrincipal()
            ],
            actions = [
                's3:GetObject'
            ],
            resources = [
                staged.arn_for_objects('*')
            ],
            conditions = {"StringEquals": {"aws:PrincipalOrgID": organization.string_value}}
        )

        staged.add_to_resource_policy(object_policy)

        temporary = _s3.Bucket(
            self, 'temporary',
            bucket_name = 'caretakertemporary',
            encryption = _s3.BucketEncryption.S3_MANAGED,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = True,
            enforce_ssl = True,
            versioned = False
        )

        temporary.add_lifecycle_rule(
            expiration = Duration.days(1),
            noncurrent_version_expiration = Duration.days(1)
        )

    ### GLUE DATABASE ###

        database = _glue.Database(
            self, 'database',
            database_name = 'caretaker'
        )

    ### GLUE TABLES ###

        address =  _glue.Table(
            self, 'address',
            bucket = research,
            s3_prefix = 'ips/',
            database = database,
            table_name = 'address',
            columns = [
                _glue.Column(
                    name = 'address',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'attrib',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'ts',
                    type = _glue.Schema.STRING
                )
            ],
            data_format = _glue.DataFormat(
                input_format = _glue.InputFormat.TEXT,
                output_format = _glue.OutputFormat.PARQUET,
                serialization_library = _glue.SerializationLibrary.OPEN_CSV
            )
        )

        domain =  _glue.Table(
            self, 'domain',
            bucket = research,
            s3_prefix = 'dns/',
            database = database,
            table_name = 'domain',
            columns = [
                _glue.Column(
                    name = 'domain',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'attrib',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'ts',
                    type = _glue.Schema.STRING
                )
            ],
            data_format = _glue.DataFormat(
                input_format = _glue.InputFormat.TEXT,
                output_format = _glue.OutputFormat.PARQUET,
                serialization_library = _glue.SerializationLibrary.OPEN_CSV
            )
        )

    ### OIDC ###

        provider = _iam.OpenIdConnectProvider(
            self, 'provider',
            url = 'https://token.actions.githubusercontent.com',
            client_ids = [
                'sts.amazonaws.com'
            ]
        )

        github = _iam.Role(
            self, 'github',
            assumed_by = _iam.WebIdentityPrincipal(provider.open_id_connect_provider_arn).with_conditions(
                {
                    "StringLike": {
                        "token.actions.githubusercontent.com:sub": "repo:jblukach/caretaker:*"
                    }
                }
            )
        )

        github.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                'ReadOnlyAccess'
            )
        )   

        github.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'cloudformation:CreateChangeSet',
                    'cloudformation:DeleteChangeSet',
                    'cloudformation:DescribeChangeSet',
                    'cloudformation:DescribeStacks',
                    'cloudformation:ExecuteChangeSet',
                    'cloudformation:CreateStack',
                    'cloudformation:UpdateStack',
                    'cloudformation:RollbackStack',
                    'cloudformation:ContinueUpdateRollback',
                    'cloudformation:DescribeStackEvents',
                    'cloudformation:GetTemplate',
                    'cloudformation:DeleteStack',
                    'cloudformation:UpdateTerminationProtection',
                    'cloudformation:GetTemplateSummary'
                ],
                resources = [
                    '*'
                ]
            )
        )

        github.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    's3:GetObject*',
                    's3:GetBucket*',
                    's3:List*',
                    's3:Abort*',
                    's3:DeleteObject*',
                    's3:PutObject*'
                ],
                resources = [
                    '*'
                ]
            )
        )

        github.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'kms:Decrypt',
                    'kms:DescribeKey',
                    'kms:Encrypt',
                    'kms:ReEncrypt*',
                    'kms:GenerateDataKey*'
                ],
                resources = [
                    '*'
                ],
                conditions = {
                    "StringEquals": {
                        "kms:ViaService": "s3.us-east-1.amazonaws.com"
                    }
                }
            )
        )

        github.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'kms:Decrypt',
                    'kms:DescribeKey',
                    'kms:Encrypt',
                    'kms:ReEncrypt*',
                    'kms:GenerateDataKey*'
                ],
                resources = [
                    '*'
                ],
                conditions = {
                    "StringEquals": {
                        "kms:ViaService": "s3.us-east-2.amazonaws.com"
                    }
                }
            )
        )

        github.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'kms:Decrypt',
                    'kms:DescribeKey',
                    'kms:Encrypt',
                    'kms:ReEncrypt*',
                    'kms:GenerateDataKey*'
                ],
                resources = [
                    '*'
                ],
                conditions = {
                    "StringEquals": {
                        "kms:ViaService": "s3.us-west-2.amazonaws.com"
                    }
                }
            )
        )

        github.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'iam:PassRole'
                ],
                resources = [
                    'arn:aws:iam::'+str(account)+':role/cdk-lukach-cfn-exec-role-'+str(account)+'-us-east-1',
                    'arn:aws:iam::'+str(account)+':role/cdk-lukach-cfn-exec-role-'+str(account)+'-us-east-2',
                    'arn:aws:iam::'+str(account)+':role/cdk-lukach-cfn-exec-role-'+str(account)+'-us-west-2'
                ]
            )
        )

        github.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'sts:GetCallerIdentity'
                ],
                resources = [
                    '*'
                ]
            )
        )

        github.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'ssm:GetParameter',
                    'ssm:GetParameters'
                ],
                resources = [
                    'arn:aws:ssm:us-east-1:'+str(account)+':parameter/cdk-bootstrap/lukach/version',
                    'arn:aws:ssm:us-east-2:'+str(account)+':parameter/cdk-bootstrap/lukach/version',
                    'arn:aws:ssm:us-west-2:'+str(account)+':parameter/cdk-bootstrap/lukach/version'
                ]
            )
        )
