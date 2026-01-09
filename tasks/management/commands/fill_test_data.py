from django.core.management.base import BaseCommand  # Базовый класс для management команд
from django.contrib.auth.models import User  # Модель пользователя
from tasks.models import Priority, Status, Tag, Project, Task  # Наши модели
from django.utils import timezone  # Для работы с датами
from datetime import timedelta  # Для работы с временными интервалами


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными (приоритеты, статусы, проекты, задачи)'  # Описание команды

    def add_arguments(self, parser):  # Добавляем аргументы команды
        parser.add_argument(  # Аргумент --clear для очистки данных перед заполнением
            '--clear',
            action='store_true',  # Это флаг (True/False)
            help='Очистить существующие данные перед заполнением',
        )

    def handle(self, *args, **options):  # Основная логика команды
        """Выполнение команды"""

        # Если передан флаг --clear, очищаем данные
        if options['clear']:
            self.stdout.write(self.style.WARNING('Очистка существующих данных...'))  # Выводим предупреждение
            Task.objects.all().delete()  # Удаляем все задачи
            Project.objects.all().delete()  # Удаляем все проекты
            Tag.objects.all().delete()  # Удаляем все теги
            Status.objects.all().delete()  # Удаляем все статусы
            Priority.objects.all().delete()  # Удаляем все приоритеты
            self.stdout.write(self.style.SUCCESS('✓ Данные очищены'))

        # Создаем приоритеты
        self.stdout.write('Создание приоритетов...')
        priorities_data = [  # Данные для приоритетов
            {'name': 'Очень низкий', 'level': 1},
            {'name': 'Низкий', 'level': 2},
            {'name': 'Средний', 'level': 3},
            {'name': 'Высокий', 'level': 4},
            {'name': 'Критический', 'level': 5},
        ]

        priorities = {}  # Словарь для хранения созданных приоритетов
        for data in priorities_data:
            priority, created = Priority.objects.get_or_create(**data)  # Создаем или получаем существующий
            priorities[data['level']] = priority  # Сохраняем в словарь
            if created:
                self.stdout.write(f'  ✓ Создан приоритет: {priority.name}')

        # Создаем статусы
        self.stdout.write('Создание статусов...')
        statuses_data = [
            {'name': 'Новая', 'color': '#6c757d'},  # Серый
            {'name': 'В работе', 'color': '#007bff'},  # Синий
            {'name': 'На проверке', 'color': '#ffc107'},  # Желтый
            {'name': 'Завершена', 'color': '#28a745'},  # Зеленый
            {'name': 'Отменена', 'color': '#dc3545'},  # Красный
        ]

        statuses = {}
        for data in statuses_data:
            status, created = Status.objects.get_or_create(**data)
            statuses[data['name']] = status
            if created:
                self.stdout.write(f'  ✓ Создан статус: {status.name}')

        # Получаем или создаем пользователя
        self.stdout.write('Проверка пользователя...')
        user, created = User.objects.get_or_create(
            username='testuser',  # Тестовый пользователь
            defaults={
                'email': 'test@example.com',
                'first_name': 'Тест',
                'last_name': 'Пользователь',
            }
        )
        if created:
            user.set_password('testpass123')  # Устанавливаем пароль
            user.save()
            self.stdout.write(f'  ✓ Создан пользователь: {user.username}')
        else:
            self.stdout.write(f'  → Пользователь уже существует: {user.username}')

        # Создаем теги
        self.stdout.write('Создание тегов...')
        tags_data = [
            {'name': 'Работа', 'color': '#007bff', 'user': user},
            {'name': 'Личное', 'color': '#28a745', 'user': user},
            {'name': 'Срочно', 'color': '#dc3545', 'user': user},
            {'name': 'Важно', 'color': '#ffc107', 'user': user},
        ]

        tags = {}
        for data in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=data['name'],
                user=data['user'],
                defaults={'color': data['color']}
            )
            tags[data['name']] = tag
            if created:
                self.stdout.write(f'  ✓ Создан тег: {tag.name}')

        # Создаем проекты
        self.stdout.write('Создание проектов...')
        projects_data = [
            {
                'name': 'Разработка сайта',
                'description': 'Проект по разработке корпоративного сайта',
                'owner': user
            },
            {
                'name': 'Личные дела',
                'description': 'Личные задачи и покупки',
                'owner': user
            },
            {
                'name': 'Курсовая работа',
                'description': 'Выполнение курсовой работы по Django',
                'owner': user
            },
        ]

        projects = {}
        for data in projects_data:
            project, created = Project.objects.get_or_create(
                name=data['name'],
                owner=data['owner'],
                defaults={'description': data['description']}
            )
            projects[data['name']] = project
            if created:
                self.stdout.write(f'  ✓ Создан проект: {project.name}')

        # Создаем задачи
        self.stdout.write('Создание задач...')
        today = timezone.now()  # Текущая дата и время

        tasks_data = [
            {
                'title': 'Создать дизайн главной страницы',
                'description': 'Разработать макет главной страницы в Figma',
                'project': projects['Разработка сайта'],
                'priority': priorities[4],  # Высокий
                'status': statuses['В работе'],
                'due_date': today + timedelta(days=3),
                'tags': [tags['Работа'], tags['Важно']],
            },
            {
                'title': 'Настроить базу данных',
                'description': 'Создать модели и миграции для проекта',
                'project': projects['Разработка сайта'],
                'priority': priorities[5],  # Критический
                'status': statuses['Завершена'],
                'due_date': today - timedelta(days=1),  # Вчера
                'tags': [tags['Работа']],
            },
            {
                'title': 'Купить продукты',
                'description': 'Молоко, хлеб, яйца',
                'project': projects['Личные дела'],
                'priority': priorities[2],  # Низкий
                'status': statuses['Новая'],
                'due_date': today + timedelta(days=1),
                'tags': [tags['Личное']],
            },
            {
                'title': 'Написать введение',
                'description': 'Написать введение к курсовой работе',
                'project': projects['Курсовая работа'],
                'priority': priorities[3],  # Средний
                'status': statuses['На проверке'],
                'due_date': today + timedelta(days=7),
                'tags': [tags['Важно']],
            },
            {
                'title': 'Провести тестирование API',
                'description': 'Протестировать все endpoints REST API',
                'project': projects['Разработка сайта'],
                'priority': priorities[4],  # Высокий
                'status': statuses['Новая'],
                'due_date': today + timedelta(days=5),
                'tags': [tags['Работа'], tags['Срочно']],
            },
        ]

        for data in tasks_data:
            tags_list = data.pop('tags')  # Извлекаем теги отдельно
            task, created = Task.objects.get_or_create(
                title=data['title'],
                project=data['project'],
                defaults={
                    **data,
                    'created_by': user,
                    'assigned_to': user,
                }
            )
            if created:
                task.tags.set(tags_list)  # Устанавливаем теги (ManyToMany)
                self.stdout.write(f'  ✓ Создана задача: {task.title}')

        # Итоговая статистика
        self.stdout.write(self.style.SUCCESS('\n=== Заполнение завершено ==='))
        self.stdout.write(f'Приоритетов: {Priority.objects.count()}')
        self.stdout.write(f'Статусов: {Status.objects.count()}')
        self.stdout.write(f'Тегов: {Tag.objects.count()}')
        self.stdout.write(f'Проектов: {Project.objects.count()}')
        self.stdout.write(f'Задач: {Task.objects.count()}')
        self.stdout.write(self.style.SUCCESS('\n✓ Команда выполнена успешно!'))
