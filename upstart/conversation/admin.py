from django.contrib import admin
from .models import Conversation, ConversationMessage

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('item', 'display_members', 'created_at', 'modified_at')
    list_filter = ('created_at', 'modified_at')
    search_fields = ('item__name', 'members__username')
    readonly_fields = ('created_at', 'modified_at')
    filter_horizontal = ('members',)  # For better management of many-to-many relationships

    def display_members(self, obj):
        return ", ".join([member.username for member in obj.members.all()])
    display_members.short_description = 'Members'

admin.site.register(Conversation, ConversationAdmin)

class ConversationMessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'created_by', 'created_at', 'short_content')
    list_filter = ('created_at', 'created_by')
    search_fields = ('content', 'created_by__username', 'conversation__item__name')
    readonly_fields = ('created_at',)

    def short_content(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    short_content.short_description = 'Message Content'

admin.site.register(ConversationMessage, ConversationMessageAdmin)
