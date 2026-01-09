from django.db.models import Q  # Для сложных запросов с OR, AND, NOT
from django.utils import timezone  # Для работы с датами и временем
from rest_framework import viewsets, status  # Базовые классы для API и статусы ответов
from rest_framework.decorators import action  # Декоратор для дополнительных методов
from rest_framework.response import Response  # Для возврата JSON ответов
from datetime import timedelta  # Для работы с временными интервалами

from .models import Priority, Status, Tag, Project, Task  # Наши модели
from .serializers import (  # Наши сериализаторы
    PrioritySerializer, StatusSerializer, TagSerializer,
    ProjectSerializer, ProjectListSerializer,
    TaskSerializer, TaskListSerializer
)


# ViewSet для Priority (Приоритет)
class PriorityViewSet(viewsets.ModelViewSet):
    queryset = Priority.objects.all()  # Все приоритеты
    serializer_class = PrioritySerializer  # Сериализатор для приоритетов
    filterset_fields = ['level']  # Фильтрация по уровню (DjangoFilterBackend)
    search_fields = ['name']  # Поиск по названию
    ordering_fields = ['level', 'name']  # Сортировка по уровню или названию


# ViewSet для Status (Статус)
class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    search_fields = ['name']  # Поиск по названию статуса
    ordering_fields = ['name']


# ViewSet для Tag (Тег)
class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    filterset_fields = ['color']  # Фильтрация по цвету (DjangoFilterBackend)
    search_fields = ['name']  # Поиск по названию тега

    def get_queryset(self):  # Переопределяем queryset для фильтрации по пользователю
        """Возвращаем только теги текущего пользователя"""
        if self.request.user.is_authenticated:  # Если пользователь авторизован
            return Tag.objects.filter(user=self.request.user)  # Фильтрация по текущему пользователю
        return Tag.objects.none()  # Иначе пустой queryset

    def perform_create(self, serializer):  # Автоматически устанавливаем текущего пользователя при создании
        serializer.save(user=self.request.user)


# ViewSet для Project (Проект)
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    filterset_fields = ['owner']  # Фильтрация по владельцу (DjangoFilterBackend)
    search_fields = ['name', 'description']  # Поиск по названию и описанию
    ordering_fields = ['created_at', 'updated_at', 'name']  # Сортировка

    def get_queryset(self):
        """Возвращаем проекты текущего пользователя"""
        if self.request.user.is_authenticated:
            return Project.objects.filter(owner=self.request.user)  # Фильтрация по текущему пользователю
        return Project.objects.none()

    def get_serializer_class(self):  # Используем разные сериализаторы для списка и деталей
        if self.action == 'list':  # Для списка проектов
            return ProjectListSerializer  # Упрощенный сериализатор
        return ProjectSerializer  # Полный сериализатор для деталей

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Автоматически устанавливаем владельца

    @action(detail=False, methods=['get'])  # Дополнительный метод для списка (detail=False)
    def my_projects(self, request):
        """GET /api/projects/my_projects/ - Получить все проекты текущего пользователя"""
        projects = self.get_queryset()  # Получаем проекты пользователя
        serializer = self.get_serializer(projects, many=True)  # Сериализуем список
        return Response(serializer.data)  # Возвращаем JSON

    @action(detail=True, methods=['post'])  # Дополнительный метод для объекта (detail=True)
    def archive(self, request, pk=None):
        """POST /api/projects/{id}/archive/ - Архивировать проект (пример)"""
        project = self.get_object()  # Получаем конкретный проект
        # Здесь можно добавить логику архивирования (например, поле is_archived)
        return Response({
            'status': 'success',
            'message': f'Проект "{project.name}" архивирован',
            'project_id': project.id
        })


