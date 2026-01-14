from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: Optional[str] = None
    role: Optional[str] = None

class EmployeeResponse(EmployeeCreate):
    id: int
    date_joined: date

    class Config:
        orm_mode = True