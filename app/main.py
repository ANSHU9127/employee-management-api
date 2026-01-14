from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models import Employee
from app.schemas import EmployeeCreate
from app.auth import create_access_token

app = FastAPI(title="Employee Management API")

Base.metadata.create_all(bind=engine)

@app.post("/token")
def login():
    token = create_access_token({"user": "admin"})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/api/employees/", status_code=201)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    if db.query(Employee).filter(Employee.email == employee.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    emp = Employee(**employee.dict())
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp

@app.get("/api/employees/")
def list_employees(page: int = 1, department: str = None, role: str = None, db: Session = Depends(get_db)):
    query = db.query(Employee)
    if department:
        query = query.filter(Employee.department == department)
    if role:
        query = query.filter(Employee.role == role)
    return query.offset((page - 1) * 10).limit(10).all()

@app.get("/api/employees/{id}/")
def get_employee(id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).get(id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@app.put("/api/employees/{id}/")
def update_employee(id: int, employee: EmployeeCreate, db: Session = Depends(get_db)):
    emp = db.query(Employee).get(id)
    if not emp:
        raise HTTPException(status_code=404)
    for key, value in employee.dict().items():
        setattr(emp, key, value)
    db.commit()
    return emp

@app.delete("/api/employees/{id}/", status_code=204)
def delete_employee(id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).get(id)
    if not emp:
        raise HTTPException(status_code=404)
    db.delete(emp)
    db.commit()