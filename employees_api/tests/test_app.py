import json
from unittest.mock import patch, Mock

from botocore.exceptions import ClientError


def test_create_employee(lambda_client, employee, employees_url):
    response = lambda_client.http.post(
        employees_url,
        body=json.dumps(employee),
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 201
    assert response.json_body == employee


def test_create_employee_without_fields(lambda_client, employees_url):
    response = lambda_client.http.post(
        employees_url,
        body="{}",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert response.json_body == [
        {
            'loc': ['employee_name'],
            'msg': 'field required',
            'type': 'value_error.missing'
        },
        {
            'loc': ['city'],
            'msg': 'field required',
            'type': 'value_error.missing'
        }
    ]


def test_list_employees(lambda_client, employees_url, database_employee):
    response = lambda_client.http.get(
        employees_url,
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    assert response.json_body == [
        {'city': 'Houston', 'employee_name': 'John Dunbar'}
    ]


def test_get_employee(lambda_client, database_employee, employee,
                      employee_url):
    response = lambda_client.http.get(
        employee_url,
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    assert response.json_body == employee


@patch("boto3.resource")
def test_get_employee_with_internal_error(boto3_resource_mock, lambda_client,
                                          database_employee, employee,
                                          employee_url):
    table_mock = Mock()
    table_mock.get_item = Mock()
    table_mock.get_item.side_effect = ClientError(
        error_response={},
        operation_name=None,
    )
    dynamodb_mock = Mock()
    dynamodb_mock.Table = Mock(return_value=table_mock)
    boto3_resource_mock.return_value = dynamodb_mock

    response = lambda_client.http.get(
        employee_url,
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 500
    assert response.json_body == {"error": "internal_error"}


def test_get_employee_not_found(lambda_client, database_employee, employee,
                                inexistent_employee_url):
    response = lambda_client.http.get(
        inexistent_employee_url,
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 404
    assert response.json_body == {"error": "not_found"}


def test_update_employee(lambda_client, employee, employee_url):
    response = lambda_client.http.put(
        employee_url,
        body=json.dumps(employee),
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    assert response.json_body == employee


def test_delete_employee(lambda_client, database_employee, employee,
                         employee_url):
    response = lambda_client.http.delete(
        employee_url,
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 204
    assert response.json_body is None


def test_delete_employee_not_found(lambda_client, employee,
                                   inexistent_employee_url):
    response = lambda_client.http.delete(
        inexistent_employee_url,
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 404
    assert response.json_body == {"error": "not_found"}


@patch("boto3.resource")
def test_delete_employee_internal_error(boto3_resource_mock, lambda_client,
                                        employee, inexistent_employee_url):
    table_mock = Mock()
    table_mock.delete_item = Mock()
    table_mock.delete_item.side_effect = ClientError(
        error_response={"Error": {"Code": "InternalError"}},
        operation_name=None,
    )
    dynamodb_mock = Mock()
    dynamodb_mock.Table = Mock(return_value=table_mock)
    boto3_resource_mock.return_value = dynamodb_mock

    response = lambda_client.http.delete(
        inexistent_employee_url,
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 500
    assert response.json_body == {"error": "internal_error"}
