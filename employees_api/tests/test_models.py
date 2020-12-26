import pytest
from pydantic.error_wrappers import ValidationError

from models import Employee


def test_employee(employee):
    instance = Employee(**employee)
    instance.dict == employee


def test_employee_without_required_fields():
    with pytest.raises(ValidationError) as exc:
        Employee(**{})
    assert exc.value.errors() == [
        {
            "loc": ("employee_name",),
            "msg": "field required",
            "type": "value_error.missing"
        },
        {
            "loc": ("city",),
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
