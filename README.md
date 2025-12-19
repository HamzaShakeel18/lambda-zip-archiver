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
```
---

## Cost Analysis 

The company is processing **1,000,000 files per hour**, with an average size of **10 MB** per file.

### Storage Cost Without Compression
10 MB × 1,000,000 files/hr × 24 hours × 30 days
= 6,912,000,000 MB ≈ 6.9 PB
S3 Standard storage cost (~$0.023 per GB):6,912,000 GB × $0.023 ≈ $158,976/month

### Storage Cost After Compression
Assuming compression reduces size by ~50%:
Final storage ≈ $79,488/month

### Additional Costs
- Lambda executions per million requests  
- S3 PUT / GET / DELETE requests  
- ECR storage for container images  

### Suggestions to Reduce Costs
- Enable lifecycle policies to move older ZIPs to Glacier Deep Archive  
- Batch compress multiple files together  

---

## Scalability / Bottlenecks 

Potential bottlenecks and considerations at scale:

- **Lambda Concurrency Limits:** High volume of S3 events may hit account concurrency limits.  
- **S3 Event Fan-out:** Sudden bursts in file uploads can overwhelm Lambda triggers.  
- **Tmp Storage Limits:** Lambda has `/tmp` limit of 512 MB; very large files may fail.  
- **Request Volume:** Each file results in a GET + PUT + DELETE, doubling S3 request count.  

**Recommendations:**
- Consider batch processing for large uploads  
- Monitor Lambda concurrency and scale limits  
- Enable logging and metrics to identify bottlenecks early  
