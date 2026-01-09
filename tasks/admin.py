from django.contrib import admin  # Импортируем модуль админки Django
from django.utils.html import format_html  # Для форматирования HTML в админке
from django.urls import reverse  # Для создания ссылок на другие объекты
from import_export.admin import ImportExportModelAdmin  # Для экспорта в Excel
from import_export import resources  # Для настройки экспорта
from simple_history.admin import SimpleHistoryAdmin  # Для отображения истории изменений
from .models import Priority, Status, Tag, Project, Task  # Импортируем наши модели


# Ресурс для экспорта Priority в Excel
class PriorityResource(resources.ModelResource):
    class Meta:
        model = Priority  # Модель для экспорта
        fields = ('id', 'name', 'level')  # Поля для экспорта
        export_order = ('id', 'name', 'level')  # Порядок полей в Excel


# Админка для модели Priority (Приоритет)
@admin.register(Priority)
class PriorityAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):  # Подключаем экспорт и историю
    resource_class = PriorityResource  # Класс для экспорта
    
    list_display = ('id', 'name', 'level', 'colored_level')  # Поля в списке объектов
    list_display_links = ('id', 'name')  # Поля-ссылки на детальную страницу
    list_filter = ('level',)  # Фильтры в боковой панели
    search_fields = ('name',)  # Поля для поиска
    ordering = ('level',)  # Сортировка по умолчанию
    
    fieldsets = (  # Группировка полей на странице редактирования
        ('Основная информация', {  # Название группы
            'fields': ('name', 'level')  # Поля в группе
        }),
    )
    
    @admin.display(description='Уровень (цветной)')  # Описание колонки в админке
    def colored_level(self, obj):  # Собственный метод для отображения уровня с цветом
        colors = {1: '#28a745', 2: '#17a2b8', 3: '#ffc107', 4: '#fd7e14', 5: '#dc3545'}  # Цвета по уровням
        color = colors.get(obj.level, '#6c757d')  # Получаем цвет или серый по умолчанию
        return format_html(  # Форматируем HTML
            '<span style="color: {}; font-weight: bold;">Уровень {}</span>',
            color, obj.level
        )


# Ресурс для экспорта Status в Excel
class StatusResource(resources.ModelResource):
    class Meta:
        model = Status
        fields = ('id', 'name', 'color')
        export_order = ('id', 'name', 'color')


# Админка для модели Status (Статус)
@admin.register(Status)
class StatusAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = StatusResource
    
    list_display = ('id', 'name', 'color_display')  # Поля в списке
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'color')
        }),
    )
    
    @admin.display(description='Цвет (превью)')  # Кастомный метод для отображения цвета
    def color_display(self, obj):
        return format_html(  # Показываем квадратик с цветом
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #000;"></div>',
            obj.color
        )


# Ресурс для экспорта Tag в Excel
class TagResource(resources.ModelResource):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'user__username')  # __ для связанных полей
        export_order = ('id', 'name', 'color', 'user__username')


# Админка для модели Tag (Тег)
@admin.register(Tag)
class TagAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = TagResource
    
    list_display = ('id', 'name', 'color_preview', 'user_link')  # Поля в списке
    list_display_links = ('id', 'name')
    list_filter = ('user', 'color')  # Фильтры
    search_fields = ('name', 'user__username')  # Поиск по имени тега и имени пользователя
    raw_id_fields = ('user',)  # Виджет для выбора пользователя (удобно при большом количестве)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'color', 'user')
        }),
    )
    
    @admin.display(description='Цвет')
    def color_preview(self, obj):
        return format_html(
            '<span style="background-color: {}; padding: 3px 10px; border-radius: 3px; color: white;">{}</span>',
            obj.color, obj.name
        )
    
    @admin.display(description='Пользователь')  # Гиперссылка на пользователя
    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.id])  # URL страницы пользователя
        return format_html('<a href="{}">{}</a>', url, obj.user.username)  # Ссылка


# Ресурс для экспорта Project в Excel
class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'owner__username', 'created_at', 'updated_at')
        export_order = ('id', 'name', 'owner__username', 'created_at', 'updated_at')


# Inline для отображения задач внутри проекта
class TaskInline(admin.TabularInline):  # Табличное отображение
    model = Task  # Модель для inline
    extra = 0  # Количество пустых форм для добавления
    fields = ('title', 'status', 'priority', 'assigned_to', 'due_date')  # Поля в inline
    readonly_fields = ('created_at',)  # Поля только для чтения
    raw_id_fields = ('assigned_to', 'priority', 'status')  # Виджеты для FK
    show_change_link = True  # Показывать ссылку на редактирование задачи


