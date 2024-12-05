from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Создаем подключение к базе данных SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Сессия для взаимодействия с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()