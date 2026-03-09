from models.task import Task, PriorityTask
from services.storage_service import StorageService


class TaskManager:
    def __init__(self):
        self.tasks = StorageService.load()

    def add_task(self, title, deadline="", priority="Medium", notes=""):
        if notes:
            task = PriorityTask(title, deadline, priority, notes)
        else:
            task = Task(title, deadline, priority)
        self.tasks.append(task)
        self.save()

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save()

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_done()
            self.save()

    def edit_task(self, index, title, deadline, priority):
        if 0 <= index < len(self.tasks):
            self.tasks[index].title = title
            self.tasks[index].deadline = deadline
            self.tasks[index].priority = priority
            self.save()

    def get_tasks(self, filter_priority=None, search_text="", show_completed=True):
        result = self.tasks
        if not show_completed:
            result = [t for t in result if not t.completed]
        if filter_priority and filter_priority != "All":
            result = [t for t in result if t.priority == filter_priority]
        if search_text:
            result = [t for t in result if search_text.lower() in t.title.lower()]
        return result

    def get_overdue_tasks(self):
        from datetime import datetime
        overdue = []
        for i, task in enumerate(self.tasks):
            if task.deadline and not task.completed:
                try:
                    dl = datetime.strptime(task.deadline, "%Y-%m-%d")
                    if dl < datetime.now():
                        overdue.append((i, task))
                except Exception:
                    pass
        return overdue

    def save(self):
        StorageService.save(self.tasks)