import logging
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from typing import List, Deque, Optional, Any
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    filename='task_manager.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

class BaseTask(ABC):
    """Базовый абстрактный класс с встроенной иерархией исключений"""
    
    def __init__(self, title: str):
        self._title = title  # Защищенный атрибут 
        logger.info(f"Создана базовая задача: {title}")
        
    # Иерархия исключений 
    class TaskError(Exception):
        """Базовое исключение для задач"""
        def __init__(self, message="Ошибка в системе задач"):
            self.message = message
            super().__init__(message)
            logger.error(f"TaskError: {message}")
            
        def __str__(self):
            return f"Ошибка задачи: {self.message}"

    class TaskNotFoundError(TaskError):
        """Задача не найдена"""
        def __init__(self, task_title=""):
            message = f"Задача '{task_title}' не найдена"
            super().__init__(message)
            logger.error(f"TaskNotFoundError: {message}")

    class ValidationError(TaskError):
        """Ошибка валидации данных"""
        def __init__(self, message="Ошибка валидации"):
            super().__init__(message)
            logger.error(f"ValidationError: {message}")

    class PriorityError(ValidationError):
        """Некорректный приоритет"""
        def __init__(self, priority):
            message = f"Приоритет {priority} должен быть между 1 и 5"
            super().__init__(message)
            logger.error(f"PriorityError: {message}")

    @abstractmethod
    def display_info(self) -> str:
        pass
        
    def get_basic_info(self) -> str:
        return f"Базовая информация: {self._title}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(title='{self._title}')"

@dataclass
class Task(BaseTask):
    _title: str
    description: str
    due_date: str
    priority: int = 1
    is_completed: bool = False
    total_tasks: int = field(default=0, init=False, repr=False)  # Статическое поле
    
    def __post_init__(self):
        super().__init__(self._title)  # Вызов конструктора базового класса
        self._validate_priority()
        Task.total_tasks += 1
        logger.info(f"Создана задача: {self._title}")
        
    def _validate_priority(self):  # Защищенный метод 
        if not 1 <= self.priority <= 5:
            logger.warning(f"Некорректный приоритет: {self.priority}")
            raise BaseTask.PriorityError(self.priority)
    
    @property
    def title(self) -> str:
        return self._title
        
    # Переопределение метода 
    def display_info(self) -> str:
        base_info = super().get_basic_info()
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
        logger.info(f"Задача '{self._title}' отмечена как выполненная")

    @staticmethod
    def get_total_tasks() -> int:
        return Task.total_tasks

    def __str__(self) -> str:
        return self._title

    def __add__(self, other: 'Task') -> str:  # Перегрузка оператора 
        if isinstance(other, Task):
            logger.info(f"Объединение задач: {self._title} и {other._title}")
            return f"Объединенные задачи: {self._title} и {other._title}"
        logger.error("Попытка объединения с объектом не типа Task")
        raise BaseTask.ValidationError("Операция '+' поддерживается только для объектов Task")

    def __eq__(self, other: Any) -> bool:  # Перегрузка оператора 
        if not isinstance(other, Task):
            return False
        return self._title == other._title

@dataclass
class UrgentTask(Task):
    """Производный класс для срочных задач"""
    emergency_level: int = 1
    
    def __post_init__(self):
        super().__post_init__()
        logger.info(f"Создана срочная задача: {self._title}")
    
    # Переопределение метода display_info
    def display_info(self) -> str:
        base_info = super().display_info()
        return f"{base_info}, Уровень срочности: {self.emergency_level}"
    
    def extend_deadline(self, days: int) -> None:
        """Увеличивает срок выполнения задачи"""
        logger.info(f"Срок для задачи '{self._title}' увеличен на {days} дней")
        # Здесь должна быть логика изменения due_date

@dataclass
class RecurringTask(Task):
    """Производный класс для повторяющихся задач"""
    recurrence_pattern: str = "daily"
    next_occurrence: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    
    def __post_init__(self):
        super().__post_init__()
        logger.info(f"Создана повторяющаяся задача: {self._title}")
    
    # Переопределение метода display_info
    def display_info(self) -> str:
        base_info = super().display_info()
        return f"{base_info}, Повтор: {self.recurrence_pattern}, Следующее выполнение: {self.next_occurrence}"
    
    def reschedule(self, new_date: str) -> None:
        """Переносит задачу на новую дату"""
        logger.info(f"Повторяющаяся задача '{self._title}' перенесена на {new_date}")
        self.next_occurrence = new_date

