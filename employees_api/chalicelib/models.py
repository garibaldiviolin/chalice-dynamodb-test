from pydantic import BaseModel


class UpdateEmployee(BaseModel):
    city: str


class Employee(UpdateEmployee):
    city: str
    employee_name: str
