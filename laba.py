from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from typing import List, Tuple, Deque, Optional, Any

# Иерархия пользовательских исключений
class TaskError(BaseException):
    """Базовое исключение для задач"""
    pass

class TaskNotFoundError(TaskError):
    """Задача не найдена"""
    pass

class TaskValidationError(TaskError):
    """Ошибка валидации задачи"""
    pass

class PriorityValidationError(TaskValidationError):
    """Некорректный приоритет"""
    pass

# Наследование и конструкторы
class BaseTask(ABC):
    def __init__(self, title: str):
        self._title = title  # Защищенный атрибут
        
    @abstractmethod
    def display_info(self) -> str:
        pass
        
    def get_basic_info(self) -> str:
        return f"Базовая информация: {self._title}"
    
    # Строковое представление
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(title='{self._title}')"

# Защищенные атрибуты + Наследование
@dataclass
class Task(BaseTask):
    _title: str
    description: str
    due_date: str
    priority: int = 1
    is_completed: bool = False
    total_tasks: int = field(default=0, init=False, repr=False)
    
    def __post_init__(self):
        super().__init__(self._title)  # 5. Вызов конструктора базового класса
        self._validate_priority()
        Task.total_tasks += 1
        
    @property
    def title(self) -> str:
        return self._title
        
    # Защищенный метод
    def _validate_priority(self):
        if not 1 <= self.priority <= 5:
            raise PriorityValidationError("Приоритет должен быть между 1 и 5")
    
    # Переопределение метода
    def display_info(self) -> str:
        base_info = super().get_basic_info()  # Вызов метода базового класса
        return (f"{base_info}, Описание: {self.description}, "
                f"Дата: {self.due_date}, Приоритет: {self.priority}, "
                f"Выполнена: {self.is_completed}")
    
    # Метод, использующий и базовый и переопределенный методы
    def get_full_info(self, detailed: bool = True) -> str:
        if detailed:
            return f"Подробно: {self.display_info()}"
        return super().get_basic_info()
    
    def mark_as_completed(self) -> None:
        self.is_completed = True

    @staticmethod
    def get_total_tasks() -> int:
        return Task.total_tasks

    def __str__(self) -> str:
        return self._title

    def __add__(self, other: 'Task') -> str:
        if isinstance(other, Task):
            return f"Объединенные задачи: {self._title} и {other._title}"
        raise TypeError("Операция '+' поддерживается только для объектов Task")

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Task):
            return False
        return self._title == other._title

# Работа с массивами объектов
class TaskList:
    def __init__(self):
        self._tasks: Deque[Task] = deque()
        self._completed_tasks: List[Task] = []
        
    def add_task(self, task: Task) -> None:
        try:
            if not isinstance(task, Task):
                raise TaskValidationError("Можно добавлять только объекты типа Task")
            self._tasks.append(task)
        except TaskValidationError as e:
            print(f"Ошибка валидации: {e}")
            raise
        finally:  # 1. Блок finally
            print("Завершение операции добавления задачи")
    
    def remove_task(self, task: Task) -> None:
        try:
            self._tasks.remove(task)
        except ValueError:
            raise TaskNotFoundError(f"Задача '{task}' не найдена в списке")
    
    def complete_task(self, task: Task) -> None:
        try:
            self._tasks.remove(task)
            task.mark_as_completed()
            self._completed_tasks.append(task)
        except ValueError:
            raise TaskNotFoundError(f"Задача '{task}' не найдена")
    
    def get_all_tasks(self) -> List[Task]:
        return list(self._tasks)
    
    def get_completed_tasks(self) -> List[Task]:
        return self._completed_tasks
    
    # Работа с двумерным списком
    def find_max_in_2d(self, tasks_2d: List[List[Task]], attribute: str) -> Optional[Task]:
        try:
            if not tasks_2d:
                return None
                
            max_task = None
            max_value = float('-inf')
            
            for row in tasks_2d:
                for task in row:
                    if hasattr(task, attribute):
                        value = getattr(task, attribute)
                        if value > max_value:
                            max_value = value
                            max_task = task
            
            return max_task
        except Exception as e:
            print(f"Ошибка при поиске: {e}")
            return None

class TaskManager:
    def __init__(self):
        self.task_lists: List[TaskList] = []  # Двумерная структура
        
    def add_task_list(self, task_list: TaskList) -> None:
        self.task_lists.append(task_list)
    
    def find_global_max_priority(self) -> Optional[Task]:
        return self.task_lists[0].find_max_in_2d([self.task_lists], 'priority') if self.task_lists else None

def main():
    try:
        # Создаем задачи
        task1 = Task("Проект", "Завершить проект", "2025-01-30", 3)
        task2 = Task("Учеба", "Подготовиться к экзамену", "2025-02-15", 4)
        task3 = Task("Дом", "Уборка", "2025-01-20", 2)
        
        # Демонстрация __repr__
        print(repr(task1))
        print(task1.get_full_info(True))
        print(task1.get_full_info(False))
        
        # Работа с TaskList
        task_list = TaskList()
        task_list.add_task(task1)
        task_list.add_task(task2)
        task_list.add_task(task3)
        
        # Демонстрация работы с двумерным массивом
        tasks_2d = [
            [task1, task2],
            [task3]
        ]
        max_priority_task = task_list.find_max_in_2d(tasks_2d, 'priority')
        print(f"Задача с максимальным приоритетом: {max_priority_task}")
        
        # Обработка исключений
        try:
            task_list.complete_task(Task("Несуществующая", "", "", 1))
        except TaskNotFoundError as e:
            print(f"Поймано исключение: {e}")
        
        # Доступ к защищенному атрибуту
        print(f"Защищенный атрибут: {task1._title}")
        
        # Демонстрация TaskManager
        manager = TaskManager()
        manager.add_task_list(task_list)
        global_max = manager.find_global_max_priority()
        print(f"Глобальная задача с максимальным приоритетом: {global_max}")
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        print("Программа завершена")

if __name__ == "__main__":
    main()