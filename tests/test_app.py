import json
from unittest.mock import patch, Mock

from botocore.exceptions import ClientError


def test_create_employee(lambda_client, employee):
    response = lambda_client.http.post(
        "/employees",
        body=json.dumps(employee),
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 201
    assert response.json_body == employee


def test_list_employees(lambda_client):
    response = lambda_client.http.get(
        f"/employees",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    assert response.json_body == {
        "results": [
            {'id': '1'}
        ]
    }


def test_get_employee(lambda_client, database_employee, employee):
    response = lambda_client.http.get(
        f"/employees/{employee['employee_name']}",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    assert response.json_body == employee


@patch("boto3.resource")
def test_get_employee_with_internal_error(boto3_resource_mock, lambda_client,
                                          database_employee, employee):
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
        f"/employees/{employee['employee_name']}",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 500
    assert response.json_body == {"error": "internal_error"}


def test_get_employee_not_found(lambda_client, database_employee, employee):
    response = lambda_client.http.get(
        f"/employees/name_not_found",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 404
    assert response.json_body == {"error": "not_found"}


def test_update_employee(lambda_client, employee):
    response = lambda_client.http.put(
        f"/employees/{employee['employee_name']}",
        body=json.dumps(employee),
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    assert response.json_body == employee


def test_delete_employee(lambda_client, database_employee, employee):
    response = lambda_client.http.delete(
        f"/employees/{employee['employee_name']}",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 204
    assert response.json_body is None


def test_delete_employee_not_found(lambda_client, employee):
    response = lambda_client.http.delete(
        f"/employees/employee_not_found",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 404
    assert response.json_body == {"error": "not_found"}
