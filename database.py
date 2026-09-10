from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# Database Configuration (Modify with your local credentials)
DATABASE_URL = "postgresql://postgres:password@localhost:5432/task_db"

# Setup SQLAlchemy Connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Task Database Model
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

# Auto-create tables if they don't exist yet
Base.metadata.create_all(bind=engine)

# FastAPI Initialization
app = FastAPI(title="CLI Task Manager Backend")
