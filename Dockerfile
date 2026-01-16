# Используем официальный Python образ
FROM python:3.9-slim

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копируем весь проект
COPY . .

# Собираем статические файлы
RUN python manage.py collectstatic --noinput --clear

# Открываем порт
EXPOSE 8000

# Команда для запуска сервера с gunicorn
CMD ["gunicorn", "--config", "gunicorn_config.py", "todo_project.wsgi:application"]
