from rest_framework import serializers  # Импортируем модуль сериализаторов
from django.contrib.auth.models import User  # Модель пользователя
from .models import Priority, Status, Tag, Project, Task  # Наши модели


# Сериализатор для модели Priority (Приоритет)
class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority  # Модель для сериализации
        fields = '__all__'  # Все поля модели

    def validate_level(self, value):  # Кастомная валидация уровня приоритета
        """Проверяем, что уровень приоритета в диапазоне 1-5"""
        if value < 1 or value > 5:  # Если уровень вне диапазона
            raise serializers.ValidationError('Уровень приоритета должен быть от 1 до 5')  # Выбрасываем ошибку
        return value  # Возвращаем валидное значение


# Сериализатор для модели Status (Статус)
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


# Сериализатор для модели Tag (Тег)
class TagSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)  # Добавляем имя пользователя (только чтение)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'user', 'user_username']  # Указываем поля явно
        extra_kwargs = {  # Дополнительные настройки полей
            'user': {'write_only': True}  # user только для записи (не показывать в ответе)
        }


# Сериализатор для модели Project (Проект)
class ProjectSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)  # Имя владельца
    tasks_count = serializers.SerializerMethodField()  # Кастомное поле - количество задач

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'owner_username', 'image', 'tasks_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']  # Эти поля только для чтения

    def get_tasks_count(self, obj):  # Метод для получения количества задач
        """Возвращает количество задач в проекте"""
        return obj.tasks.count()


# Упрощенный сериализатор для Project (для вложенных объектов)
class ProjectListSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'owner_username']


# Сериализатор для модели Task (Задача)
class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)  # Название проекта
    priority_name = serializers.CharField(source='priority.name', read_only=True)  # Название приоритета
    priority_details = PrioritySerializer(source='priority', read_only=True)  # Полная информация о приоритете
    status_name = serializers.CharField(source='status.name', read_only=True)  # Название статуса
    status_details = StatusSerializer(source='status', read_only=True)  # Полная информация о статусе
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)  # Имя ответственного
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)  # Кто создал
    tags_list = TagSerializer(source='tags', many=True, read_only=True)  # Список тегов (вложенный сериализатор)
    tags_details = TagSerializer(source='tags', many=True, read_only=True)  # Альтернативное название для тегов

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'project', 'project_name',
            'priority', 'priority_name', 'priority_details',
            'status', 'status_name', 'status_details',
            'assigned_to', 'assigned_to_username', 'due_date', 'image',
            'tags', 'tags_list', 'tags_details', 'created_at', 'updated_at',
            'created_by', 'created_by_username'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_due_date(self, value):  # Кастомная валидация даты окончания
        """Проверяем, что дата окончания не раньше текущей даты"""
        from django.utils import timezone  # Импортируем для работы с датами
        if value and value < timezone.now():  # Если дата в прошлом
            raise serializers.ValidationError('Дата окончания не может быть в прошлом')
        return value

    def validate(self, data):  # Общая валидация всех полей сразу
        """Проверяем уникальность названия задачи для пользователя"""
        request = self.context.get('request')  # Получаем request из контекста
        if request and request.user:  # Если есть пользователь
            title = data.get('title')  # Название задачи
            project = data.get('project')  # Проект
            # Проверяем, есть ли уже задача с таким названием в этом проекте
            if Task.objects.filter(project=project, title=title).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise serializers.ValidationError({'title': 'Задача с таким названием уже существует в данном проекте'})
        return data


# Упрощенный сериализатор для списка задач
class TaskListSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    status_name = serializers.CharField(source='status.name', read_only=True)
    priority_name = serializers.CharField(source='priority.name', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'project_name', 'status_name', 'priority_name', 'due_date', 'created_at']


# Сериализатор для User (для отображения в API)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']
