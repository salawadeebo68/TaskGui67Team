import json
import os
from models.task import Task, PriorityTask


class StorageService:
    FILE = "data/tasks.json"

    @staticmethod
    def save(tasks):
        os.makedirs("data", exist_ok=True)
        data = [t.to_dict() for t in tasks]
        with open(StorageService.FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load():
        tasks = []
        try:
            with open(StorageService.FILE, encoding="utf-8") as f:
                data = json.load(f)
            for item in data:
                if item.get("type") == "priority":
                    task = PriorityTask(
                        item["title"],
                        item.get("deadline", ""),
                        item.get("priority", "Medium"),
                        item.get("notes", "")
                    )
                else:
                    task = Task(
                        item["title"],
                        item.get("deadline", ""),
                        item.get("priority", "Medium")
                    )
                task.completed = item.get("completed", False)
                task.created_at = item.get("created_at", "")
                tasks.append(task)
        except Exception:
            pass
        return tasks