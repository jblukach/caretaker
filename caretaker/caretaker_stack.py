from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_iam as _iam,
    aws_s3 as _s3,
    aws_ssm as _ssm
)

from constructs import Construct

class CaretakerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

    ### LAMBDA LAYER ###

        organization = _ssm.StringParameter.from_string_parameter_arn(
            self, 'organization',
            'arn:aws:ssm:us-east-1:070176467818:parameter/root/organization'
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
                bucket.bucket_arn
            ],
            conditions = {"StringEquals": {"aws:PrincipalOrgID": organization.string_value}}
        )

        bucket.add_to_resource_policy(bucket_policy)

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
                bucket.arn_for_objects('*')
            ],
            conditions = {"StringEquals": {"aws:PrincipalOrgID": organization.string_value}}
        )

        bucket.add_to_resource_policy(object_policy)

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