class TaskList:
    """Класс для работы с динамическими структурами данных"""
    
    class DuplicateTaskError(BaseTask.TaskError):
        """Попытка добавить существующую задачу"""
        def __init__(self, message="Дубликат задачи"):
            super().__init__(message)
            logger.error(f"DuplicateTaskError: {message}")
    
    def __init__(self):
        self._tasks: Deque[Task] = deque()  # Динамическая структура
        self._completed_tasks: List[Task] = []
        logger.info("Создан новый список задач")
        
    def add_task(self, task: Task) -> None:
        try:
            if not isinstance(task, Task):
                logger.error("Попытка добавить объект не типа Task")
                raise BaseTask.ValidationError("Можно добавлять только объекты типа Task")
            if task in self._tasks:
                logger.warning(f"Попытка добавить существующую задачу: {task.title}")
                raise TaskList.DuplicateTaskError(f"Задача '{task.title}' уже существует")
            self._tasks.append(task)
            logger.info(f"Задача '{task.title}' добавлена в список")
        except BaseTask.TaskError as e:
            logger.error(f"Ошибка при добавлении задачи: {e}")
            raise
        finally:  # Блок finally 
            logger.info(f"Текущее количество задач: {len(self._tasks)}")
            print(f"Задач в списке: {len(self._tasks)}")
    
    def remove_task(self, task: Task) -> None:
        try:
            self._tasks.remove(task)
            logger.info(f"Задача '{task.title}' удалена из списка")
        except ValueError:
            logger.error(f"Задача '{task.title}' не найдена при удалении")
            raise BaseTask.TaskNotFoundError(str(task))
    
    def complete_task(self, task: Task) -> None:
        try:
            self._tasks.remove(task)
            task.mark_as_completed()
            self._completed_tasks.append(task)
            logger.info(f"Задача '{task.title}' выполнена и перемещена в архив")
        except ValueError:
            logger.error(f"Задача '{task.title}' не найдена при выполнении")
            raise BaseTask.TaskNotFoundError(str(task))
    
    def get_all_tasks(self) -> List[Task]:
        logger.info("Запрошен список всех задач")
        return list(self._tasks)
    
    def get_completed_tasks(self) -> List[Task]:
        logger.info("Запрошен список выполненных задач")
        return self._completed_tasks
    
    # Работа с двумерным списком
    def find_max_in_2d(self, tasks_2d: List[List[Task]], attribute: str) -> Optional[Task]:
        try:
            if not tasks_2d:
                logger.warning("Пустой двумерный список задач")
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
            
            if max_task:
                logger.info(f"Найдена задача с максимальным {attribute}: {max_task.title}")
            else:
                logger.warning(f"Не найдено задач с атрибутом {attribute}")
            
            return max_task
        except Exception as e:
            logger.error(f"Ошибка при поиске максимального значения: {e}")
            raise BaseTask.TaskError(f"Ошибка при поиске: {e}")

    # Метод с лямбда-выражениями для фильтрации задач
    def filter_tasks(self, condition) -> List[Task]:
        """Фильтрует задачи по условию (лямбда-функции)"""
        logger.info(f"Фильтрация задач по условию: {condition.__name__ if hasattr(condition, '__name__') else 'лямбда'}")
        return list(filter(condition, self._tasks))

    # Метод с лямбда-выражениями для сортировки задач
    def sort_tasks(self, key_func) -> List[Task]:
        """Сортирует задачи по ключу (лямбда-функции)"""
        logger.info(f"Сортировка задач по ключу: {key_func.__name__ if hasattr(key_func, '__name__') else 'лямбда'}")
        return sorted(self._tasks, key=key_func)

class TaskManager:
    """Класс для управления несколькими списками задач"""
    def __init__(self):
        self.task_lists: List[TaskList] = []  # Двумерная структура
        logger.info("Создан новый менеджер задач")
        
    def add_task_list(self, task_list: TaskList) -> None:
        self.task_lists.append(task_list)
        logger.info(f"Добавлен новый список задач. Всего списков: {len(self.task_lists)}")
    
    def find_global_max_priority(self) -> Optional[Task]:
        logger.info("Поиск задачи с максимальным приоритетом")
        return self.task_lists[0].find_max_in_2d([self.task_lists], 'priority') if self.task_lists else None

    # Метод с лямбда-выражением для обработки всех задач
    def process_all_tasks(self, action) -> None:
        """Применяет действие (лямбда-функцию) ко всем задачам"""
        logger.info(f"Применение действия ко всем задачам: {action.__name__ if hasattr(action, '__name__') else 'лямбда'}")
        for task_list in self.task_lists:
            for task in task_list.get_all_tasks():
                action(task)

def main():
    try:
        logger.info("Начало работы программы")
        
        # Создаем задачи разных типов
        task1 = Task("Проект", "Завершить проект", "2025-01-30", 3)
        task2 = UrgentTask("Учеба", "Подготовиться к экзамену", "2025-02-15", 5, emergency_level=3)
        task3 = RecurringTask("Дом", "Уборка", "2025-01-20", 2, recurrence_pattern="weekly")
        
        # Демонстрация полиморфизма
        tasks = [task1, task2, task3]
        for task in tasks:
            print(task.display_info())  # Каждый объект вызывает свою версию метода
            
        # Демонстрация строкового представления 
        print(repr(task1))  # __repr__
        print(task1)        # __str__
        print(task1 + task2)  # __add__
        
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
        except BaseTask.TaskNotFoundError as e:
            print(f"Поймано исключение: {e}")
        
        # Доступ к защищенному атрибуту
        print(f"Защищенный атрибут: {task1._title}")
        
        # Демонстрация TaskManager
        manager = TaskManager()
        manager.add_task_list(task_list)
        global_max = manager.find_global_max_priority()
        print(f"Глобальная задача с максимальным приоритетом: {global_max}")
        
        # Примеры использования лямбда-выражений
        print("\nИспользование лямбда-выражений:")
        
        # Фильтрация задач с приоритетом > 2
        high_priority_tasks = task_list.filter_tasks(lambda t: t.priority > 2)
        print(f"Задачи с высоким приоритетом: {[t.title for t in high_priority_tasks]}")
        
        # Сортировка задач по приоритету
        sorted_tasks = task_list.sort_tasks(lambda t: t.priority)
        print(f"Задачи, отсортированные по приоритету: {[t.title for t in sorted_tasks]}")
        
        # Применение действия ко всем задачам
        manager.process_all_tasks(lambda t: print(f"Обработка: {t.title}"))
        
        # Фильтрация срочных задач
        urgent_tasks = task_list.filter_tasks(lambda t: isinstance(t, UrgentTask))
        print(f"Срочные задачи: {[t.title for t in urgent_tasks]}")
        
    except BaseTask.TaskError as e:
        logger.critical(f"Критическая ошибка: {e}")
        print(f"Критическая ошибка: {e}")
    finally:
        logger.info("Программа завершена")
        print("Программа завершена")

if __name__ == "__main__":
    main()