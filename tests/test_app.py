import json


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
