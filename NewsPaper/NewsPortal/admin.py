from django.contrib import admin

from .models import Author, Category, Post, PostCategory, Comment, CategorySubscribers


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')


class CategorySubscribersAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'user')


# Register your models here.
admin.site.register(CategorySubscribers)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
