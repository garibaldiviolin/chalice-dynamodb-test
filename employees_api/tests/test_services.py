from boto3.dynamodb.conditions import Key

from services import get_query_parameters


def test_get_query_parameters_without_parameters():
    parameters = get_query_parameters(None)
    assert parameters == {"Limit": 5}


def test_get_query_parameters_with_parameters():
    parameters = get_query_parameters({"employee_name": "James"})
    assert parameters == {
        "Limit": 5,
        "KeyConditionExpression": Key("employee_name").eq("James"),
    }


def test_get_query_parameters_with_last_result():
    parameters = get_query_parameters({"last_result": "John"})
    assert parameters == {
        'Limit': 5,
        'ExclusiveStartKey': {
            'employee_name': 'John'
        }
    }