# ViewSet для Task (Задача) - основной с фильтрацией и Q-запросами
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filterset_fields = ['status', 'priority', 'project', 'assigned_to']  # Фильтрация (DjangoFilterBackend)
    search_fields = ['title', 'description']  # Поиск по названию и описанию
    ordering_fields = ['created_at', 'due_date', 'priority__level']  # Сортировка

    def get_queryset(self):
        """Базовый queryset с возможностью фильтрации"""
        queryset = Task.objects.select_related('project', 'priority', 'status', 'assigned_to', 'created_by').prefetch_related('tags')  # Оптимизация запросов

        # Фильтрация по статусу через URL (именованные аргументы)
        status_name = self.kwargs.get('status')  # Получаем статус из URL
        if status_name:
            queryset = queryset.filter(status__name=status_name)

        # Фильтрация по GET параметрам (priority)
        priority_level = self.request.query_params.get('priority_level')  # ?priority_level=5
        if priority_level:
            queryset = queryset.filter(priority__level=priority_level)

        # Фильтрация по GET параметрам (due_date)
        due_date_from = self.request.query_params.get('due_date_from')  # ?due_date_from=2026-01-10
        if due_date_from:
            queryset = queryset.filter(due_date__gte=due_date_from)

        due_date_to = self.request.query_params.get('due_date_to')  # ?due_date_to=2026-01-20
        if due_date_to:
            queryset = queryset.filter(due_date__lte=due_date_to)

        # Фильтрация по текущему пользователю
        if self.request.user.is_authenticated:
            queryset = queryset.filter(
                Q(project__owner=self.request.user)
                | Q(assigned_to=self.request.user)
                | Q(created_by=self.request.user)
            )

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer  # Упрощенный для списка
        return TaskSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)  # Автоматически устанавливаем создателя

    # Q-запрос 1: Задачи на ближайшие 7 дней
    @action(detail=False, methods=['get'])
    def upcoming_week(self, request):
        """GET /api/tasks/upcoming_week/ - Задачи на ближайшие 7 дней"""
        today = timezone.now()  # Текущая дата
        week_later = today + timedelta(days=7)  # Через 7 дней

        # Q-запрос: задачи со сроком в ближайшие 7 дней
        tasks = self.get_queryset().filter(
            Q(due_date__gte=today) & Q(due_date__lte=week_later)  # И дата >= сегодня И дата <= через 7 дней
        )

        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    # Q-запрос 2: Просроченные задачи
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """GET /api/tasks/overdue/ - Все просроченные задачи"""
        # Q-запрос: задачи с просроченным сроком и не завершенные
        tasks = self.get_queryset().filter(
            Q(due_date__lt=timezone.now())
            & ~Q(status__name='Завершена')
        )

        serializer = self.get_serializer(tasks, many=True)
        return Response({
            'count': tasks.count(),
            'tasks': serializer.data
        })

    # Q-запрос 3: Задачи с высоким приоритетом и не завершенные ИЛИ задачи на завтра
    @action(detail=False, methods=['get'])
    def urgent_or_tomorrow(self, request):
        """GET /api/tasks/urgent_or_tomorrow/ - Срочные незавершенные задачи ИЛИ задачи на завтра"""
        tomorrow = timezone.now() + timedelta(days=1)  # Завтра
        tomorrow_start = tomorrow.replace(hour=0, minute=0, second=0)  # Начало завтрашнего дня
        tomorrow_end = tomorrow.replace(hour=23, minute=59, second=59)  # Конец завтрашнего дня

        # Сложный Q-запрос с OR и AND
        tasks = self.get_queryset().filter(
            (Q(priority__level__gte=4) & ~Q(status__name='Завершена'))
            | Q(due_date__range=[tomorrow_start, tomorrow_end])
        )

        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    # Q-запрос 4: Задачи НЕ текущего пользователя И (статус "В работе" ИЛИ "Отменена")
    @action(detail=False, methods=['get'])
    def others_in_progress_or_cancelled(self, request):
        """GET /api/tasks/others_in_progress_or_cancelled/ - Задачи других пользователей в работе или отмененные"""
        tasks = Task.objects.filter(
            ~Q(created_by=request.user)
            & (Q(status__name='В работе') | Q(status__name='Отменена'))
        )

        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """POST /api/tasks/{id}/change_status/ - Изменить статус задачи"""
        task = self.get_object()  # Получаем задачу
        new_status_id = request.data.get('status_id')  # Получаем ID нового статуса из body

        if not new_status_id:
            return Response({'error': 'Укажите status_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_status = Status.objects.get(id=new_status_id)  # Находим статус
            task.status = new_status  # Меняем статус
            task.save()  # Сохраняем

            return Response({
                'status': 'success',
                'message': f'Статус задачи изменен на "{new_status.name}"',
                'task': TaskSerializer(task).data
            })
        except Status.DoesNotExist:
            return Response({'error': 'Статус не найден'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """GET /api/tasks/{id}/history/ - История изменений задачи"""
        task = self.get_object()
        history_records = task.history.all()  # Получаем историю изменений (simple_history)

        history_data = []
        for record in history_records:
            history_data.append({
                'id': record.history_id,
                'title': record.title,
                'status': record.status.name if record.status else None,
                'changed_at': record.history_date,
                'changed_by': record.history_user.username if record.history_user else 'Система',
                'change_type': record.get_history_type_display()  # Created, Changed, Deleted
            })

        return Response(history_data)
