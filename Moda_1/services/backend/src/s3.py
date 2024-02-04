import boto3
from fastapi import HTTPException, status
from config import settings
from botocore.exceptions import ClientError

def s3_upload(content: bytes, key: str):
    session = boto3.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=settings.YANDEX_S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.YANDEX_S3_SECRET_ACCESS_KEY,
    )
    
    bucket_name = settings.YANDEX_S3_BUCKET_NAME
    
    s3.put_object(Body=content, Bucket=bucket_name, Key=key)
    
def s3_get_object(key: str):
    session = boto3.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=settings.YANDEX_S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.YANDEX_S3_SECRET_ACCESS_KEY,
    )
    
    bucket_name = settings.YANDEX_S3_BUCKET_NAME

    try:
        response = s3.get_object(Bucket=bucket_name, Key=key)
        return response['Body'].read()
    except s3.exceptions.NoSuchKey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Object with key '{key}' not found."
        )
        
def list_objects_in_bucket():
    session = boto3.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=settings.YANDEX_S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.YANDEX_S3_SECRET_ACCESS_KEY,
    )

    bucket_name = settings.YANDEX_S3_BUCKET_NAME

    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        objects = response.get('Contents', [])
        for obj in objects:
            print(f"Object Key: {obj['Key']}")
    except Exception as e:
        print(f"Error: {e}")
        
def generate_presigned_url(object_key, expiration_time=7200, session=None):
    bucket_name = settings.YANDEX_S3_BUCKET_NAME

    if session is None:
        session = boto3.Session()

    s3 = session.client('s3', 
            endpoint_url='https://storage.yandexcloud.net',
            aws_access_key_id=settings.YANDEX_S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.YANDEX_S3_SECRET_ACCESS_KEY
    )

    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_key
            },
            ExpiresIn=expiration_time
        )
        return url
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return None