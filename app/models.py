from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.sql import func
from app.database import Base

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    department = Column(String, nullable=True)
    role = Column(String, nullable=True)
    date_joined = Column(Date, server_default=func.current_date())