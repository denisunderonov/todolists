from django.urls import path, include  # Для создания URL путей
from rest_framework.routers import DefaultRouter  # Автоматический роутинг для ViewSets
from . import views  # Импортируем наши views

# Создаем роутер для автоматической генерации URLs
router = DefaultRouter()  # DefaultRouter автоматически создает пути для ViewSets

# Регистрируем ViewSets в роутере
# router.register(prefix, viewset, basename) - prefix это префикс URL
router.register(r'priorities', views.PriorityViewSet, basename='priority')  # /api/priorities/
router.register(r'statuses', views.StatusViewSet, basename='status')  # /api/statuses/
router.register(r'tags', views.TagViewSet, basename='tag')  # /api/tags/
router.register(r'projects', views.ProjectViewSet, basename='project')  # /api/projects/
router.register(r'tasks', views.TaskViewSet, basename='task')  # /api/tasks/
router.register(r'users', views.UserViewSet, basename='user')  # /api/users/

# URL patterns для приложения tasks
urlpatterns = [
    path('', include(router.urls)),  # Подключаем все URLs из роутера
]
