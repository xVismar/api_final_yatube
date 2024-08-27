from django.contrib import admin

from posts.models import Post, Comment, Group

empty_value_display = '-пусто-'
text = '__str__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'group', 'pub_date', text, 'image')
    list_editable = ('image', 'group')
    search_fields = ('text',)
    list_filter = ('pub_date', 'group', 'author')
    date_hierarchy = ('pub_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created', text)
    search_fields = ('content',)
    list_filter = ('author', 'created')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description')
    list_filter = ('title', 'slug')
    list_display_links = ('title',)