# Админка для модели Project (Проект)
@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = ProjectResource
    
    list_display = ('id', 'name', 'owner_link', 'tasks_count', 'created_at', 'updated_at')  # Поля в списке
    list_display_links = ('id', 'name')
    list_filter = ('owner', 'created_at')  # Фильтры
    search_fields = ('name', 'description', 'owner__username')  # Поиск
    raw_id_fields = ('owner',)
    readonly_fields = ('created_at', 'updated_at')  # Поля только для чтения
    date_hierarchy = 'created_at'  # Навигация по датам вверху списка
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'owner')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Свернутая секция
        }),
    )
    
    inlines = [TaskInline]  # Встроенное отображение задач
    
    @admin.display(description='Владелец')  # Ссылка на владельца
    def owner_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.owner.id])
        return format_html('<a href="{}">{}</a>', url, obj.owner.username)
    
    @admin.display(description='Количество задач')  # Кастомный метод: количество задач в проекте
    def tasks_count(self, obj):
        count = obj.tasks.count()  # Подсчитываем задачи через related_name
        return format_html('<b>{}</b>', count)


# Ресурс для экспорта Task в Excel с кастомизацией
class TaskResource(resources.ModelResource):
    
    # Метод 1: get_export_queryset - фильтруем только задачи с высоким приоритетом (4-5)
    def get_export_queryset(self, queryset):
        """Экспортируем только задачи с высоким приоритетом (уровень >= 4)"""
        return queryset.filter(priority__level__gte=4).select_related('project', 'priority', 'status', 'assigned_to')
    
    # Метод 2: dehydrate_due_date - преобразуем дату в формат DD-MM-YYYY
    def dehydrate_due_date(self, task):
        """Преобразуем дату в формат DD-MM-YYYY HH:MM"""
        if task.due_date:
            return task.due_date.strftime('%d-%m-%Y %H:%M')  # Форматируем дату
        return 'Без срока'  # Если даты нет
    
    # Метод 3: get_status - преобразуем статус в читаемый формат
    def get_status(self, task):
        """Преобразуем статус в читаемый формат с эмодзи"""
        if task.status:
            status_emoji = {  # Словарь соответствия статусов и эмодзи
                'Новая': '🆕',
                'В работе': '⚙️',
                'На проверке': '🔍',
                'Завершена': '✅',
                'Отменена': '❌',
            }
            emoji = status_emoji.get(task.status.name, '📋')  # Получаем эмодзи или дефолтный
            return f'{emoji} {task.status.name}'  # Возвращаем статус с эмодзи
        return '❓ Без статуса'
    
    class Meta:
        model = Task
        fields = ('id', 'title', 'project__name', 'priority__name', 'status', 'assigned_to__username', 'due_date', 'created_at')
        export_order = ('id', 'title', 'project__name', 'priority__name', 'status', 'assigned_to__username', 'due_date', 'created_at')


# Админка для модели Task (Задача)
@admin.register(Task)
class TaskAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = TaskResource
    
    list_display = ('id', 'title', 'project_link', 'status', 'priority_display', 'assigned_to_link', 'due_date', 'created_at')  # Поля в списке
    list_display_links = ('id', 'title')
    list_filter = ('status', 'priority', 'project', 'created_at', 'due_date')  # Фильтры
    search_fields = ('title', 'description', 'project__name', 'assigned_to__username')  # Поиск
    raw_id_fields = ('project', 'priority', 'status', 'assigned_to', 'created_by')  # Виджеты для FK
    readonly_fields = ('created_at', 'updated_at', 'image_preview')  # Поля только для чтения
    filter_horizontal = ('tags',)  # Виджет для ManyToMany (удобный выбор тегов)
    date_hierarchy = 'created_at'  # Навигация по датам
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'project')
        }),
        ('Параметры задачи', {
            'fields': ('priority', 'status', 'assigned_to', 'due_date')
        }),
        ('Дополнительно', {
            'fields': ('image', 'image_preview', 'tags'),
            'classes': ('collapse',)  # Свернутая секция
        }),
        ('Системная информация', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    @admin.display(description='Проект')  # Ссылка на проект
    def project_link(self, obj):
        url = reverse('admin:tasks_project_change', args=[obj.project.id])
        return format_html('<a href="{}">{}</a>', url, obj.project.name)
    
    @admin.display(description='Приоритет')  # Цветной приоритет
    def priority_display(self, obj):
        if obj.priority:
            colors = {1: '#28a745', 2: '#17a2b8', 3: '#ffc107', 4: '#fd7e14', 5: '#dc3545'}
            color = colors.get(obj.priority.level, '#6c757d')
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}</span>',
                color, obj.priority.name
            )
        return '-'
    
    @admin.display(description='Назначена')  # Ссылка на пользователя
    def assigned_to_link(self, obj):
        if obj.assigned_to:
            url = reverse('admin:auth_user_change', args=[obj.assigned_to.id])
            return format_html('<a href="{}">{}</a>', url, obj.assigned_to.username)
        return '-'
    
    @admin.display(description='Превью изображения')  # Превью прикрепленного изображения
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 300px;" />', obj.image.url)
        return 'Нет изображения'
