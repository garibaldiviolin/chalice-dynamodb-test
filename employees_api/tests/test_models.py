import pytest
from pydantic.error_wrappers import ValidationError

from models import Employee, UpdateEmployee


def test_update_employee(employee):
    del employee["employee_name"]
    instance = UpdateEmployee(**employee)
    instance.dict == employee


def test_update_employee_without_required_fields():
    with pytest.raises(ValidationError) as exc:
        UpdateEmployee(**{})
    assert exc.value.errors() == [
        {
            "loc": ("city",),
            "msg": "field required",
            "type": "value_error.missing"
        },
    ]


def test_employee(employee):
    instance = Employee(**employee)
    instance.dict == employee


def test_employee_without_required_fields():
    with pytest.raises(ValidationError) as exc:
        Employee(**{})
    assert exc.value.errors() == [
        {
            "loc": ("city",),
            "msg": "field required",
            "type": "value_error.missing"
        },
        {
            "loc": ("employee_name",),
            "msg": "field required",
            "type": "value_error.missing"
        },
    ]
