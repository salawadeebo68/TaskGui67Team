from datetime import datetime


class NotificationService:
    def __init__(self, task_manager):
        self.task_manager = task_manager

    def check_notifications(self):
        alerts = []
        overdue = self.task_manager.get_overdue_tasks()
        for i, task in overdue:
            alerts.append(f"⚠️ เกินกำหนด: {task.title} (ครบ {task.deadline})")

        today = datetime.now().strftime("%Y-%m-%d")
        for task in self.task_manager.tasks:
            if task.deadline == today and not task.completed:
                alerts.append(f"🔔 ครบกำหนดวันนี้: {task.title}")
        return alerts