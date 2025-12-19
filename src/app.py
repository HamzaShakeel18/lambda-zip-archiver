import json
import boto3
import zipfile
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):

    bucket = "test-lambda-archiver-manual"
    key = "test-file1.json"

    download_path = f"/tmp/{os.path.basename(key)}"
    zip_path = f"{download_path}.zip"
    zip_key = f"{key}.zip"

    try:
        s3.download_file(bucket, key, download_path)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(download_path, arcname=os.path.basename(key))
        s3.upload_file(zip_path, bucket, zip_key)
    finally:
        if os.path.exists(download_path):
            os.remove(download_path)
        if os.path.exists(zip_path):
            os.remove(zip_path)

    return {
        "statusCode": 200,
        "body": json.dumps("Compression completed successfully")
    }
