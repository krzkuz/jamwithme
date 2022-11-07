from django.contrib import admin
from .models import Post, Tag, Comment

class BookAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'id')

admin.site.register(Comment, BookAdmin)
admin.site.register(Post)
admin.site.register(Tag)
# admin.site.register(Comment)
