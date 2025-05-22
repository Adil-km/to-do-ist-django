from django.contrib import admin

from . models import TodoList
# Register your models here.


@admin.register(TodoList)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'is_checked', 'created_at')
    list_filter = ('is_checked', 'user')
    search_fields = ('task', 'user__username')