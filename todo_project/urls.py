"""
URL configuration for todo_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin  # Админ-панель Django
from django.urls import path, include  # Для создания URL путей
from django.conf import settings  # Настройки проекта
from django.conf.urls.static import static  # Для раздачи медиа-файлов в режиме разработки
from tasks.views import home_view, projects_view, tasks_view  # HTML views

urlpatterns = [
    path('', home_view, name='home'),  # Главная страница
    path('projects/', projects_view, name='projects'),  # Страница проектов
    path('tasks/', tasks_view, name='tasks'),  # Страница задач
    path('admin/', admin.site.urls),  # Админ-панель: http://127.0.0.1:8000/admin/
    path('api/', include('tasks.urls')),  # API приложения tasks: http://127.0.0.1:8000/api/
    path('api-auth/', include('rest_framework.urls')),  # Аутентификация DRF (для browsable API)
]

# Раздача медиа-файлов в режиме разработки (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Доступ к загруженным изображениям
