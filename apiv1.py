from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

class Task(BaseModel):
    task_name: str
    task_details: str
    is_done: bool = False

class TaskDB:
    def __init__(self):
        self.tasks: List[Dict] = [
            {"task_id": 1, "task_name": "Lab Activity", "task_details": "Complete Lab 2", "is_done": False}
        ]
        self.current_id = 2

    def get_task(self, task_id: int):
        task = next((task for task in self.tasks if task["task_id"] == task_id), None)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
        return task

    def add_task(self, task_data: Task):
        new_task = {
            "task_id": self.current_id,
            **task_data.dict()
        }
        self.tasks.append(new_task)
        self.current_id += 1
        return new_task

    def update_task(self, task_id: int, task_data: Task):
        task = self.get_task(task_id)
        task.update(task_data.dict(exclude_unset=True))
        return task

    def remove_task(self, task_id: int):
        task = self.get_task(task_id)
        self.tasks.remove(task)
        return task

    def replace_task(self, task_id: int, task_data: Task):
        task = self.get_task(task_id)
        task.clear()  
        task.update({"task_id": task_id, **task_data.dict()})
        return task

task_db = TaskDB()

@app.get("/tasks/{task_id}")
def fetch_task(task_id: int):
    task = task_db.get_task(task_id)
    return {"status": "success", "task": task}

@app.post("/tasks")
def create_task(task: Task):
    new_task = task_db.add_task(task)
    return {"status": "success", "task": new_task}

@app.put("/tasks/{task_id}")
def replace_task(task_id: int, task_data: Task):
    replaced_task = task_db.replace_task(task_id, task_data)
    return {"status": "success", "task": replaced_task}

@app.patch("/tasks/{task_id}")
def modify_task(task_id: int, task_data: Task):
    updated_task = task_db.update_task(task_id, task_data)
    return {"status": "success", "task": updated_task}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    task_db.remove_task(task_id)
    return {"status": "success", "message": f"Task {task_id} has been deleted"}


