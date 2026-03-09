from datetime import datetime


class Task:
    def __init__(self, title, deadline="", priority="Medium"):
        self.title = title
        self.deadline = deadline
        self.priority = priority
        self.completed = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def mark_done(self):
        self.completed = True

    def to_dict(self):
        return {
            "title": self.title,
            "deadline": self.deadline,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at
        }

    def __str__(self):
        status = "✓" if self.completed else "○"
        deadline_str = f" | 📅 {self.deadline}" if self.deadline else ""
        return f"{status} [{self.priority}] {self.title}{deadline_str}"


class PriorityTask(Task):
    PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}

    def __init__(self, title, deadline="", priority="High", notes=""):
        super().__init__(title, deadline, priority)
        self.notes = notes

    def get_priority_level(self):
        return self.PRIORITY_ORDER.get(self.priority, 1)

    def to_dict(self):
        d = super().to_dict()
        d["notes"] = self.notes
        d["type"] = "priority"
        return d

    def __str__(self):
        base = super().__str__()
        if self.notes:
            return f"{base}\n   📝 {self.notes}"
        return base