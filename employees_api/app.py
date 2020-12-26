import boto3
from botocore.exceptions import ClientError
from chalice import Chalice, Response

from database import load_database_table

app = Chalice(app_name="employees_api")


@app.route("/employees", methods=["POST"])
def create_employee():
    table = load_database_table("Employees")

    json_body = app.current_request.json_body

    table.put_item(Item=json_body)

    return Response(
        body=json_body,
        status_code=201
    )


@app.route("/employees", methods=["GET"])
def list_employees():
    return Response(
        body={
            "results": [
                {"id": "1"}
            ]
        },
        status_code=200
    )


@app.route("/employees/{employee_name}", methods=["GET"])
def get_employee(employee_name):
    table = load_database_table("Employees")

    try:
        response = table.get_item(Key={"employee_name": employee_name})
    except ClientError:
        return Response(body={"error": "internal_error"}, status_code=500)

    try:
        return Response(body=response["Item"], status_code=200)
    except KeyError:
        return Response(body={"error": "not_found"}, status_code=404)


@app.route("/employees/{employee_name}", methods=["PUT"])
def update_employee(employee_name):
    table = load_database_table("Employees")

    json_body = app.current_request.json_body
    del json_body["employee_name"]

    response = table.update_item(
        Key={"employee_name": employee_name},
        UpdateExpression="set city=:city",
        ExpressionAttributeValues={
            ":city": json_body["city"],
        },
        ReturnValues="ALL_NEW"
    )
    return response["Attributes"]


@app.route("/employees/{employee_name}", methods=["DELETE"])
def delete_employee(employee_name):
    table = load_database_table("Employees")

    try:
        table.delete_item(
            Key={
                "employee_name": employee_name,
            },
            ConditionExpression="employee_name = :v_employee_name",
            ExpressionAttributeValues={
                ":v_employee_name": employee_name
            }
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return Response(body={"error": "not_found"}, status_code=404)
        else:
            return Response(body={"error": "internal_error"}, status_code=500)
    else:
        return Response(body=None, status_code=204)
