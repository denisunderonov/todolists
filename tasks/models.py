from django.db import models  # Импортируем модели Django
from django.contrib.auth.models import User  # Встроенная модель пользователя Django
from simple_history.models import HistoricalRecords  # Для отслеживания истории изменений


# Модель: Приоритет задачи (справочник)
class Priority(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')  # Название приоритета (например, "Низкий", "Высокий")
    level = models.IntegerField(unique=True, verbose_name='Уровень')  # Числовой уровень приоритета (1-5)

    history = HistoricalRecords()  # Отслеживание истории изменений

    class Meta:
        verbose_name = 'Приоритет'  # Название модели в единственном числе
        verbose_name_plural = 'Приоритеты'  # Название модели во множественном числе
        ordering = ['level']  # Сортировка по уровню приоритета

    def __str__(self):
        return self.name  # Строковое представление объекта


# Модель: Статус задачи (справочник)
class Status(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')  # Название статуса (например, "Новая", "В работе", "Завершена")
    color = models.CharField(max_length=7, default='#808080', verbose_name='Цвет')  # Цвет в формате HEX для визуализации

    history = HistoricalRecords()  # Отслеживание истории изменений

    class Meta:
        verbose_name = 'Статус'  # Название модели в единственном числе
        verbose_name_plural = 'Статусы'  # Название модели во множественном числе
        ordering = ['name']  # Сортировка по названию

    def __str__(self):
        return self.name  # Строковое представление объекта


# Модель: Тег (справочник)
class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')  # Название тега (например, "Работа", "Личное")
    color = models.CharField(max_length=7, default='#007bff', verbose_name='Цвет')  # Цвет тега в формате HEX
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')  # К какому пользователю относится тег

    history = HistoricalRecords()  # Отслеживание истории изменений

    class Meta:
        verbose_name = 'Тег'  # Название модели в единственном числе
        verbose_name_plural = 'Теги'  # Название модели во множественном числе
        ordering = ['name']  # Сортировка по названию
        unique_together = ['name', 'user']  # Уникальность: один пользователь не может создать два тега с одинаковым именем

    def __str__(self):
        return f'{self.name} ({self.user.username})'  # Строковое представление объекта


# Модель: Проект (список задач)
class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')  # Название проекта
    description = models.TextField(blank=True, null=True, verbose_name='Описание')  # Описание проекта (необязательное)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects', verbose_name='Владелец')  # Владелец проекта
    image = models.ImageField(upload_to='projects/', null=True, blank=True, verbose_name='Изображение')  # Изображение проекта
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')  # Автоматически заполняется при создании
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')  # Автоматически обновляется при изменении

    history = HistoricalRecords()  # Отслеживание истории изменений

    class Meta:
        verbose_name = 'Проект'  # Название модели в единственном числе
        verbose_name_plural = 'Проекты'  # Название модели во множественном числе
        ordering = ['-created_at']  # Сортировка по дате создания (новые первые)

    def __str__(self):
        return self.name  # Строковое представление объекта


# Модель: Задача
class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')  # Название задачи
    description = models.TextField(blank=True, null=True, verbose_name='Описание')  # Описание задачи (необязательное)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', verbose_name='Проект')  # К какому проекту относится задача
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True, verbose_name='Приоритет')  # Приоритет задачи (при удалении приоритета ставится NULL)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, verbose_name='Статус')  # Статус задачи
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks', verbose_name='Назначена')  # Кому назначена задача (необязательно)
    due_date = models.DateTimeField(null=True, blank=True, verbose_name='Срок выполнения')  # Дата и время дедлайна (необязательно)
    image = models.ImageField(upload_to='tasks_images/', null=True, blank=True, verbose_name='Изображение')  # Прикрепленное изображение (необязательно)
    tags = models.ManyToManyField(Tag, blank=True, related_name='tasks', verbose_name='Теги')  # Связь многие-ко-многим с тегами

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')  # Когда задача была создана
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')  # Когда задача была изменена
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tasks', verbose_name='Создал')  # Кто создал задачу

    history = HistoricalRecords()  # Отслеживание истории изменений

    class Meta:
        verbose_name = 'Задача'  # Название модели в единственном числе
        verbose_name_plural = 'Задачи'  # Название модели во множественном числе
        ordering = ['-created_at']  # Сортировка по дате создания (новые первые)

    def __str__(self):
        return self.title  # Строковое представление объекта
