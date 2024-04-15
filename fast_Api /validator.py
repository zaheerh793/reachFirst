from pydantic import BaseModel
from datetime import datetime, date


class EmployeeSerializer(BaseModel):
    id: int
    name: str
    email: str
    phone: str


class ShiftSerializer(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime
    shift_date: date
    employee_id: int