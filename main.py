from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
from database import engine, Base, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# HOME PAGE - DISPLAY TASKS
@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "tasks": tasks}
    )


# ADD TASK
@app.post("/add")
def add_task(
    title: str = Form(...),
    description: str = Form(...),
    priority: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db)
):

    new_task = models.Task(
        title=title,
        description=description,
        priority=priority,
        status=status
    )

    db.add(new_task)
    db.commit()

    return RedirectResponse("/", status_code=303)


# DELETE TASK
@app.get("/delete/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):

    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    db.delete(task)
    db.commit()

    return RedirectResponse("/", status_code=303)


# EDIT PAGE
@app.get("/edit/{task_id}", response_class=HTMLResponse)
def edit_task_page(task_id: int, request: Request, db: Session = Depends(get_db)):

    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    return templates.TemplateResponse(
        "edit.html",
        {"request": request, "task": task}
    )


# UPDATE TASK
@app.post("/update/{task_id}")
def update_task(
    task_id: int,
    title: str = Form(...),
    description: str = Form(...),
    priority: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db)
):

    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    task.title = title
    task.description = description
    task.priority = priority
    task.status = status

    db.commit()

    return RedirectResponse("/", status_code=303)