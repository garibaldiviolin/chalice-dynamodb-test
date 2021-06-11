from pydantic import BaseModel


class UpdateEmployee(BaseModel):
    city: str


class Employee(UpdateEmployee):
    employee_name: str
