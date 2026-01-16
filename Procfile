release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn todo_project.wsgi:application
