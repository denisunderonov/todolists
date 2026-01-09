from pathlib import Path
import os  # Для работы с переменными окружения

# Определяем базовую директорию проекта
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-%p8jy93-kt9^^ws46bi0^gvo7k$utehzg!n#w@)ll_nynu%qwg'

DEBUG = True

ALLOWED_HOSTS = ['*']  # Разрешаем все хосты для разработки и Docker


# Определение приложений

INSTALLED_APPS = [
    'django.contrib.admin',  # Админ-панель Django
    'django.contrib.auth',  # Система аутентификации пользователей
    'django.contrib.contenttypes',  # Система типов контента
    'django.contrib.sessions',  # Система сессий
    'django.contrib.messages',  # Система сообщений
    'django.contrib.staticfiles',  # Управление статическими файлами (CSS, JS, изображения)

    # Сторонние приложения
    'rest_framework',  # Django REST Framework для создания API
    'django_filters',  # Фильтрация данных в API
    'simple_history',  # Отслеживание истории изменений объектов
    'import_export',  # Импорт и экспорт данных в Excel

    # Наши приложения
    'tasks',  # Приложение для управления задачами
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Защита от различных атак
    'django.contrib.sessions.middleware.SessionMiddleware',  # Управление сессиями пользователей
    'django.middleware.common.CommonMiddleware',  # Общие функции (например, нормализация URL)
    'django.middleware.csrf.CsrfViewMiddleware',  # Защита от CSRF атак (подделка запросов)
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Аутентификация пользователей
    'django.contrib.messages.middleware.MessageMiddleware',  # Система сообщений
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Защита от clickjacking
    'simple_history.middleware.HistoryRequestMiddleware',  # Отслеживание кто изменял объекты
]

ROOT_URLCONF = 'todo_project.urls'  # Главный файл маршрутов (URLs)

TEMPLATES = [  # Настройки шаблонов (HTML)
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Движок шаблонов Django
        'DIRS': [],  # Дополнительные папки с шаблонами
        'APP_DIRS': True,  # Искать шаблоны в папках приложений
        'OPTIONS': {
            'context_processors': [  # Процессоры контекста (передают данные в шаблоны)
                'django.template.context_processors.debug',  # Информация для отладки
                'django.template.context_processors.request',  # Объект запроса
                'django.contrib.auth.context_processors.auth',  # Данные авторизации
                'django.contrib.messages.context_processors.messages',  # Сообщения пользователю
            ],
        },
    },
]

WSGI_APPLICATION = 'todo_project.wsgi.application'  # WSGI приложение для продакшена


# База данных
# Поддержка переменных окружения для Docker

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Используем PostgreSQL
        'NAME': os.environ.get('DATABASE_NAME', 'todo_db'),  # Из переменной окружения или 'todo_db'
        'USER': os.environ.get('DATABASE_USER', 'a1111'),  # Из переменной окружения или 'a1111'
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),  # Из переменной окружения или пусто
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),  # Из переменной окружения или 'localhost'
        'PORT': os.environ.get('DATABASE_PORT', '5432'),  # Из переменной окружения или '5432'
    }
}


# Валидаторы паролей

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Пароль не должен быть похож на личные данные
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Минимальная длина пароля
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Пароль не должен быть слишком распространенным
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Пароль не должен состоять только из цифр
    },
]


# Интернационализация (языки и форматы)

LANGUAGE_CODE = 'ru-ru'  # Язык интерфейса - русский

TIME_ZONE = 'Europe/Moscow'  # Часовой пояс - Москва

USE_I18N = True  # Включить интернационализацию (перевод интерфейса)

USE_TZ = True  # Использовать часовые пояса


# Статические файлы (CSS, JavaScript, изображения)

STATIC_URL = 'static/'  # URL для статических файлов (CSS, JS)
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Папка для сборки статики в продакшене

# Медиа-файлы (загружаемые пользователями файлы, например изображения)
MEDIA_URL = 'media/'  # URL для медиа-файлов
MEDIA_ROOT = BASE_DIR / 'media'  # Папка для хранения медиа-файлов

# Тип первичного ключа по умолчанию для моделей

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Автоинкрементный ID (большое целое число)

# Настройки Django REST Framework (для API)
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',  # Тип пагинации (по номерам страниц)
    'PAGE_SIZE': 10,  # Количество элементов на одной странице
    'DEFAULT_FILTER_BACKENDS': [  # Фильтры, которые будут доступны по умолчанию
        'django_filters.rest_framework.DjangoFilterBackend',  # Фильтрация через django-filter
        'rest_framework.filters.SearchFilter',  # Поиск по текстовым полям
        'rest_framework.filters.OrderingFilter',  # Сортировка по полям
    ],
}
