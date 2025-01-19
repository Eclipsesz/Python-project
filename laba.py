# Task Scheduler
class Task:
    def __init__(self, title, description, due_date):
        self.title = title;
        self.description = description;
        self.due_date = due_date;
        self.comleted = False;

    def mark_as_completed(self):
        self.comleted = True;

class TaskList:
    def __init__(self):
        self.tasks = [];

    def add_task(self, task):
        self.tasks.append(task);

    def remove_task(self,task):
        self.tasks.remove(task);

    def get_all_tasks(self):
        return self.tasks;

class Reminder:
    def __init__(self):
        self.reminders = [];

    def add_reminder(self, task, reminder_time):
        self.reminders.append((task, reminder_time));

    def get_reminders(self):
        return self.reminders;

class Category:
    def __init__(self, name):
        self.name = name;
        self.tasks = [];

    def add_task(self, task):
        self.tasks.append(task);

    def get_tasks(self):
        return self.tasks;

class User:
    def __init__(self, username):
        self.username = username;
        self.task_list = TaskList();

    def add_task(self, task):
        self.task_list.add_task(task);

    def get_all_tasks(self):
        return self.task_list.get_all_tasks();
        