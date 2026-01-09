# Django TODO List - Курсовой проект

## Описание
REST API для управления задачами (TODO list) с расширенными возможностями:
- 5 моделей данных с отслеживанием истории
- Валидация полей через serializers
- Сложные Q-запросы с OR, AND, NOT
- 5 видов фильтрации
- Пагинация и сортировка
- Админ-панель с 15+ настройками
- Экспорт в Excel с кастомизацией
- Management команды
- @action методы в ViewSets
- Linter (flake8)
- Docker поддержка

## Технологии
- Django 4.2.27
- Django REST Framework 3.16.1
- PostgreSQL
- django-filter 25.1
- django-simple-history 3.10.1
- django-import-export 4.3.14
- Docker & Docker Compose

## Запуск локально

### 1. Клонируйте репозиторий
```bash
git clone <url>
cd course2sem
```

### 2. Создайте виртуальное окружение
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# или
venv\Scripts\activate  # Windows
```

### 3. Установите зависимости
```bash
pip install -r requirements.txt
```

### 4. Настройте PostgreSQL
Убедитесь, что PostgreSQL установлен и создана база данных `todo_db`:
```bash
psql postgres
CREATE DATABASE todo_db;
\q
```

### 5. Примените миграции
```bash
python manage.py migrate
```

### 6. Создайте суперпользователя
```bash
python manage.py createsuperuser
```

### 7. Загрузите тестовые данные (опционально)
```bash
python manage.py fill_test_data
```

### 8. Запустите сервер
```bash
python manage.py runserver
```

Приложение будет доступно по адресу: http://127.0.0.1:8000/

## Запуск в Docker

### 1. Убедитесь, что Docker и Docker Compose установлены
```bash
docker --version
docker-compose --version
```

### 2. Настройте пароль базы данных
Отредактируйте `docker-compose.yml` и измените `yourpassword` на свой пароль в двух местах:
- `db.environment.POSTGRES_PASSWORD`
- `web.environment.DATABASE_PASSWORD`

### 3. Запустите контейнеры
```bash
docker-compose up --build
```

Приложение будет доступно по адресу: http://localhost:8000/

### 4. Создайте суперпользователя в Docker (в новом терминале)
```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Загрузите тестовые данные в Docker (опционально)
```bash
docker-compose exec web python manage.py fill_test_data
```

### 6. Остановите контейнеры
```bash
docker-compose down
```

## API Endpoints

### Базовые CRUD операции
- `/api/priorities/` - Приоритеты задач
- `/api/statuses/` - Статусы задач
- `/api/tags/` - Теги
- `/api/projects/` - Проекты
- `/api/tasks/` - Задачи

### Дополнительные @action методы
- `GET /api/projects/{id}/tasks/` - Все задачи проекта
- `GET /api/projects/my_projects/` - Мои проекты (где я владелец)
- `GET /api/tasks/upcoming_week/` - Задачи на следующую неделю
- `GET /api/tasks/overdue/` - Просроченные задачи
- `GET /api/tasks/urgent_or_tomorrow/` - Срочные или на завтра
- `GET /api/tasks/others_in_progress_or_cancelled/` - Задачи других пользователей
- `POST /api/tasks/{id}/change_status/` - Изменить статус задачи
- `GET /api/tasks/{id}/history/` - История изменений задачи

### Фильтрация задач
```bash
# По приоритету
GET /api/tasks/?priority__level__gte=4

# По проекту
GET /api/tasks/?project=1

# По статусу
GET /api/tasks/?status__name=В работе

# По дате создания
GET /api/tasks/?created_at__date__gte=2024-01-01

# Поиск по названию
GET /api/tasks/?search=название

# Сортировка
GET /api/tasks/?ordering=-created_at
```

## Админ-панель
Доступна по адресу: http://127.0.0.1:8000/admin/

Возможности:
- Просмотр и редактирование всех моделей
- Фильтры по полям
- Поиск
- Inline редактирование связанных объектов
- Экспорт в Excel/CSV/JSON
- История изменений (django-simple-history)
- Кастомные методы отображения (цветные приоритеты, превью изображений)

## Linter
Проверка кода с помощью flake8:
```bash
flake8 tasks/ todo_project/
```

Конфигурация находится в файле `.flake8`

## Management команды

### fill_test_data
Заполняет базу тестовыми данными:
```bash
python manage.py fill_test_data

# С очисткой существующих данных
python manage.py fill_test_data --clear
```

Создает:
- 5 приоритетов
- 5 статусов
- 4 тега
- 3 проекта
- 5 задач
- Тестового пользователя (testuser)

## Структура проекта
```
course2sem/
├── tasks/                      # Основное приложение
│   ├── models.py              # Модели данных
│   ├── serializers.py         # Сериализаторы REST API
│   ├── views.py               # ViewSets и логика API
│   ├── admin.py               # Конфигурация админ-панели
│   ├── urls.py                # URL маршруты
│   └── management/
│       └── commands/
│           └── fill_test_data.py  # Команда для тестовых данных
├── todo_project/              # Настройки проекта
│   ├── settings.py           # Конфигурация Django
│   └── urls.py               # Главные URL маршруты
├── Dockerfile                # Docker образ
├── docker-compose.yml        # Docker Compose конфигурация
├── .dockerignore            # Исключения для Docker
├── .flake8                  # Конфигурация linter
├── requirements.txt         # Python зависимости
└── manage.py               # Django CLI
```

## Модели данных

### Priority (Приоритет)
- `name` - Название
- `level` - Уровень (1-5)
- `color` - Цветовой код
- История изменений

### Status (Статус)
- `name` - Название
- `description` - Описание
- История изменений

### Tag (Тег)
- `name` - Название
- `color` - Цветовой код
- История изменений

### Project (Проект)
- `title` - Название
- `description` - Описание
- `owner` - Владелец
- `created_at` - Дата создания
- `image` - Изображение
- История изменений

### Task (Задача)
- `title` - Название
- `description` - Описание
- `project` - Проект
- `priority` - Приоритет
- `status` - Статус
- `tags` - Теги (M2M)
- `due_date` - Срок выполнения
- `assigned_to` - Назначена пользователю
- `created_by` - Создал
- `created_at` - Дата создания
- История изменений

## Валидация
- Уровень приоритета: 1-5
- Срок выполнения: не в прошлом
- Уникальность названия задачи внутри проекта

## Автор
Курсовой проект по Django REST Framework
