from boto3.dynamodb.conditions import Key


def get_query_parameters(query_params):
    query_params = query_params or {}

    filters = None
    for key, value in query_params.items():
        if key not in ("employee_name", ):
            continue

        table_filter = Key(key).eq(value)
        if filters is None:
            filters = table_filter
        else:
            filters &= table_filter

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
