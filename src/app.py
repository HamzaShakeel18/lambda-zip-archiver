import json
import boto3
import zipfile
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        if key.endswith('.zip'):
            print(f"Skipping already zipped file: {key}")
            continue

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
            s3.delete_object(Bucket=bucket, Key=key)
            print(f"Compressed and archived: {key}")

    return {
        "statusCode": 200,
        "body": json.dumps("Compression completed successfully")
    }
