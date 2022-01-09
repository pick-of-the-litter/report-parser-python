# report-parser-python

This is a PoC and is currently unfinished. This is a list of things to be added:

- The rest of the lambdas/topics
- unit tests, maybe mutation tests
- CI/CD, git hooks(black, pytest), fleshed out makefile
- Poetry for package management
- A boto3 script to upload contact's username/email mappings in Dynamo
- Get parameters from Parameter Store
- Dockerfile so we can deploy images and also Dockerise our pipelines
- Terraform for any infrastrcutures resources (let SAM do the serverless bits)
- Create a serverless framework of the SAM template to see which is best and so I have reference to both.
- Complete this README