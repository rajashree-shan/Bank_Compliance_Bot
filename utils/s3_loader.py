import boto3
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, S3_BUCKET_NAME

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def list_files():
    response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME)
    return [obj['Key'] for obj in response.get('Contents', [])] if 'Contents' in response else []

def download_file(key):
    local_path = f"/tmp/{key.replace('/', '_')}"
    s3.download_file(S3_BUCKET_NAME, key, local_path)
    return local_path
