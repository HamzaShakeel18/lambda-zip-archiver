# Zip Archiver Lambda

This project implements an automated flow to reduce S3 storage costs by compressing uploaded files. An S3 event triggers a Lambda function which downloads the file, compresses it to ZIP, uploads the zipped object back to the same bucket, and deletes the original.

The solution uses AWS SAM for deployment and CloudFormation for provisioning all required resources.

---

## Overview

- **Trigger:** S3 ObjectCreated events  
- **Action:** Download, compress to ZIP, upload, delete original  
- **Packaging:** Docker container image  
- **Versioning:** Lambda versions for rollback  
- **Deployment:** SAM CLI + CloudFormation  

---

## Tech Stack & AWS Services

- AWS Lambda (Python/Docker)  
- Amazon S3  
- IAM roles with managed policies  
- Amazon ECR (for container images)  
- Amazon VPC with private subnets and security groups  
- AWS SAM CLI and CloudFormation  

---

## Flow Explanation

1. A file is uploaded to the S3 bucket.  
2. S3 event triggers the Lambda function.  
3. Lambda downloads the object to `/tmp`.  
4. The file is compressed using the Python `zipfile` module.  
5. The ZIP is uploaded to S3 with `.zip` appended to the key.  
6. The original file is deleted to save storage cost.  

---

## Lambda Versioning Strategy

The Lambda is containerized and stored in an ECR repository. Every deployment publishes a new Lambda version automatically, updating the alias to point to the latest. This allows:

- Safe deployments  
- Easy rollback  
- Traceability of changes  

---

## Deployment Instructions

```bash
sam build
sam deploy --guided  --stack-name zip-archiver-stack --capabilities CAPABILITY_NAMED_IAM
