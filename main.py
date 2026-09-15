from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session, Mapped, mapped_column

# 1. Database Configuration
DATABASE_URL = "postgresql://postgres:password@localhost:5432/task_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Database Model
class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True, default=None)
    completed: Mapped[bool] = mapped_column(default=False)

Base.metadata.create_all(bind=engine)

# 3. FastAPI Initialization
app = FastAPI(title="Task Manager API")

# 4. Dependency to get DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 5. Pydantic Schemas (For data validation)
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool

    class Config:
        from_attributes = True

# 6. FastAPI Route Endpoints
@app.get("/tasks", response_model=List[TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(Task).order_by(Task.id).all()

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def add_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    if not task_data.title.strip():
        raise HTTPException(status_code=400, detail="Task title cannot be empty")
    new_task = Task(title=task_data.title, description=task_data.description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task ID not found")
    
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed

    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task ID not found")
    db.delete(task)
    db.commit()
    return None
