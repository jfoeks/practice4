from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from database import Base

class Employee(Base):
    __tablename__ = "Employees"
    RegNumber = Column(Integer, primary_key=True, index=True,autoincrement=True)
    Familiya = Column(String(25))
    Imya = Column(String(25))
    Otchestvo = Column(String(25))
    DateOfBirth = Column(DateTime)
    Address = Column(String(255))
    Phone = Column(String(15))
    EducationLevel = Column(String(255))
    Rating = Column(Integer)
    DatePriem = Column(DateTime)
    DateUvol = Column(DateTime)
    Comment = Column(String(255))

class Education(Base):
    __tablename__ = "Education"
    EducationID = Column(Integer, primary_key=True, autoincrement=True)
    RegNumber = Column(Integer, ForeignKey("Employees.RegNumber"))
    EducationSpec = Column(String(255))
    EducationQual = Column(String(50))
    EducationInstitute = Column(String(255))
    EducationYearFinish = Column(Integer)

class Position(Base):
    __tablename__ = "Positions"
    PositionID = Column(Integer, primary_key=True, autoincrement=True)
    Rank = Column(String(25))
    Wage = Column(DECIMAL(10, 2))


class EmployeePosition(Base):
    __tablename__ = "EmployeePositions"
    EmpPosID = Column(Integer, primary_key=True, autoincrement=True)
    RegNumber = Column(Integer, ForeignKey("Employees.RegNumber"))
    PositionID = Column(Integer, ForeignKey("Positions.PositionID"))
    Discharge = Column(Integer)

class BankCard(Base):
    __tablename__ = "BankCards"
    CardID = Column(Integer, primary_key=True, autoincrement=True)
    RegNumber = Column(Integer, ForeignKey("Employees.RegNumber"))
    NumberBankKar = Column(String(60))
    Bank = Column(String(60))

class Rating(Base):
    __tablename__ = "Ratings"
    RatingID = Column(Integer, primary_key=True, autoincrement=True)
    RegNumber = Column(Integer, ForeignKey("Employees.RegNumber"))
    Rating = Column(Integer)

class Document(Base):
    __tablename__ = "Documents"
    DocumentID = Column(Integer, primary_key=True, autoincrement=True)
    RegNumber = Column(Integer, ForeignKey("Employees.RegNumber"))
    DocumentType = Column(String(25))
    DocumentSeria = Column(String(10))
    DocumentNumber = Column(String(10))
    DateDocument = Column(DateTime)
    DocumentWho = Column(String(255))

class IdentificationInfo(Base):
    __tablename__ = "IdentificationInfo"
    IdentificationID = Column(Integer, primary_key=True, autoincrement=True)
    RegNumber = Column(Integer, ForeignKey("Employees.RegNumber"))
    Inn = Column(Integer)
    Snils = Column(String(11))