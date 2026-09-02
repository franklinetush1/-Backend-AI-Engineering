from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

tasks = [
    {"id": 1, "title": "Finish CRUD project", "done": False},
    {"id": 2, "title": "Play the piano", "done": True},
    {"id": 3, "title": "Go for a walk", "done": False},
]

@app.get("/")
def read_root():
    return { 
        "name": "Task API", 
        "version": "1.0", 
        "endpoints": ["/tasks"] 
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
            
    return JSONResponse(
        status_code=404, 
        content={"error": f"Task {task_id} not found"}
    )


class CreateTask(BaseModel):
    title: Optional[str] = None 


@app.post("/tasks", status_code=201)
def add_task(task_data: CreateTask):
    if task_data.title is None or not task_data.title.strip():
        return JSONResponse(
            status_code=400, 
            content={"error": "The title is required and can't be empty"}
        )
    
    post_id = tasks[-1]["id"] + 1 if tasks else 1
    
    new_task = {
        "id": post_id,
        "title": task_data.title.strip(),
        "done": False
    }
    
    tasks.append(new_task)
    return new_task

class CreateTask(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: CreateTask):
    task = None
    for task in tasks:
        if task["id"] == task_id:
            task = task
            break

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

    if update.title is not None and not update.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title cannot be empty"}
        )

    if update.title is not None:
        task["title"] = update.title.strip()
    if update.done is not None:
        task["done"] = update.done

    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    task_idx = None
    for idx, task in enumerate(tasks):
        if task["id"] == task_id:
            task_idx = idx
            break

    if task_idx is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

    tasks.pop(task_idx)
    return None

