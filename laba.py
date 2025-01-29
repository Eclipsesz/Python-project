class Task:
    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.is_completed = False

    def mark_as_completed(self):
        self.is_completed = True


class TaskList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def get_all_tasks(self):
        return self.tasks


class Reminder:
    def __init__(self):
        self.reminders = []

    def add_reminder(self, task, reminder_time):
        self.reminders.append((task, reminder_time))

    def get_reminders(self):
        return self.reminders


class Category:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def get_tasks(self):
        return self.tasks

class User:
    def __init__(self, username):
        self.username = username
        self.task_list = TaskList()

    def add_task(self, task):
        self.task_list.add_task(task)

    def remove_task(self, task):
        self.task_list.remove_task(task)

    def get_all_tasks(self):
        return self.task_list.get_all_tasks()


def main():
    user1 = User("Иван")
    user2 = User("Михаил")

    task1 = Task("Работа над проектом", "Подготовить презентацию для встречи", "2025-30-01")
    task2 = Task("Прочитать книгу", "Завершить чтение", "2025-30-01")

    user1.add_task(task1)
    user2.add_task(task2)

    print(f"Задачи {user1.username}: {[task.title for task in user1.get_all_tasks()]}")
    print(f"Задачи {user2.username}: {[task.title for task in user2.get_all_tasks()]}")

    reminder = Reminder()
    reminder.add_reminder(task1, "2025-01-02 12:00")
    
    print(f"Напоминания: {reminder.get_reminders()}")

    task1.mark_as_completed()
    print(f"Задача '{task1.title}' выполнена: {task1.is_completed}")

    user1.remove_task(task1)
    print(f"Задачи {user1.username} после удаления: {[task.title for task in user1.get_all_tasks()]}")

if __name__ == "__main__":
    main()
