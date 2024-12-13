from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from models import Employee, Education, BankCard, Position, EmployeePosition, Document
from datetime import datetime

router = APIRouter()

@router.get("/add_employee")
async def get_add_employee_form(request: Request, db: Session = Depends(get_db)):
    # Получаем список физических лиц
    individuals = db.query(Individuals).all()
    return templates.TemplateResponse("add_employee.html", {"request": request, "individuals": individuals})

@router.post("/add_employee")
async def add_employee(
    # Выбор физического лица из списка
    individual_id: int = Form(...),  # ID физического лица из таблицы Individuals

    # Данные для таблицы Employee
    education_level: str = Form(...),
    rating: int = Form(...),
    date_priem: str = Form(...),
    date_uvol: str = Form(None),
    comment: str = Form(None),

    # Данные для таблицы Education
    education_spec: str = Form(...),
    education_qual: str = Form(...),
    education_institute: str = Form(...),
    education_year_finish: int = Form(...),

    # Данные для таблицы BankCards
    number_bank_kar: str = Form(...),
    bank: str = Form(...),

    # Данные для таблицы Positions
    rank: str = Form(...),
    wage: float = Form(...),

    # Данные для таблицы EmployeePositions
    discharge: int = Form(...),

    # Данные для таблицы Documents
    document_type: str = Form(...),
    document_seria: str = Form(...),
    document_number: str = Form(...),
    date_document: str = Form(...),
    document_who: str = Form(...),

    # Данные для таблицы IdentificationInfo
    inn: int = Form(...),
    snils: str = Form(...),

    db: Session = Depends(get_db)
):
    # Проверяем, существует ли выбранное физическое лицо
    individual = db.query(Individuals).filter_by(IndividualsID=individual_id).first()
    if not individual:
        raise HTTPException(status_code=404, detail="Физическое лицо не найдено")

    # Создаем запись в таблице Employee, используя данные из физического лица
    new_employee = Employee(
        IndividualsID=individual.IndividualsID,  # Связь с таблицей Individuals
        Familiya=individual.Familiya,
        Imya=individual.Imya,
        Otchestvo=individual.Otchestvo,
        DateOfBirth=individual.DateOfBirth,
        Address=individual.Address,
        Phone=individual.Phone,
        EducationLevel=education_level,
        Rating=rating,
        DatePriem=datetime.strptime(date_priem, "%Y-%m-%d"),
        DateUvol=datetime.strptime(date_uvol, "%Y-%m-%d") if date_uvol else None,
        Comment=comment,
        Inn=inn,
        Snils=snils
    )
    db.add(new_employee)
    db.flush()  # Получаем RegNumber для последующего использования

    # Запись в таблицу Education
    new_education = Education(
        RegNumber=new_employee.RegNumber,
        EducationSpec=education_spec,
        EducationQual=education_qual,
        EducationInstitute=education_institute,
        EducationYearFinish=education_year_finish
    )
    db.add(new_education)

    # Запись в таблицу BankCards
    new_bank_card = BankCard(
        RegNumber=new_employee.RegNumber,
        NumberBankKar=number_bank_kar,
        Bank=bank
    )
    db.add(new_bank_card)

    # Запись в таблицу Positions
    new_position = Position(
        Rank=rank,
        Wage=wage
    )
    db.add(new_position)
    db.flush()  # Получаем PositionID для связи с EmployeePositions

    # Запись в таблицу EmployeePositions
    new_employee_position = EmployeePosition(
        RegNumber=new_employee.RegNumber,
        PositionID=new_position.PositionID,
        Discharge=discharge
    )
    db.add(new_employee_position)

    # Запись в таблицу Documents
    new_document = Document(
        RegNumber=new_employee.RegNumber,
        DocumentType=document_type,
        DocumentSeria=document_seria,
        DocumentNumber=document_number,
        DateDocument=datetime.strptime(date_document, "%Y-%m-%d"),
        DocumentWho=document_who
    )
    db.add(new_document)

    # Финальное сохранение данных
    db.commit()
    return RedirectResponse("/", status_code=303)

@router.get("/delete/{regnumber}")
async def delete_employee(regnumber: int, db: Session = Depends(get_db)):
    employee = []
    employee.append(db.query(Employee).filter(Employee.RegNumber == regnumber).first())
    employee.append(db.query(Education).filter(Education.RegNumber == regnumber).first())
    employee.append(db.query(EmployeePosition).filter(EmployeePosition.RegNumber == regnumber).first())
    employee.append(db.query(BankCard).filter(BankCard.RegNumber == regnumber).first())
    employee.append(db.query(Position).filter(Position.PositionID == regnumber).first())
    employee.append(db.query(Document).filter(Document.RegNumber == regnumber).first())
    if employee:
        for i in employee:
            db.delete(i)
        db.commit()
    return RedirectResponse("/", status_code=303)


