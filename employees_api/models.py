from pydantic import BaseModel


class Employee(BaseModel):
    employee_name: str
    city: str
