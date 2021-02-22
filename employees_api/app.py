from botocore.exceptions import ClientError
from chalice import Chalice, Response
from pydantic.error_wrappers import ValidationError

from database import load_database_table
from models import UpdateEmployee, Employee
from services import get_query_parameters

app = Chalice(app_name="employees_api")


@app.route("/employees", methods=["POST"])
def create_employee():
    try:
        employee = Employee(**app.current_request.json_body)
    except ValidationError as exc:
        return Response(
            body=exc.json(),
            status_code=400
        )

    table = load_database_table("Employees")

    table.put_item(Item=employee.dict())

    return Response(
        body=employee.json(),
        status_code=201
    )


@app.route("/employees", methods=["GET"])
def list_employees():
    table = load_database_table("Employees")

    parameters = get_query_parameters(app.current_request.query_params)

    if parameters.get("KeyConditionExpression"):
        results = table.query(
            **parameters
        )
    else:
        results = table.scan(**parameters)

    response = {
        "results": results["Items"]
    }
    next_results = results.get("LastEvaluatedKey")
    if next_results:
        response["last_result"] = next_results["employee_name"]

    return response


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
    try:
        employee = UpdateEmployee(**app.current_request.json_body)
    except ValidationError as exc:
        return Response(
            body=exc.json(),
            status_code=400
        )

    table = load_database_table("Employees")

    response = table.update_item(
        Key={"employee_name": employee_name},
        UpdateExpression="set city=:city",
        ExpressionAttributeValues={
            ":city": employee.dict()["city"],
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
