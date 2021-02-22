from boto3.dynamodb.conditions import Key


def get_query_parameters(query_params):
    query_params = query_params or {}

    filters = None
    if "employee_name" in query_params:
        filters = Key("employee_name").eq(query_params["employee_name"])

    parameters = {
        "Limit": 5,
    }

    if filters:
        parameters["KeyConditionExpression"] = filters

    last_result = query_params.get("last_result")
    if last_result:
        parameters["ExclusiveStartKey"] = {
            "employee_name": last_result
        }

    return parameters
