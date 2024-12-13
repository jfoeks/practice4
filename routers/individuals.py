from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from models import Individuals
from datetime import datetime

router = APIRouter()


@router.get("/add_individual")
async def get_add_employee_form(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("add_individual.html", {"request": request})
@router.post("/add_individual")
async def add_individual(
    familiya: str = Form(...),
    imya: str = Form(...),
    otchestvo: str = Form(None),
    date_of_birth: str = Form(...),
    address: str = Form(...),
    phone: str = Form(...),
    db: Session = Depends(get_db)
):
    new_individual = Individuals(
        Familiya=familiya,
        Imya=imya,
        Otchestvo=otchestvo,
        DateOfBirth=datetime.strptime(date_of_birth, "%Y-%m-%d"),
        Address=address,
        Phone=phone
    )
    db.add(new_individual)
    db.commit()
    return RedirectResponse("/", status_code=303)