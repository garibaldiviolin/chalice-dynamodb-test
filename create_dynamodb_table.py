import boto3
import os


def create_employees_table(dynamodb=None):
    print(os.environ)
    if not dynamodb:
        dynamodb = boto3.resource(
            "dynamodb",
            endpoint_url="http://localhost:8000"
        )

    table = dynamodb.create_table(
        TableName="Employees",
        KeySchema=[
            {
                "AttributeName": "employee_name",
                "KeyType": "HASH"  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "employee_name",
                "AttributeType": "S"
            },
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 10,
            "WriteCapacityUnits": 10
        }
    )
    return table


if __name__ == "__main__":
    movie_table = create_employees_table()
    print("Table status:", movie_table.table_status)
