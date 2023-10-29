import boto3
from django.conf import settings

class PublicS3(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PublicS3, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            self.access_key = settings.AWS_S3_ACCESS_KEY_ID
            self.secret_access_key = settings.AWS_S3_SECRET_ACCESS_KEY
            self.resource = boto3.resource(
                "s3",
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_access_key,
            )
            cls._init = True

    def get_bucket(self):
        return self.resource.Bucket(settings.AWS_STORAGE_BUCKET_NAME)

    def put_object(self, key, body, content_type):
        bucket = self.get_bucket()
        bucket.put_object(
            Key=key,
            Body=body,
            ContentType=content_type,
        )

    def delete_object(self, key):
        bucket = self.get_bucket()
        bucket.delete_objects(
            Delete={
                'Objects': [{ "Key": key }]
            }
        )
