import multiprocessing
import os

# Основные настройки
bind = f"0.0.0.0:{os.environ.get('PORT', 8000)}"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Логирование
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Процесс
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Сервер
preload_app = True
max_requests = 1000
max_requests_jitter = 50
