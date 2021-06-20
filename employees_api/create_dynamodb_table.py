from chalicelib.database import load_database


def create_employees_table():
    database = load_database()

    table = database.create_table(
        TableName="Employees",
        KeySchema=[
            {
                "AttributeName": "username",
                "KeyType": "HASH"  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "username",
                "AttributeType": "S"
            },
            {
                "AttributeName": "country",
                "AttributeType": "S"
            },
            {
                "AttributeName": "city",
                "AttributeType": "S"
            },
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "RegionIndex",
                "KeySchema": [
                    {
                        "AttributeName": "country",
                        "KeyType": "HASH"
                    },
                    {
                        "AttributeName": "city",
                        "KeyType": "RANGE"
                    },
                ],
                "Projection": {
                    "ProjectionType": "ALL"
                },
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 10,
                    "WriteCapacityUnits": 10,
                }
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
