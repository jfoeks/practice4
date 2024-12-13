from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import get_db
from models import Employee

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_employees(request: Request, db: Session = Depends(get_db)):
    employees = db.query(Employee).all()

    employees_data = [EmployeeBase.from_orm(emp) for emp in employees]

    return {"request": request, "employees": employees_data}