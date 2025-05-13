# email-api-micro1

## Function
REST API that accepts payload and forwards it to SQS after validating input.

## Flow
1. Accepts POST to `/send`
2. Validates token via AWS Parameter Store
3. Validates `email_timestream`
4. Publishes to SQS

TECH STACK:
- Flask 
- AWS Parameter Store, SQS, ECR, ECS
- Docker container
- CI/CD via GitHub actions workflow