@router.get("/edit/{regnumber}", response_class=HTMLResponse)
async def edit_employee_form(request: Request, regnumber: int, db: Session = Depends(get_db)):
    # Извлекаем сотрудника
    employee = db.query(Employee).filter(Employee.RegNumber == regnumber).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")

    # Получаем физическое лицо, связанное с сотрудником
    individual = employee.individual

    # Извлекаем остальные данные
    education = db.query(Education).filter(Education.RegNumber == regnumber).first()
    bank_card = db.query(BankCard).filter(BankCard.RegNumber == regnumber).first()
    position = (
        db.query(Position)
        .join(EmployeePosition, EmployeePosition.PositionID == Position.PositionID)
        .filter(EmployeePosition.RegNumber == regnumber)
        .first()
    )
    employee_position = db.query(EmployeePosition).filter(EmployeePosition.RegNumber == regnumber).first()
    document = db.query(Document).filter(Document.RegNumber == regnumber).first()

    return templates.TemplateResponse("edit_employee.html", {
        "request": request,
        "employee": employee,
        "individual": individual,  # Передаем данные физического лица
        "education": education,
        "bank_card": bank_card,
        "position": position,
        "employee_position": employee_position,
        "document": document,
    })

@router.post("/edit/{regnumber}")
async def edit_employee(
        regnumber: int,
        address: str = Form(...),
        phone: str = Form(...),
        education_level: str = Form(...),
        rating: int = Form(...),
        date_priem: str = Form(...),
        date_uvol: str = Form(None),
        comment: str = Form(None),

        education_spec: str = Form(...),
        education_qual: str = Form(...),
        education_institute: str = Form(...),
        education_year_finish: int = Form(...),

        number_bank_kar: str = Form(...),
        bank: str = Form(...),

        rank: str = Form(...),
        wage: float = Form(...),
        discharge: int = Form(...),

        document_type: str = Form(...),
        document_seria: str = Form(...),
        document_number: str = Form(...),
        date_document: str = Form(...),
        document_who: str = Form(...),

        inn: int = Form(...),
        snils: str = Form(...),

        db: Session = Depends(get_db)
):
    # Получаем запись сотрудника из базы
    employee = db.query(Employee).filter(Employee.RegNumber == regnumber).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")

    # Обновление данных сотрудника
    employee.Address = address
    employee.Phone = phone
    employee.EducationLevel = education_level
    employee.Rating = rating
    employee.DatePriem = datetime.strptime(date_priem, "%Y-%m-%d")
    employee.DateUvol = datetime.strptime(date_uvol, "%Y-%m-%d") if date_uvol else None
    employee.Comment = comment
    employee.Inn = inn
    employee.Snils = snils

    # Обновление таблицы Education
    education = db.query(Education).filter(Education.RegNumber == regnumber).first()
    if education:
        education.EducationSpec = education_spec
        education.EducationQual = education_qual
        education.EducationInstitute = education_institute
        education.EducationYearFinish = education_year_finish

    # Обновление таблицы BankCard
    bank_card = db.query(BankCard).filter(BankCard.RegNumber == regnumber).first()
    if bank_card:
        bank_card.NumberBankKar = number_bank_kar
        bank_card.Bank = bank

    # Обновление таблицы Position и EmployeePosition
    position = (
        db.query(Position)
        .join(EmployeePosition, EmployeePosition.PositionID == Position.PositionID)
        .filter(EmployeePosition.RegNumber == regnumber)
        .first()
    )
    if position:
        position.Rank = rank
        position.Wage = wage

    employee_position = db.query(EmployeePosition).filter(EmployeePosition.RegNumber == regnumber).first()
    if employee_position:
        employee_position.Discharge = discharge

    # Обновление таблицы Document
    document = db.query(Document).filter(Document.RegNumber == regnumber).first()
    if document:
        document.DocumentType = document_type
        document.DocumentSeria = document_seria
        document.DocumentNumber = document_number
        document.DateDocument = datetime.strptime(date_document, "%Y-%m-%d")
        document.DocumentWho = document_who


    # Сохранение изменений
    db.commit()
    return RedirectResponse("/", status_code=303)

@router.get("/details/{regnumber}", response_class=HTMLResponse)
async def employee_details(request: Request, regnumber: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.RegNumber == regnumber).first()
    education = db.query(Education).filter(Education.RegNumber == regnumber).first()
    bank_card = db.query(BankCard).filter(BankCard.RegNumber == regnumber).first()
    position = (
        db.query(Position)
        .join(EmployeePosition, EmployeePosition.PositionID == Position.PositionID)
        .filter(EmployeePosition.RegNumber == regnumber)
        .first()
    )
    employee_position = db.query(EmployeePosition).filter(EmployeePosition.RegNumber == regnumber).first()
    document = db.query(Document).filter(Document.RegNumber == regnumber).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")

    return templates.TemplateResponse("employee_details.html", {
        "request": request,
        "employee": employee,
        "education": education,
        "bank_card": bank_card,
        "position": position,
        "employee_position": employee_position,
        "document": document,
    })