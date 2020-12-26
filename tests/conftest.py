import boto3
import pytest
from chalice.test import Client

from employees_api.app import app


@pytest.fixture
def lambda_client():
    with Client(app) as client:
        yield client


@pytest.fixture
def employee():
    return {
        "employee_name": "John Dunbar",
        "city": "Houston"
    }


@pytest.fixture
def database_table():
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url="http://localhost:8000"
    )

    return dynamodb.Table("Employees")


@pytest.fixture
def database_employee(database_table, employee):
    return database_table.put_item(Item=employee)
