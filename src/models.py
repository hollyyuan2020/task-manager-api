from datetime import datetime
from typing import List, Optional

class Task:
    def __init__(self, id: int, title: str, description: str = "", 
                 status: str = "pending", created_at: datetime = None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status  # pending, in_progress, completed
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            status=data.get("status", "pending"),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else None
        )

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id = 1
    
    def create_task(self, title: str, description: str = "") -> Task:
        task = Task(self.next_id, title, description)
        self.tasks.append(task)
        self.next_id += 1
        return task
    
    def get_all_tasks(self) -> List[Task]:
        return self.tasks.copy()
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task_status(self, task_id: int, status: str) -> bool:
        task = self.get_task_by_id(task_id)
        if task:
            task.status = status
            return True
        return False
    
    def delete_task(self, task_id: int) -> bool:
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                return True
        return False

