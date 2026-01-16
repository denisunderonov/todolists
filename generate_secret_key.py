"""
Скрипт для генерации безопасного SECRET_KEY для Django

Использование:
    python generate_secret_key.py
"""

from django.core.management.utils import get_random_secret_key

if __name__ == '__main__':
    print("Сгенерированный SECRET_KEY:")
    print("=" * 60)
    print(get_random_secret_key())
    print("=" * 60)
    print("\nКопируй это значение в переменную окружения SECRET_KEY")
