from abc import ABC, abstractmethod
from collections import deque

class BaseTask(ABC):
    @abstractmethod
    def display_info(self):
        pass

class Task(BaseTask):
    total_tasks = 0
    
    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.is_completed = False
        Task.total_tasks += 1

    def mark_as_completed(self):
        self.is_completed = True

    def display_info(self):
        return f"Задача: {self.title}, Описание: {self.description}, Дата выполнения: {self.due_date}, Выполнена: {self.is_completed}"

    @staticmethod
    def get_total_tasks():
        return Task.total_tasks

    def __str__(self):
        return self.title

    def __add__(self, other):
        if isinstance(other, Task):
            return f"Объединенные задачи: {self.title} и {other.title}"
        else:
            raise TypeError("Операция '+' поддерживается только для объектов Task")

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.title == other.title
        return False


class TaskList:
    def __init__(self):
        self.tasks = deque()  # используем двустороннюю очередь

    def add_task(self, task):
        if not isinstance(task, Task):
            raise TypeError("Можно добавлять только объекты типа Task")
        self.tasks.append(task)

    def remove_task(self, task):
        try:
            self.tasks.remove(task)
        except ValueError:
            print(f"Задача '{task}' не найдена в списке.")

    def get_all_tasks(self):
        return list(self.tasks)

    def __len__(self):
        return len(self.tasks)


class Reminder:
    def __init__(self):
        self.reminders = deque()

    def add_reminder(self, task, reminder_time):
        if not isinstance(task, Task):
            raise TypeError("Можно добавлять напоминания только для объектов типа Task")
        self.reminders.append((task, reminder_time))

    def get_reminders(self):
        return list(self.reminders)


class User:
    def __init__(self, username):
        self.username = username
        self.task_list = TaskList()

    def add_task(self, task):
        try:
            self.task_list.add_task(task)
        except TypeError as e:
            print(e)

    def remove_task(self, task):
        try:
            self.task_list.remove_task(task)
        except Exception as e:
            print(f"Ошибка при удалении задачи: {e}")

    def get_all_tasks(self):
        return self.task_list.get_all_tasks()


def main():
    user1 = User("Иван")
    user2 = User("Михаил")

    task1 = Task("Работа над проектом", "Подготовить презентацию для встречи", "2025-30-01")
    task2 = Task("Прочитать книгу", "Завершить чтение", "2025-30-01")

    user1.add_task(task1)
    user2.add_task(task2)

    print(f"Задачи {user1.username}: {[str(task) for task in user1.get_all_tasks()]}")
    print(f"Задачи {user2.username}: {[str(task) for task in user2.get_all_tasks()]}")

    reminder = Reminder()
    reminder.add_reminder(task1, "2025-01-02 12:00")
    
    print(f"Напоминания: {reminder.get_reminders()}")

    task1.mark_as_completed()
    print(f"Задача '{task1.title}' выполнена: {task1.is_completed}")

    user1.remove_task(task1)
    print(f"Задачи {user1.username} после удаления: {[str(task) for task in user1.get_all_tasks()]}")
    
    # Демонстрация статического метода
    print(f"Общее количество задач: {Task.get_total_tasks()}")

    # Перегрузка оператора
    print(task1 + task2)
    print(f"Задача1 равна Задаче2: {task1 == task2}")


if __name__ == "__main__":
    main()
