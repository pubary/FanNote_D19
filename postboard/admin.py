from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'time')
    list_display_links = ('title', 'author',)
    search_fields = ('author', 'title', )
    list_editable = ('category',)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'time')
    list_display_links = ('author',)
    search_fields = ('author',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('cat_name', 'slug')
    list_display_links = ('cat_name',)
    exclude = ['slug']


admin.site.register(Post, PostAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Category, CategoryAdmin)
