from boto3.dynamodb.conditions import Key


def get_query_parameters(query_params):
    query_params = query_params or {}

    filters = None
    if "username" in query_params:
        filters = Key("username").eq(query_params["username"])

    parameters = {
        "Limit": 5,
    }

    if filters:
        parameters["KeyConditionExpression"] = filters

    last_result = query_params.get("last_result")
    if last_result:
        parameters["ExclusiveStartKey"] = {
            "username": last_result
        }

    return parameters
