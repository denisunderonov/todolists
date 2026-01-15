#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_project.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='denisunderonov').exists():
    User.objects.create_superuser('denisunderonov', 'denisunderonov@example.com', 'Denimz13.')
    print("✅ Суперпользователь создан!")
else:
    user = User.objects.get(username='denisunderonov')
    user.set_password('Denimz13.')
    user.save()
    print("✅ Пароль обновлен!")

print("📧 Логин: denisunderonov")
print("🔐 Пароль: Denimz13.")
