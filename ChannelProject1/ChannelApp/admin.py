from django.contrib import admin
from .models import Group, Chat

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'groupName')
    search_fields = ('groupName',)

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'Gname', 'content', 'timestamp')
    search_fields = ('content',)
    list_filter = ('Gname', 'timestamp')
    ordering = ('-timestamp',)
