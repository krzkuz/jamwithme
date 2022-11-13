from django.contrib import admin
from .models import Message, Conversation

class BookAdmin(admin.ModelAdmin):
    readonly_fields = ('updated', 'id')

admin.site.register(Conversation, BookAdmin)

# admin.site.register(Conversation)
admin.site.register(Message)

