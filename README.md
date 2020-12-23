# chalice-dynamodb-test
A test using Chalice (Python framework for AWS Lambda) and AWS DynamoDB

## Requirements
- [Python3+](https://www.python.org/downloads/);
- [Pipenv](https://github.com/pypa/pipenv);
- **[DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html) for local tests (rename the folder to dynamodb_local_latest).**

## Development
1) Run `make run-local-dynamodb` to run DynamoDB locally in one terminal;
2) Run `make run-local-chalice` to start the chalice development server.
