import boto3
import pytest
from chalice.test import Client

from app import app
from database import load_database_table


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


@pytest.fixture
def six_database_employee(database_table, employee):
    employees = []
    for number in range(6):
        employee["employee_name"] = str(number)
        employees.append(database_table.put_item(Item=employee))
    return employees


@pytest.fixture
def employees_url():
    return "/employees"


@pytest.fixture
def employee_url(employee):
    return f"/employees/{employee['employee_name']}"


@pytest.fixture
def inexistent_employee_url():
    return "/employees/inexistent_employee"


@pytest.fixture(autouse=True)
def run_around_tests():
    table = load_database_table("Employees")

    scan = table.scan()

    with table.batch_writer() as batch:
        for each in scan['Items']:
            batch.delete_item(Key={"employee_name": each["employee_name"]})
