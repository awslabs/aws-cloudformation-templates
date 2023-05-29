# Aurora Postgres serverless cluster

## Features
- Aurora Postgres compliant serverless cluster.
- Inside an existing VPC so not publicly accessible.
- Creates DB Sunbet Group 
- Creates a Security Group with 5432 port open to all IP.  Lock down after

## After creating the stack
- Add the database password to AWS Secret Manager so you will be able to retrieve it from your authorized applications. Secret Manager can also automatically rotate the password periodically.
