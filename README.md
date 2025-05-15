# email-api-micro1

## Repository Secrets

For the CI/CD pipeline to work properly, add these secrets to the repository:
- `AWS_ACCESS_KEY_ID`: Your AWS access key with appropriate permissions (SQS, S3)
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `AWS_REGION`: us-east-2 (Ohio region)
- `GH_TOKEN`: GitHub personal access token (classic) with repo access to the Terraform repository

## Function
REST API that accepts payload and forwards it to SQS after validating input.

## Flow
1. Accepts POST to `/send`
2. Validates token via AWS Parameter Store
3. Validates `email_timestream`
4. Publishes to SQS


- Flask 
- AWS Parameter Store, SQS, ECR, ECS
- Docker container
- CI/CD via GitHub actions workflow


**For the main repo and instructions, please refer to:** [https://github.com/EdBo-Nk/terraform]
