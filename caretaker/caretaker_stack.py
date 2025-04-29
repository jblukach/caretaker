from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_s3 as _s3,
    aws_s3_deployment as _deployment,
)

from constructs import Construct

class CaretakerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

    ### S3 BUCKET ###

        binary = _s3.Bucket(
            self, 'binary',
            bucket_name = 'caretakerbinary',
            encryption = _s3.BucketEncryption.S3_MANAGED,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = True,
            enforce_ssl = True,
            versioned = False
        )

        deployment = _deployment.BucketDeployment(
            self, 'deployment',
            sources = [_deployment.Source.asset('binary')],
            destination_bucket = binary,
            prune = False
        )

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
