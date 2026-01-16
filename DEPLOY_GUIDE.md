# 📋 Руководство по деплою Django TODO List

## 🚀 Быстрый деплой на Render.com (РЕКОМЕНДУЕМЫЙ)

### Шаг 1: Подготовка репозитория
```bash
# Убедись, что все файлы закоммичены
git add .
git commit -m "Подготовка к деплою"
git push origin main
```

### Шаг 2: Создание аккаунта на Render.com
1. Перейди на https://render.com
2. Зарегистрируйся через GitHub
3. Авторизируй доступ к репозиториям

### Шаг 3: Создание Web Service
1. На dashboard Render нажми **"New +"**
2. Выбери **"Web Service"**
3. Найди и выбери репозиторий `course2sem`
4. Заполни параметры:
   - **Name:** `todo-list-app`
   - **Runtime:** `Python 3.9`
   - **Build Command:** `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command:** `gunicorn todo_project.wsgi:application`
   - **Plan:** Free (или Starter за $7/месяц)

### Шаг 4: Создание PostgreSQL базы данных
1. На dashboard нажми **"New +"**
2. Выбери **"PostgreSQL"**
3. Заполни параметры:
   - **Name:** `todolist-db`
   - **Database:** `todolist`
   - **User:** `todolist_user`
   - **Plan:** Free
4. Скопируй **Internal Database URL**

### Шаг 5: Настройка переменных окружения
В Web Service найди **"Environment"** и добавь:

```
DEBUG=False
SECRET_KEY=django-insecure-xxxxxxxxxxxxxxx  # Генерируем новый ключ!
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=postgresql://... (скопировать из БД)
```

### Шаг 6: Развертывание
Нажми **"Deploy"** — приложение развернётся автоматически!

---

## 💻 Локальное тестирование перед деплоем

```bash
# 1. Установить зависимости
pip install -r requirements.txt
pip install gunicorn

# 2. Создать .env файл
cp .env.example .env
# Отредактировать .env с локальными настройками

# 3. Запустить миграции
python manage.py migrate

# 4. Собрать статические файлы
python manage.py collectstatic --noinput

# 5. Тестовый запуск с gunicorn
gunicorn todo_project.wsgi:application --bind 127.0.0.1:8000
```

---

## 📝 Коррекция settings.py для production

Добавь в конец `todo_project/settings.py`:

```python
# Production settings
if not DEBUG:
    # HTTPS
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Security headers
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Allowed hosts from environment
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
    
    # Database from environment variable
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
```

---

## 🐳 Альтернатива: Docker + Railway.app

### Шаг 1: Подготовка
```bash
git push origin main
```

### Шаг 2: На Railway.app
1. Зарегистрируйся на https://railway.app
2. New Project → GitHub Repo
3. Выбери `course2sem`
4. Railway автоматически обнаружит `Dockerfile`

### Шаг 3: Переменные окружения
Добавь в Railway:
```
DEBUG=False
SECRET_KEY=your-secure-key
DATABASE_URL=postgresql://...
```

### Шаг 4: Deploy
Railway автоматически деплоится на каждый push!

---

## 🔧 Альтернатива: Docker + DigitalOcean (Full Control)

### Требования
- DigitalOcean App или Droplet ($5/месяц)
- Docker installed

### Шаги
```bash
# 1. Создать DigitalOcean Droplet (Ubuntu 22.04)

# 2. SSH на сервер
ssh root@your_droplet_ip

# 3. Установить Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 4. Клонировать репозиторий
git clone https://github.com/denisunderonov/course2sem.git
cd course2sem

# 5. Создать .env файл
nano .env
# Добавить все переменные

# 6. Запустить с docker-compose
docker-compose up -d

# 7. Миграции
docker-compose exec web python manage.py migrate

# 8. Создать суперпользователя
docker-compose exec web python manage.py createsuperuser
```

---

## ✅ Чек-лист перед деплоем

- [ ] `DEBUG = False` в production settings
- [ ] `SECRET_KEY` изменён на новый (НИКОГДА не коммитить старый)
- [ ] `ALLOWED_HOSTS` правильно настроены
- [ ] `STATIC_ROOT` указана (для collectstatic)
- [ ] `MEDIA_ROOT` указана
- [ ] PostgreSQL база создана
- [ ] Переменные окружения добавлены в платформу деплоя
- [ ] Миграции запущены (`python manage.py migrate`)
- [ ] Статические файлы собраны (`python manage.py collectstatic`)
- [ ] Суперпользователь создан (`python manage.py createsuperuser`)
- [ ] Все требуемые пакеты в requirements.txt

---

## 🚨 Частые ошибки и решения

### Ошибка: "Database connection refused"
**Решение:** Убедись, что DATABASE_URL правильно скопирован из хостинга БД

### Ошибка: "Static files not found"
**Решение:** Запусти `python manage.py collectstatic --noinput`

### Ошибка: "Secret key not set"
**Решение:** Сгенерируй новый ключ:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Ошибка: "Allowed host not configured"
**Решение:** Добавь домен в `ALLOWED_HOSTS` в settings.py или в переменную окружения

---

## 📞 Полезные команды

```bash
# Просмотр логов на Render
# Веб-интерфейс: Dashboard → Logs

# SSH на контейнер
docker exec -it todo_web bash

# Пересоздать контейнер
docker-compose down
docker-compose up -d

# Очистить статику и пересобрать
python manage.py collectstatic --clear --noinput
```

---

## 💡 Рекомендация

**ДЛЯ НАЧИНАЮЩИХ:** Render.com + Free план (самый простой способ)
**ДЛЯ PRODUCTION:** Railway.app ($7/месяц) или DigitalOcean ($5/месяц)
